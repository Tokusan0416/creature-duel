import random
from typing import Optional

from creature_duel.domain.entities.creature import Creature
from creature_duel.domain.entities.skill import Skill
from creature_duel.domain.entities.ability import Ability
from creature_duel.domain.enums.move_category import MoveCategory
from creature_duel.application.services.type_effectiveness import TypeEffectivenessService
from creature_duel.application.services.stat_modifier_service import StatModifierService
from creature_duel.infrastructure.data.loader import MasterDataLoader

# サービス（モジュールレベルでシングルトン的に使用）
_type_service = TypeEffectivenessService()
_stat_modifier_service = StatModifierService()
_loader = MasterDataLoader()


def _get_ability_boost(attacker: Creature, skill: Skill) -> float:
    """Abilityによるダメージ補正を計算

    Args:
        attacker: 攻撃側のクリーチャー
        skill: 使用する技

    Returns:
        補正倍率（通常は1.0、補正があれば1.5等）

    Notes:
        - もうか/げきりゅう/しんりょく: HP 1/3以下で特定タイプの技威力1.5倍
    """
    if attacker.ability is None:
        return 1.0

    # Abilityを読み込み
    try:
        ability: Ability = _loader.get_ability(attacker.ability)
    except KeyError:
        return 1.0

    # タイプ強化特性の場合
    if ability.is_type_boost():
        config = ability.effect_config

        # HP閾値チェック
        hp_threshold = config.get("hp_threshold", 0.0)
        if attacker.get_hp_percentage() > hp_threshold:
            return 1.0

        # タイプチェック
        boosted_type = config.get("boosted_type", "")
        if skill.type.value != boosted_type:
            return 1.0

        # 補正倍率を返す
        return config.get("multiplier", 1.0)

    return 1.0


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
        base_damage = (攻撃力 * 技威力 / 防御力) * 能力ランク補正 * 状態異常補正
        type_effectiveness = タイプ相性倍率
        stab = タイプ一致ボーナス（1タイプ: 1.5倍, 2タイプ: 1.25倍）
        hp_boost = HP依存の補正（50%以下: 1.25倍, 25%以下: 1.5倍）
        ability_boost = Ability補正（もうか等: 1.5倍）
        critical = クリティカルヒット（2.0倍）

        最終ダメージ = base_damage * type_effectiveness * stab * hp_boost * ability_boost * critical

    処理フロー:
        1. 攻撃力・防御力を取得（能力ランク補正込み）
        2. 物理攻撃の場合、状態異常補正を適用（火傷で半減）
        3. 基本ダメージを計算
        4. タイプ相性を取得
        5. STAB補正を計算
        6. HP依存補正を計算
        7. Ability補正を計算（もうか、げきりゅう、しんりょく等）
        8. クリティカルヒット判定
        9. 最終ダメージを計算して返す
    """
    if skill.category == MoveCategory.STATUS:
        return 0

    # 攻撃力と防御力を取得（能力ランク補正込み）
    if skill.category == MoveCategory.PHYSICAL:
        attack = attacker.battle_stats.attack * attacker.battle_stats.get_attack_multiplier()
        # 状態異常補正（火傷で物理攻撃半減）
        attack = _stat_modifier_service.apply_status_ailment_modifiers(attacker, attack)
        defence = defender.battle_stats.defence * defender.battle_stats.get_defence_multiplier()
    else:  # SPECIAL
        attack = attacker.battle_stats.sp_attack * attacker.battle_stats.get_sp_attack_multiplier()
        defence = defender.battle_stats.sp_defence * defender.battle_stats.get_sp_defence_multiplier()

    # 基本ダメージ
    base_damage = attack * skill.power / defence

    # タイプ相性
    type_effectiveness = _type_service.get_type_multiplier(skill.type, defender.types)

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

    # Ability補正（もうか、げきりゅう、しんりょく等）
    ability_boost = _get_ability_boost(attacker, skill)

    # クリティカルヒット判定
    critical = 2.0 if random.random() < attacker.battle_stats.critical_rate else 1.0

    # 最終ダメージ
    final_damage = (
        base_damage * type_effectiveness * stab * hp_boost * ability_boost * critical
    )

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
