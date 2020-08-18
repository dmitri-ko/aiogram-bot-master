from dataclasses import dataclass
from typing import List

@dataclass
class Position():
    position: int
    team: str
    games: int
    won: int
    draw: int
    lost: int
    goals_for: int
    goals_against: int
    points: int
    zone: str

@dataclass
class Standings():
    last_updated: str
    table: List[Position]