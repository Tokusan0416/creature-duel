import pytest
from creature_duel.domain.entities.creature import Creature
from creature_duel.domain.entities.skill import Skill
from creature_duel.domain.value_objects.stats import Stats
from creature_duel.domain.value_objects.type import Type
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
