"""状態異常のタイプ定義"""

from enum import Enum


class AilmentType(Enum):
    """状態異常のタイプ

    各状態異常は固有の効果を持つ：
    - POISON: ターン終了時に最大HPの1/8ダメージ
    - BURN: ターン終了時に最大HPの1/16ダメージ、物理攻撃半減
    - FREEZE: 行動不能、20%で回復
    - SLEEP: 行動不能、1-3ターンで回復
    - PARALYSIS: 素早さ1/4、25%で行動不能
    - CONFUSION: 50%で自分攻撃、1-4ターン継続
    """

    POISON = "poison"
    BURN = "burn"
    FREEZE = "freeze"
    SLEEP = "sleep"
    PARALYSIS = "paralysis"
    CONFUSION = "confusion"
