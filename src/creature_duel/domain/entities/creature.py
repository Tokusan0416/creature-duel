from dataclasses import dataclass, field
from typing import List, Optional

from creature_duel.domain.value_objects.type import Type
from creature_duel.domain.value_objects.stats import Stats, BattleStats
from creature_duel.domain.entities.skill import Skill


@dataclass
class Creature:
    """クリーチャー（ポケモン相当）"""
    name: str
    types: List[Type]  # 1~2個
    base_stats: Stats
    skills: List[Skill]  # 最大4つ
    ability: Optional[str] = None  # 特性名（後で実装）

    battle_stats: BattleStats = field(init=False)
    status_ailment: Optional[str] = None  # 状態異常（後で実装）

    def __post_init__(self):
        """初期化後の処理"""
        self.reset()

    def reset(self):
        """バトル終了後のリセット処理"""
        self.battle_stats = BattleStats(
            current_hp=self.base_stats.hp,
            max_hp=self.base_stats.hp,
            attack=self.base_stats.attack,
            defence=self.base_stats.defence,
            sp_attack=self.base_stats.sp_attack,
            sp_defence=self.base_stats.sp_defence,
            speed=self.base_stats.speed,
        )
        self.status_ailment = None

        # 技のPPリセット
        for skill in self.skills:
            skill.reset_pp()

    def is_fainted(self) -> bool:
        """戦闘不能か"""
        return self.battle_stats.current_hp <= 0

    def take_damage(self, damage: int):
        """ダメージを受ける"""
        self.battle_stats.current_hp = max(0, self.battle_stats.current_hp - damage)

    def heal(self, amount: int):
        """回復する"""
        self.battle_stats.current_hp = min(
            self.battle_stats.max_hp,
            self.battle_stats.current_hp + amount
        )

    def get_hp_percentage(self) -> float:
        """HP残量の割合を取得（0.0 ~ 1.0）"""
        if self.battle_stats.max_hp == 0:
            return 0.0
        return self.battle_stats.current_hp / self.battle_stats.max_hp

    def get_available_skills(self) -> List[Skill]:
        """使用可能な技のリストを取得"""
        return [skill for skill in self.skills if skill.can_use()]
