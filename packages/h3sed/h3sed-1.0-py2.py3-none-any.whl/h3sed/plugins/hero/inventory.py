# -*- coding: utf-8 -*-
"""
Inventory subplugin for hero-plugin, shows inventory artifacts list.

------------------------------------------------------------------------------
This file is part of h3sed - Heroes3 Savegame Editor.
Released under the MIT License.

@created   16.03.2020
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



PROPS = {"name": "inventory", "label": "Inventory", "index": 3}
UIPROPS = [{
    "type":        "itemlist",
    "orderable":   True,
    "nullable":    True,
    "min":          0,
    "max":         64,
    "item": [{
        "type":    "label",
        "label":   "Inventory slot",
      }, {
        "type":    "combo",
        "choices": None, # Populated later
    }]
}]



def props():
    """Returns props for inventory-tab, as {label, index}."""
    return PROPS


def factory(parent, hero, panel):
    """Returns a new inventory-plugin instance."""
    return InventoryPlugin(parent, hero, panel)



class InventoryPlugin(object):
    """Encapsulates inventory-plugin state and behaviour."""


    def __init__(self, parent, hero, panel):
        self.name    = PROPS["name"]
        self.parent  = parent
        self._hero   = hero
        self._panel  = panel # Plugin contents panel
        self._state  = []    # ["Skull Helmet", None, ..]
        self._state0 = []    # Original state ["Skull Helmet", None, ..]
        self._ctrls  = []    # [wx.ComboBox, ]
        if hero:
            self.parse(hero.bytes)
            hero.inventory = self._state


    def props(self):
        """Returns props for inventory-tab, as [{type: "itemlist", ..}]."""
        result = []
        ver = self._hero.savefile.version
        cc = sorted(metadata.Store.get("artifacts", version=ver, category="inventory"))
        for prop in UIPROPS:
            myprop = dict(prop, item=[])
            for item in prop["item"]:
                myitem = dict(item, choices=cc) if "choices" in item else item
                myprop["item"].append(myitem)
            result.append(myprop)
        return result


    def state(self):
        """Returns data state for inventory-plugin, as ["Skull Helmet", None, ..]."""
        return self._state


    def load(self, hero, panel=None):
        """Loads hero to plugin."""
        self._hero = hero
        self._state[:] = []
        if panel: self._panel = panel
        if hero:
            self.parse(hero.bytes)
            hero.inventory = self._state


    def load_state(self, state):
        """Loads plugin state from given data, ignoring unknown values. Returns whether state changed."""
        state0 = type(self._state)(self._state)
        state = state + [None] * (self.props()[0]["max"] - len(state))
        ver = self._hero.savefile.version
        cmap = {x.lower(): x for x in metadata.Store.get("artifacts", version=ver, category="inventory")}
        for i, v in enumerate(state):
            if v and hasattr(v, "lower") and v.lower() in cmap:
                self._state[i] = cmap[v.lower()]
            elif v in ("", None):
                self._state[i] = None
            else:
                logger.warning("Invalid inventory item #%s: %r", i + 1, v)
        return state0 != self._state


    def render(self):
        """Populates controls from state, using existing if already built."""
        if self._ctrls and all(self._ctrls):
            for i, value in enumerate(self._state):
                self._ctrls[i].Value = value or ""
        else:
            self._ctrls = gui.build(self, self._panel)[0]


    def parse(self, bytes):
        """Builds inventory state from hero bytearray."""
        result = []

        IDS   = metadata.Store.get("ids")
        NAMES = {x[y]: y for x in [IDS]
                 for y in metadata.Store.get("artifacts", category="inventory")}
        MYPOS = plugins.adapt(self, "pos", POS)

        def parse_item(pos):
            b, v = bytes[pos:pos + 4], util.bytoi(bytes[pos:pos + 4])
            if all(x == metadata.Blank for x in b): return None # Blank
            return util.bytoi(bytes[pos:pos + 8]) if v == IDS["Spell Scroll"] else v

        for prop in self.props():
            for i in range(prop["max"]):
                v = parse_item(MYPOS["inventory"] + i*8)
                result.append(NAMES.get(v))
        self._state[:] = result
        self._state0 = copy.deepcopy(result)


    def serialize(self):
        """Returns new hero bytearray, with edited inventory section."""
        result = self._hero.bytes[:]
        bytes0 = self._hero.get_bytes(original=True)

        IDS = metadata.Store.get("ids")
        SCROLL_ARTIFACTS = metadata.Store.get("artifacts", category="scroll")
        MYPOS = plugins.adapt(self, "pos", POS)
        pos = MYPOS["inventory"]

        for prop in self.props():
            for i, name in enumerate(self._state) if "itemlist" == prop["type"] else ():
                v = IDS.get(name)
                if name in SCROLL_ARTIFACTS:
                    b = util.itoby(v, 8)
                elif v:
                    b = util.itoby(v, 4) + metadata.Blank * 4
                elif not self._state0[i]:
                    # Retain original bytes unchanged, as game uses both 0x00 and 0xFF
                    b = bytes0[pos + i * 8:pos + (i + 1) * 8]
                else:
                    b = metadata.Blank * 4 + metadata.Null * 4
                result[pos + i * len(b):pos + (i + 1) * len(b)] = b

        return result
