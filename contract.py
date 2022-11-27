from parse_engine import Parser
from dataclasses import dataclass
import re
import time
import rarity 

@dataclass
class Contract():
    name: str = ""
    rarity: str = ""
    location: str = ""
    client: str = ""
    target: str = ""
    skill: str = ""
    area_level: int = 0
    item_quatity: int = 0
    item_rarity: int = 0
    alert_level_reduction: int = 0
    time_before_lockdown: int = 0
    max_reinforcements: int = 0
    ilvl: int = 0
    mods: list[str] = None
    time: int = 0
    map_start: int = 0
    map_stop: int = 0
    deaths: int = 0

    def html(self, mapsDB):
        mods = []
        if self.mods: mods.extend([f'{mod} {mapsDB.modHtml(mod)}' for mod in self.mods])
        color = rarity.getColor(self.rarity)
        status = 'Not started'
        if self.map_start:
            status = 'Started'
            if self.map_stop:
                status = f'Done in {(self.map_stop - self.map_start)/60.} minutes.'
        return f'''<div>
            <span style="color:{color}"> Lvl. {self.ilvl} {self.skill} - {self.name} </span> 
            {mapsDB.contractLvlHtml(self.ilvl)}
            {''.join([f'<li>{mod}' for mod in mods])}<br/>
            {status}<br>
            {self.deaths} deaths
        </div>
        '''

    def AddFragment(self, _):
        pass

    @staticmethod
    def Parse(lines):
        c = Contract()
        c.mods = []
        c.time = time.localtime()
        rules =[
            [(r'Rarity: (\w+)', 'rarity'),
             (r'Contract: (.*)', 'location'),
             (r'(.*)', 'name'),
            ],
            [(r'Client: (.*)', 'client'),
             (r'Heist Target: (.*)', 'target'),
             (r'Area Level: (.*)', 'area_level'),
             (r'Requires ([^ ]+)', 'skill'),
             (r'Alert Level Reduction: +(\d+)%', 'alert_level_reduction'),
             (r'Time Before Lockdown: +(\d+)%', 'time_before_lockdown'),
             (r'Maximum Alive Reinforcements: +(\d+)%', 'max_reinforcements'),
            ],
            [(r'Item Level: (\d+)', 'ilvl')],
            [(r'([^\d]*)(\d+)(.*)', 'mods'),
             (r'(.*)', 'mods'),
            ],
        ]
        Parser(rules, c, lines)
        return c
    
    def __hash__(self):
        return hash(self.time)