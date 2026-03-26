import pytest
from creature_duel.domain.entities.creature import Creature
from creature_duel.domain.entities.skill import Skill
from creature_duel.domain.value_objects.stats import Stats
from creature_duel.domain.value_objects.status_ailment import StatusAilment
from creature_duel.domain.value_objects.type import Type
from creature_duel.domain.enums.ailment_type import AilmentType
from creature_duel.domain.enums.move_category import MoveCategory


@pytest.fixture
def sample_skill():
    """サンプルの技を作成"""
    return Skill(
        name="Flamethrower",
        type=Type.FIRE,
        category=MoveCategory.SPECIAL,
        power=90,
        accuracy=1.0,
        max_pp=15,
    )


@pytest.fixture
def sample_creature(sample_skill):
    """サンプルのクリーチャーを作成"""
    stats = Stats(
        hp=100,
        attack=80.0,
        defence=70.0,
        sp_attack=110.0,
        sp_defence=80.0,
        speed=90.0,
    )

    return Creature(
        name="Charizard",
        types=[Type.FIRE],
        base_stats=stats,
        skills=[sample_skill],
    )


def test_creature_initialization(sample_creature):
    """クリーチャーの初期化テスト"""
    assert sample_creature.name == "Charizard"
    assert sample_creature.types == [Type.FIRE]
    assert sample_creature.battle_stats.current_hp == 100
    assert sample_creature.battle_stats.max_hp == 100
    assert not sample_creature.is_fainted()


def test_creature_take_damage(sample_creature):
    """ダメージを受けるテスト"""
    sample_creature.take_damage(30)
    assert sample_creature.battle_stats.current_hp == 70
    assert not sample_creature.is_fainted()

    sample_creature.take_damage(80)
    assert sample_creature.battle_stats.current_hp == 0
    assert sample_creature.is_fainted()


def test_creature_heal(sample_creature):
    """回復のテスト"""
    sample_creature.take_damage(50)
    assert sample_creature.battle_stats.current_hp == 50

    sample_creature.heal(30)
    assert sample_creature.battle_stats.current_hp == 80

    # 最大HP以上には回復しない
    sample_creature.heal(50)
    assert sample_creature.battle_stats.current_hp == 100


def test_creature_hp_percentage(sample_creature):
    """HP残量割合のテスト"""
    assert sample_creature.get_hp_percentage() == 1.0

    sample_creature.take_damage(50)
    assert sample_creature.get_hp_percentage() == 0.5

    sample_creature.take_damage(25)
    assert sample_creature.get_hp_percentage() == 0.25


def test_creature_reset(sample_creature):
    """リセット機能のテスト"""
    sample_creature.take_damage(50)
    sample_creature.battle_stats.attack_stage = 2
    sample_creature.skills[0].use()

    assert sample_creature.battle_stats.current_hp == 50
    assert sample_creature.battle_stats.attack_stage == 2
    assert sample_creature.skills[0].current_pp == 14

    sample_creature.reset()

    assert sample_creature.battle_stats.current_hp == 100
    assert sample_creature.battle_stats.attack_stage == 0
    assert sample_creature.skills[0].current_pp == 15


def test_get_available_skills(sample_creature):
    """使用可能な技の取得テスト"""
    available = sample_creature.get_available_skills()
    assert len(available) == 1

    # PPを使い切る
    for _ in range(15):
        sample_creature.skills[0].use()

    available = sample_creature.get_available_skills()
    assert len(available) == 0


def test_apply_status_ailment(sample_creature):
    """状態異常の適用テスト"""
    ailment = StatusAilment(AilmentType.POISON)
    result = sample_creature.apply_status_ailment(ailment)

    assert result is True
    assert sample_creature.has_status_ailment() is True
    assert sample_creature.status_ailment == ailment


def test_apply_status_ailment_already_has_ailment(sample_creature):
    """既に状態異常がある場合のテスト"""
    ailment1 = StatusAilment(AilmentType.POISON)
    ailment2 = StatusAilment(AilmentType.BURN)

    sample_creature.apply_status_ailment(ailment1)
    result = sample_creature.apply_status_ailment(ailment2)

    assert result is False
    assert sample_creature.status_ailment == ailment1


def test_clear_status_ailment(sample_creature):
    """状態異常の解除テスト"""
    ailment = StatusAilment(AilmentType.POISON)
    sample_creature.apply_status_ailment(ailment)

    assert sample_creature.has_status_ailment() is True

    sample_creature.clear_status_ailment()

    assert sample_creature.has_status_ailment() is False
    assert sample_creature.status_ailment is None


def test_process_status_ailment_turn_end_poison(sample_creature):
    """毒状態のターン終了時処理テスト"""
    ailment = StatusAilment(AilmentType.POISON)
    sample_creature.apply_status_ailment(ailment)

    # ターン終了時処理
    damage = sample_creature.process_status_ailment_turn_end()

    # 最大HPの1/8のダメージ（100 * 0.125 = 12.5 → 12）
    assert damage == 12
    assert sample_creature.battle_stats.current_hp == 88


def test_process_status_ailment_turn_end_burn(sample_creature):
    """火傷状態のターン終了時処理テスト"""
    ailment = StatusAilment(AilmentType.BURN)
    sample_creature.apply_status_ailment(ailment)

    damage = sample_creature.process_status_ailment_turn_end()

    # 最大HPの1/16のダメージ（100 * 0.0625 = 6.25 → 6）
    assert damage == 6
    assert sample_creature.battle_stats.current_hp == 94


def test_process_status_ailment_turn_end_with_duration(sample_creature):
    """ターン制限付き状態異常のテスト"""
    ailment = StatusAilment(AilmentType.SLEEP, turns_remaining=2)
    sample_creature.apply_status_ailment(ailment)

    # 1ターン目（ダメージなし、継続）
    damage1 = sample_creature.process_status_ailment_turn_end()
    assert damage1 == 0
    assert sample_creature.has_status_ailment() is True
    assert sample_creature.status_ailment is not None
    assert sample_creature.status_ailment.turns_remaining == 1

    # 2ターン目（解除）
    damage2 = sample_creature.process_status_ailment_turn_end()
    assert damage2 == 0
    assert sample_creature.has_status_ailment() is False
