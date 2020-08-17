from dataclasses import dataclass
from typing import List

@dataclass
class Match:
    home_team: str
    away_team: str
    home_goals: int
    away_goals: int
    
@dataclass
class MatchDay:
    games: List[Match]
