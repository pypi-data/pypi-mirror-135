# -*- coding: utf-8 -*-
"""
Army subplugin for hero-plugin, shows hero army creatures and counts.

------------------------------------------------------------------------------
This file is part of h3sed - Heroes3 Savegame Editor.
Released under the MIT License.

@created   21.03.2020
@modified  16.01.2022
------------------------------------------------------------------------------
"""
import copy
import logging

from h3sed import gui
from h3sed import metadata
from h3sed import plugins
from h3sed.lib import util
from h3sed.plugins.hero import POS


logger = logging.getLogger(__package__)


PROPS = {"name": "army", "label": "Army", "index": 5}
UIPROPS = [{
    "type":        "itemlist",
    "orderable":   True,
    "nullable":    True,
    "min":         1,
    "max":         7,
    "item": [{
        "type":    "label",
        "label":   "Army slot",
      }, {
        "name":    "name",
        "type":    "combo",
        "choices": None,  # Populated later
      }, {
        "name":    "count",
        "type":    "number",
        "min":     1,
        "max":     2**32 - 1,
      }, {
        "name":    "placeholder",
        "type":    "window",
    }]
}]


def props():
    """Returns props for army-tab, as {label, index}."""
    return PROPS


def factory(parent, hero, panel):
    """Returns a new army-plugin instance."""
    return ArmyPlugin(parent, hero, panel)



