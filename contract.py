from parse_engine import Parser
from dataclasses import dataclass
import re
import time

@dataclass
class Contract():
    name: str = ""
    rarity: str = ""
    location: str = ""
    client: str = ""
    target: str = ""
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
        # TODO: Fix This
        return ""

    @staticmethod
    def Parse(lines):
        c = Contract()
        c.time = time.localtime()
        rules =[
            [(r'Rarity: (\w+)', 'rarity'),
             (r'Contract: (.*)', 'location'),
             (r'(.*)', 'name'),
            ],
            [(r'Client: (.*)', 'client'),
             (r'Heist Target: (.*)', 'target'),
             (r'Area Level: (.*)', 'area_level'),
             (r'Alert Level Reduction: +(\d+)%', 'alert_level_reduction'),
             (r'Time Before Lockdown: +(\d+)%', 'time_before_lockdown'),
             (r'Maximum Alive Reinforcements: +(\d+)%', 'max_reinforcements'),
            ],
            [(r'Item Level: (\d+)', 'ilvl')],
            [(r'([^\d]*)(\d+)([^\d]*)', 'mods')],
        ]
        Parser(rules, c, lines)
        return c