"""
Creature Duel - Pokemon-like battle simulation system

ポケモンに似た対戦バトルシミュレーションシステム
バトルログをJSON形式で出力し、BigQueryに格納して分析・機械学習に活用
"""

__version__ = "0.1.0"

# Domain entities
from creature_duel.domain.entities.creature import Creature
from creature_duel.domain.entities.skill import Skill

# Domain value objects
from creature_duel.domain.value_objects.stats import Stats, BattleStats
from creature_duel.domain.value_objects.type import Type

# Domain enums
from creature_duel.domain.enums.move_category import MoveCategory

# Battle engine
from creature_duel.battle.battle_engine import BattleEngine
from creature_duel.battle.battle_state import BattleState

__all__ = [
    # Version
    "__version__",
    # Entities
    "Creature",
    "Skill",
    # Value Objects
    "Stats",
    "BattleStats",
    "Type",
    # Enums
    "MoveCategory",
    # Battle
    "BattleEngine",
    "BattleState",
]