class ArmyPlugin(object):
    """Encapsulates army-plugin state and behaviour."""


    def __init__(self, parent, hero, panel):
        self.name    = PROPS["name"]
        self.parent  = parent
        self._hero   = hero
        self._panel  = panel # Plugin contents panel
        self._state  = []    # [{"name": "Roc", "count": 6}, {}, ]
        self._state0 = []    # Original state [{"name": "Roc", "count": 6}, {}, ]
        self._ctrls  = []    # [{"name": wx.ComboBox, "count": wx.SpinCtrl}, ]
        if hero:
            self.parse(hero.bytes)
            hero.army = self._state


    def props(self):
        """Returns props for army-tab, as [{type: "itemlist", ..}]."""
        result = []
        ver = self._hero.savefile.version
        cc = sorted(metadata.Store.get("creatures", version=ver))
        for prop in UIPROPS:
            myprop = dict(prop, item=[])
            for item in prop["item"]:
                myitem = dict(item, choices=cc) if "choices" in item else item
                myprop["item"].append(myitem)
            result.append(myprop)
        return result


    def state(self):
        """Returns data state for army-plugin, as [{"name": "Roc", "count": 6}, {}, ]."""
        return self._state


    def load(self, hero, panel=None):
        """Loads hero to plugin."""
        self._hero = hero
        self._state[:] = []
        if panel: self._panel = panel
        if hero:
            self.parse(hero.bytes)
            hero.army = self._state


    def load_state(self, state):
        """Loads plugin state from given data, ignoring unknown values. Returns whether state changed."""
        MYPROPS = self.props()
        state0 = type(self._state)(self._state)
        state = state + [{}] * (MYPROPS[0]["max"] - len(state))
        ver = self._hero.savefile.version
        cmap = {x.lower(): x for x in metadata.Store.get("creatures", version=ver)}
        countitem = next(x for x in MYPROPS[0]["item"] if "count" == x.get("name"))
        MIN, MAX = countitem["min"], countitem["max"]
        for i, v in enumerate(state):
            if not isinstance(v, (dict, type(None))):
                logger.warning("Invalid data type in army #%s: %r", i + 1, v)
                continue  # for
            name, count = v and v.get("name"), v and v.get("count")
            if name and hasattr(name, "lower") and name.lower() in cmap \
            and isinstance(count, int) and MIN <= count <= MAX:
                self._state[i] = {"name": cmap[name.lower()], "count": count}
            elif v in ({}, None):
                self._state[i] = {}
            else:
                logger.warning("Invalid army #%s: %r", i + 1, v)
        return state0 != self._state


    def render(self):
        """Populates controls from state, using existing if already built."""
        MYPROPS = self.props()
        if self._ctrls and all(all(x.values()) for x in self._ctrls):
            ver = self._hero.savefile.version
            cc = [""] + sorted(metadata.Store.get("creatures", version=ver))
            for i, row in enumerate(self._state):
                creature = None
                for prop in MYPROPS[0]["item"]:
                    if "name" not in prop: continue # for prop
                    name, choices = prop["name"], cc
                    ctrl, value = self._ctrls[i][name], self._state[i].get(name)
                    if "choices" in prop:
                        choices = ([value] if value and value not in cc else []) + cc
                        ctrl.SetItems(choices)
                        creature = value
                    else: ctrl.Show(not creature if "window" == prop.get("type") else bool(creature))
                    if value is not None and hasattr(ctrl, "Value"): ctrl.Value = value
        else:
            self._ctrls = gui.build(self, self._panel)[0]
            # Hide count controls where no creature type selected
            for i, row in enumerate(self._state):
                creature, size = None, None
                for prop in MYPROPS[0]["item"]:
                    if "name" not in prop: continue # for prop
                    name = prop["name"]
                    ctrl, value = self._ctrls[i][name], self._state[i].get(name)
                    if "choices" in prop: creature = value
                    else:  # Show blank placeholder instead of count-control
                        if "window" == prop.get("type"): ctrl.Size = ctrl.MinSize = size
                        ctrl.Show(not creature if "window" == prop.get("type") else bool(creature))
                    size = ctrl.Size
        self._panel.Layout()


    def on_change(self, prop, row, ctrl, value):
        """
        Handler for army change, enables or disables creature count.
        Returns True.
        """
        row[prop["name"]] = value
        if "name" == prop["name"]:
            if value and not row.get("count"):
                row["count"] = ctrl.GetNextSibling().Value = 1
            ctrl.GetNextSibling().Show(bool(value))
        return True


    def parse(self, bytes):
        """Builds army state from hero bytearray."""
        result = []

        NAMES = {x[y]: y for x in [metadata.Store.get("ids")]
                 for y in metadata.Store.get("creatures")}
        MYPOS = plugins.adapt(self, "pos", POS)

        for prop in self.props():
            for i in range(prop["max"]):
                unit  = util.bytoi(bytes[MYPOS["army_types"]  + i * 4:MYPOS["army_types"]  + i * 4 + 4])
                count = util.bytoi(bytes[MYPOS["army_counts"] + i * 4:MYPOS["army_counts"] + i * 4 + 4])
                name = NAMES.get(unit)
                if not unit or not count or not name: result.append({})
                else: result.append({"name": name, "count": count})
        self._state[:] = result
        self._state0 = copy.deepcopy(result)


    def serialize(self):
        """Returns new hero bytearray, with edited army section."""
        result = self._hero.bytes[:]
        bytes0 = self._hero.get_bytes(original=True)

        IDS = {y: x[y] for x in [metadata.Store.get("ids")]
               for y in metadata.Store.get("creatures")}
        MYPOS = plugins.adapt(self, "pos", POS)

        for prop in self.props():
            for i in range(prop["max"]):
                name, count = (self._state[i].get(x) for x in ("name", "count"))
                if (not name or not count) and not self._state0[i].get("name"):
                    # Retain original bytes unchanged, as game uses both 0x00 and 0xFF
                    b1 = bytes0[MYPOS["army_types"]  + i * 4:MYPOS["army_types"]  + i * 4 + 4]
                    b2 = bytes0[MYPOS["army_counts"] + i * 4:MYPOS["army_counts"] + i * 4 + 4]
                else:
                    b1, b2 = metadata.Blank * 4, metadata.Null * 4
                    if count and name in IDS:
                        b1 = util.itoby(IDS[name], 4)
                        b2 = util.itoby(count,     4)
                result[MYPOS["army_types"]  + i * 4:MYPOS["army_types"]  + i * 4 + 4] = b1
                result[MYPOS["army_counts"] + i * 4:MYPOS["army_counts"] + i * 4 + 4] = b2

        return result
