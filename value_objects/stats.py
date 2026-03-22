from dataclasses import dataclass

@dataclass
class Stats:
    hp: int
    attack: float
    defence: float
    sp_attack: float
    sp_defence: float
    speed: float

@dataclass
class BattleStats:
    current_hp: int
    attack: float
    defence: float
    sp_attack: float
    sp_defence: float
    speed: float