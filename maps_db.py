from operator import truediv
from os import stat
import pickle
from re import I
import time

import stats
from map import Map
from contract import Contract


class MapsDB():
    def __init__(self, db_file):
        self._all_maps = []
        self._tiers = {}
        self._mods = {}
        self._fragments = {}
        self._total = stats.Stats()
        self._db_file = db_file
        self._contract_levels = {}
        self._contract_total = stats.Stats()

    def Load(self):
        with open(self._db_file, 'rb') as pf:
            try:
                while True:
                    self.add(pickle.load(pf))
            except EOFError:
                pass
        print(f'Loaded {len(self._all_maps)} maps.')
    
    def Save(self, map):
        self.add(map)
        with open(self._db_file, 'ab+') as pf:
            pickle.dump(map, pf)
        
    @staticmethod
    def formatMod(mod):
        if ',' not in mod: return mod
        return mod.split(',')[0]
    
    def tierHtml(self, tier):
        if tier not in self._tiers:
            return ""
        return self._tiers[tier].html(self._total)

    def contractLvlHtml(self, ilvl):
        if ilvl not in self._contract_levels:
            return ""
        return self._contract_levels[ilvl].html(self._contract_total)
        
    def modHtml(self, mod):
        mod = self.formatMod(mod)
        if mod not in self._mods:
            return ""
        return self._mods[mod].html(self._total)
        
    def fragmentHtml(self, fragment):
        if fragment not in self._fragments:
            return ""
        return self._fragments[fragment].html(self._total)
    
    def add(self, m):
        self._total.update(m)
        for mod in m.mods:
            mod_name = self.formatMod(mod)            
            if mod_name not in self._mods:
                self._mods[mod_name] = stats.Stats()
            self._mods[mod_name].update(m)
        self._all_maps.append(m)

        if isinstance(m, Contract):            
            self._contract_total.update(m)
            if m.ilvl not in self._contract_levels:
                self._contract_levels[m.ilvl] = stats.Stats()
            self._contract_levels[m.ilvl].update(m)

        if isinstance(m, Map):
            
        
            if m.tier not in self._tiers:
                self._tiers[m.tier] = stats.Stats()
            self._tiers[m.tier].update(m)
            if m.fragments:
                for f in m.fragments:
                    if f not in self._fragments:
                        self._fragments[f] = stats.Stats()
                    self._fragments[f].update(m)

    def remove(self, map_id):
        print(map_id)
        map_id = int(map_id)
        for m in self._all_maps:
            print(hash(m), '  ', map_id)
            if hash(m) == map_id:
                self._all_maps.remove(m)
                return True
        return False

    def GetMapsContext(self):
        r = []
        for m in self._all_maps[::-1]:
            if isinstance(m, Map):
                name = f'{m.rarity} T{m.tier} {m.name}'
            if isinstance(m, Contract):
                name = f'{m.ilvl} {m.skill} - {m.name}'
                
            r.append({
                'date': time.strftime("%b %d %a; %H:%M:%S", m.time),
                'name': name,
                'duration': ("%0.2f" % ((m.map_stop - m.map_start)/60.)) if m.map_stop and m.map_start else "invalid",
                'deaths': m.deaths,
                'id': f"{hash(m)}",
            })
        return r