"""StatModifierServiceのテスト"""

from creature_duel.application.services.stat_modifier_service import (
    StatModifierService,
)
from creature_duel.domain.entities.creature import Creature
from creature_duel.domain.entities.skill import Skill
from creature_duel.domain.value_objects.stats import Stats, BattleStats
from creature_duel.domain.value_objects.status_ailment import StatusAilment
from creature_duel.domain.value_objects.type import Type
from creature_duel.domain.enums.ailment_type import AilmentType
from creature_duel.domain.enums.move_category import MoveCategory


def test_modify_stat_stage():
    """能力ランク変更のテスト"""
    battle_stats = BattleStats(
        current_hp=100,
        max_hp=100,
        attack=80.0,
        defence=70.0,
        sp_attack=60.0,
        sp_defence=60.0,
        speed=70.0,
    )

    service = StatModifierService()

    # +2段階上昇
    change = service.modify_stat_stage(battle_stats, "attack", 2)
    assert change == 2
    assert battle_stats.attack_stage == 2

    # さらに+1段階上昇
    change = service.modify_stat_stage(battle_stats, "attack", 1)
    assert change == 1
    assert battle_stats.attack_stage == 3


def test_modify_stat_stage_limits():
    """能力ランクの上限・下限テスト"""
    battle_stats = BattleStats(
        current_hp=100,
        max_hp=100,
        attack=80.0,
        defence=70.0,
        sp_attack=60.0,
        sp_defence=60.0,
        speed=70.0,
    )

    service = StatModifierService()

    # +6まで上昇
    service.modify_stat_stage(battle_stats, "attack", 6)
    assert battle_stats.attack_stage == 6

    # さらに上げようとしても上限
    change = service.modify_stat_stage(battle_stats, "attack", 2)
    assert change == 0
    assert battle_stats.attack_stage == 6

    # -6まで下降
    service.modify_stat_stage(battle_stats, "defence", -6)
    assert battle_stats.defence_stage == -6

    # さらに下げようとしても下限
    change = service.modify_stat_stage(battle_stats, "defence", -2)
    assert change == 0
    assert battle_stats.defence_stage == -6


def test_get_hp_boost_multiplier_full():
    """HP満タン時の補正テスト"""
    skill = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    stats = Stats(
        hp=100, attack=80.0, defence=70.0, sp_attack=60.0, sp_defence=60.0, speed=70.0
    )
    creature = Creature(name="Test", types=[Type.NORMAL], base_stats=stats, skills=[skill])

    service = StatModifierService()
    multiplier = service.get_hp_boost_multiplier(creature)

    assert multiplier == 1.0


def test_get_hp_boost_multiplier_half():
    """HP 50%以下の補正テスト"""
    skill = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    stats = Stats(
        hp=100, attack=80.0, defence=70.0, sp_attack=60.0, sp_defence=60.0, speed=70.0
    )
    creature = Creature(name="Test", types=[Type.NORMAL], base_stats=stats, skills=[skill])

    # HP を50%にする
    creature.take_damage(50)

    service = StatModifierService()
    multiplier = service.get_hp_boost_multiplier(creature)

    assert multiplier == 1.25


def test_get_hp_boost_multiplier_quarter():
    """HP 25%以下の補正テスト"""
    skill = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    stats = Stats(
        hp=100, attack=80.0, defence=70.0, sp_attack=60.0, sp_defence=60.0, speed=70.0
    )
    creature = Creature(name="Test", types=[Type.NORMAL], base_stats=stats, skills=[skill])

    # HP を25%にする
    creature.take_damage(75)

    service = StatModifierService()
    multiplier = service.get_hp_boost_multiplier(creature)

    assert multiplier == 1.5


def test_apply_status_ailment_modifiers_burn():
    """火傷状態の攻撃力補正テスト"""
    skill = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    stats = Stats(
        hp=100, attack=80.0, defence=70.0, sp_attack=60.0, sp_defence=60.0, speed=70.0
    )
    creature = Creature(name="Test", types=[Type.NORMAL], base_stats=stats, skills=[skill])

    # 火傷状態を適用
    ailment = StatusAilment(AilmentType.BURN)
    creature.apply_status_ailment(ailment)

    service = StatModifierService()
    modified_attack = service.apply_status_ailment_modifiers(creature, 80.0)

    # 火傷で攻撃力半減
    assert modified_attack == 40.0


def test_apply_status_ailment_modifiers_no_ailment():
    """状態異常なしの補正テスト"""
    skill = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    stats = Stats(
        hp=100, attack=80.0, defence=70.0, sp_attack=60.0, sp_defence=60.0, speed=70.0
    )
    creature = Creature(name="Test", types=[Type.NORMAL], base_stats=stats, skills=[skill])

    service = StatModifierService()
    modified_attack = service.apply_status_ailment_modifiers(creature, 80.0)

    # 状態異常なしなので変化なし
    assert modified_attack == 80.0


def test_get_effective_speed_normal():
    """通常時の実効素早さテスト"""
    skill = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    stats = Stats(
        hp=100, attack=80.0, defence=70.0, sp_attack=60.0, sp_defence=60.0, speed=100.0
    )
    creature = Creature(name="Test", types=[Type.NORMAL], base_stats=stats, skills=[skill])

    service = StatModifierService()
    speed = service.get_effective_speed(creature)

    assert speed == 100.0


def test_get_effective_speed_with_stage():
    """能力ランク補正付きの実効素早さテスト"""
    skill = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    stats = Stats(
        hp=100, attack=80.0, defence=70.0, sp_attack=60.0, sp_defence=60.0, speed=100.0
    )
    creature = Creature(name="Test", types=[Type.NORMAL], base_stats=stats, skills=[skill])

    # 素早さランク+2
    creature.battle_stats.speed_stage = 2

    service = StatModifierService()
    speed = service.get_effective_speed(creature)

    # +2段階 = 2.0倍
    assert speed == 200.0


def test_get_effective_speed_paralysis():
    """麻痺状態の実効素早さテスト"""
    skill = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    stats = Stats(
        hp=100, attack=80.0, defence=70.0, sp_attack=60.0, sp_defence=60.0, speed=100.0
    )
    creature = Creature(name="Test", types=[Type.NORMAL], base_stats=stats, skills=[skill])

    # 麻痺状態を適用
    ailment = StatusAilment(AilmentType.PARALYSIS)
    creature.apply_status_ailment(ailment)

    service = StatModifierService()
    speed = service.get_effective_speed(creature)

    # 麻痺で1/4
    assert speed == 25.0


def test_reset_stat_stages():
    """能力ランクリセットのテスト"""
    battle_stats = BattleStats(
        current_hp=100,
        max_hp=100,
        attack=80.0,
        defence=70.0,
        sp_attack=60.0,
        sp_defence=60.0,
        speed=70.0,
        attack_stage=2,
        defence_stage=-1,
        sp_attack_stage=3,
        speed_stage=-2,
    )

    service = StatModifierService()
    service.reset_stat_stages(battle_stats)

    assert battle_stats.attack_stage == 0
    assert battle_stats.defence_stage == 0
    assert battle_stats.sp_attack_stage == 0
    assert battle_stats.sp_defence_stage == 0
    assert battle_stats.speed_stage == 0
    assert battle_stats.evasion_stage == 0
    assert battle_stats.accuracy_stage == 0
