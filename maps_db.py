import pickle

import stats
from map import Map

class MapsDB():
    def __init__(self, db_file):
        self._all_maps = []
        self._tiers = {}
        self._mods = {}
        self._fragments = {}
        self._total = stats.Stats()
        self._db_file = db_file

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
        self._all_maps.append(m)
        self._total.update(m)
        if m.tier not in self._tiers:
            self._tiers[m.tier] = stats.Stats()
        self._tiers[m.tier].update(m)
        for mod in m.mods:
            mod_name = self.formatMod(mod)            
            if mod_name not in self._mods:
                self._mods[mod_name] = stats.Stats()
            self._mods[mod_name].update(m)
        if m.fragments:
            for f in m.fragments:
                if f not in self._fragments:
                    self._fragments[f] = stats.Stats()
                self._fragments[f].update(m)
