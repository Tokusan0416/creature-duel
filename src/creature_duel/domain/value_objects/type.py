from enum import Enum
from typing import List


class Type(Enum):
    """ポケモンのタイプ（簡易版6タイプ）"""
    NORMAL = "normal"
    FIRE = "fire"
    WATER = "water"
    GRASS = "grass"
    ELECTRIC = "electric"
    ICE = "ice"


# タイプ相性表（攻撃側タイプ、防御側タイプ）→ 倍率
TYPE_EFFECTIVENESS = {
    # ほのお
    (Type.FIRE, Type.GRASS): 2.0,
    (Type.FIRE, Type.WATER): 0.5,
    (Type.FIRE, Type.ICE): 2.0,
    (Type.FIRE, Type.FIRE): 0.5,
    # みず
    (Type.WATER, Type.FIRE): 2.0,
    (Type.WATER, Type.GRASS): 0.5,
    (Type.WATER, Type.WATER): 0.5,
    # くさ
    (Type.GRASS, Type.FIRE): 0.5,
    (Type.GRASS, Type.WATER): 2.0,
    (Type.GRASS, Type.GRASS): 0.5,
    # でんき
    (Type.ELECTRIC, Type.WATER): 2.0,
    (Type.ELECTRIC, Type.GRASS): 0.5,
    (Type.ELECTRIC, Type.ELECTRIC): 0.5,
    # こおり
    (Type.ICE, Type.GRASS): 2.0,
    (Type.ICE, Type.FIRE): 0.5,
    (Type.ICE, Type.WATER): 0.5,
    (Type.ICE, Type.ICE): 0.5,
}


def get_type_multiplier(attack_type: Type, defender_types: List[Type]) -> float:
    """
    タイプ相性による倍率を計算する

    Args:
        attack_type: 攻撃技のタイプ
        defender_types: 防御側のタイプリスト（1~2個）

    Returns:
        ダメージ倍率（0.25, 0.5, 1.0, 2.0, 4.0のいずれか）

    Notes:
        - 2タイプ持ちの場合、両方のタイプ相性を掛け合わせる
        - 例：ほのお技 vs みず/くさ → 0.5 * 2.0 = 1.0倍
    """
    multiplier = 1.0
    for defender_type in defender_types:
        multiplier *= TYPE_EFFECTIVENESS.get((attack_type, defender_type), 1.0)

    return multiplier
