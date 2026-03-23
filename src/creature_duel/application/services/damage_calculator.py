import random
from creature_duel.domain.entities.creature import Creature
from creature_duel.domain.entities.skill import Skill
from creature_duel.domain.enums.move_category import MoveCategory
from creature_duel.domain.value_objects.type import get_type_multiplier


def calculate_damage(attacker: Creature, defender: Creature, skill: Skill) -> int:
    """
    ダメージを計算する

    Args:
        attacker: 攻撃側のクリーチャー
        defender: 防御側のクリーチャー
        skill: 使用する技

    Returns:
        ダメージ量（整数）

    Notes:
        計算式：
        base_damage = (攻撃力 * 技威力 / 防御力) * 能力ランク補正
        type_effectiveness = タイプ相性倍率
        stab = タイプ一致ボーナス（1タイプ: 1.5倍, 2タイプ: 1.25倍）
        hp_boost = HP依存の補正（50%以下: 1.25倍, 25%以下: 1.5倍）
        critical = クリティカルヒット（2.0倍）

        最終ダメージ = base_damage * type_effectiveness * stab * hp_boost * critical
    """
    if skill.category == MoveCategory.STATUS:
        return 0

    # 攻撃力と防御力を取得（能力ランク補正込み）
    if skill.category == MoveCategory.PHYSICAL:
        attack = attacker.battle_stats.attack * attacker.battle_stats.get_attack_multiplier()
        defence = defender.battle_stats.defence * defender.battle_stats.get_defence_multiplier()
    else:  # SPECIAL
        attack = attacker.battle_stats.sp_attack * attacker.battle_stats.get_sp_attack_multiplier()
        defence = defender.battle_stats.sp_defence * defender.battle_stats.get_sp_defence_multiplier()

    # 基本ダメージ
    base_damage = attack * skill.power / defence

    # タイプ相性
    type_effectiveness = get_type_multiplier(skill.type, defender.types)

    # タイプ一致ボーナス (STAB: Same Type Attack Bonus)
    stab = 1.0
    if skill.type in attacker.types:
        if len(attacker.types) == 1:
            stab = 1.5
        else:
            stab = 1.25

    # HP依存の補正
    hp_percentage = attacker.get_hp_percentage()
    if hp_percentage <= 0.25:
        hp_boost = 1.5
    elif hp_percentage <= 0.5:
        hp_boost = 1.25
    else:
        hp_boost = 1.0

    # クリティカルヒット判定
    critical = 2.0 if random.random() < attacker.battle_stats.critical_rate else 1.0

    # 最終ダメージ
    final_damage = base_damage * type_effectiveness * stab * hp_boost * critical

    return int(final_damage)


def check_critical_hit(creature: Creature) -> bool:
    """
    クリティカルヒットが発生するかチェック

    Args:
        creature: 攻撃側のクリーチャー

    Returns:
        クリティカルヒットが発生する場合True
    """
    return random.random() < creature.battle_stats.critical_rate
