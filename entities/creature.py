from dataclasses import dataclass, field
from typing import List
from value_objects.type import Type
from value_objects.stats import Stats, BattleStats
from entities.skill import Skill

@dataclass
class Creature:
    name: str
    types: List[Type]
    base_stats: Stats
    skills: List[Skill]

    battle_stats: BattleStats = field(init=False)

    def __post_init__(self):
        self.reset()

    def reset(self):
        self.battle_stats = BattleStats(
            current_hp=self.base_stats.hp,
            attack=self.base_stats.attack,
            defence=self.base_stats.defence,
            sp_attack=self.base_stats.sp_attack,
            sp_defence=self.base_stats.sp_defence,
            speed=self.base_stats.speed,
        )

    def is_fainted(self):
        return self.battle_stats.current_hp <= 0