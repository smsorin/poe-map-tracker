from dataclasses import dataclass
from typing import List

@dataclass
class Stats(object):
    runs: int = 0
    deaths: int = 0
    run_sec: List[int] = None

    def update(self, m):
        self.runs += 1
        self.deaths += m.deaths
        if self.run_sec is None:
            self.run_sec = []
        if m.map_start > 0 and m.map_stop > 0:
            self.run_sec.append(m.map_stop - m.map_start)
            
    @property
    def ratio(self):
        return self.deaths/self.runs if self.runs >0 else 0
    
    def html(self, average):
        ratio = self.deaths / float(self.runs) if self.runs else 0
        avg_ratio = average.deaths / average.runs if average.runs else 0
        color = 'black'
        if ratio > 0.1 * avg_ratio:
            color = 'green'
        if ratio > avg_ratio:
            color = '#880'
        if ratio > 2 * avg_ratio:
            color = 'red'
        return f'<span style="color:{color}">{self.deaths / self.runs:.2f}  {self.deaths}/{self.runs}</span>'
