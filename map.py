from dataclasses import dataclass
import re
import time
import rarity

@dataclass(eq=True)
class Map():
    rarity: str = None
    name: str = None
    tier: int = 0
    quantity: int = 0
    item_rarity: int = 0
    pack_size: int = 0
    quality: int = 0
    ilvl: int = 0
    mods: list[str] = None
    fragments: list[str] = None
    time: int = 0
    map_start: int = 0
    map_stop: int = 0
    deaths: int = 0

    def __init__(self) -> None:
        self.mods = []

    def html(self, mapsDB):
        mods = []       
        if self.mods: mods.extend([f'{mod} {mapsDB.modHtml(mod)}' for mod in self.mods])
        if self.fragments: mods.extend([f'{f} {mapsDB.fragmentHtml(f)}' for f in self.fragments])
        color = rarity.getColor(self.rarity)        
        status = 'Not Started'
        if self.map_start:
            status = 'Started'
            if self.map_stop:
                status = f'Done in {(self.map_stop - self.map_start) / 60.0} minutes'
        return f'''<div>
            <span style="color:{color}">{self.quality}% T{self.tier} {self.name}
            </span> {mapsDB.tierHtml(self.tier)}
            {''.join([f'<li>{mod}' for mod in mods])}<br>
            {status}<br>
            {self.deaths} deaths
        </div>
        '''

    def AddFragment(self, f):
        if not self.fragments:
            self.fragments = [f.name]
        else:
            self.fragments.append(f.name)        

    @staticmethod
    def Parse(lines):
        l = 1
        m = Map()
        m.time = time.localtime()
        # Header
        while l<len(lines):
            if lines[l] == '--------':
                l+=1
                break
            result = re.match(r'Rarity: (\w+)', lines[l])
            if result:
                m.rarity = result.group(1)
            else:
                m.name = lines[l]
            l+=1
        for line in lines[l:]:
            if line == '--------': continue                
            result = re.match(r'Map Tier: (\d+)', line)
            if result:
                m.tier = int(result.group(1))
                continue
            result = re.match(r'Item Quantity: \+(\d+)%', line)
            if result:
                m.quantity = int(result.group(1))
                continue
            result = re.match(r'Item Rarity: \+(\d+)%', line)
            if result:
                m.item_rarity = int(result.group(1))
                continue
            result = re.match(r'Monster Pack Size: \+(\d+)%', line)
            if result:
                m.pack_size = int(result.group(1))
                continue
            result = re.match(r'Quality: \+(\d+)%', line)
            if result:
                m.quality = int(result.group(1))
                continue
            result = re.match(r'Item Level: (\d+)', line)
            if result:
                m.ilvl = int(result.group(1))
                continue
            result = re.fullmatch(r'([^\d]*)(\d+)([^\d]*)', line)
            if result: line = result.group(1) + '#'+result.group(3) + ', ' + result.group(2)
            if m.mods is None: m.mods = []
            if line: m.mods.append(line)
            
        return m

    def __hash__(self):
        return hash(self.time)