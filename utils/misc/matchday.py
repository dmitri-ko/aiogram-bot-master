from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from aiogram.utils.markdown import hbold

@dataclass
class Match:
    home_team: str
    away_team: str
    home_goals: int
    away_goals: int
    date: datetime = datetime.today() 
    scores: str = None
    schedule: str =None
    
    def __post_init__(self):
        self.scores = f"{self.home_team} - {self.away_team}" + \
                " " + hbold(f"{self.home_goals} - {self.away_goals}") + "\n"
        self.schedule  = hbold(f"{self.date.strftime('%H:%M')}") + \
                f" {self.home_team} - {self.away_team}\n"     
    
@dataclass
class MatchDay:
    games: List[Match]

@dataclass
class Fixtures:
    matchdays: Dict[str, MatchDay]