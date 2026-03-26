"""Playerのテスト"""

import pytest
from creature_duel.domain.entities.player import Player
from creature_duel.domain.entities.creature import Creature
from creature_duel.domain.entities.skill import Skill
from creature_duel.domain.value_objects.stats import Stats
from creature_duel.domain.value_objects.type import Type
from creature_duel.domain.enums.move_category import MoveCategory


@pytest.fixture
def sample_skill():
    """サンプルの技を作成"""
    return Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )


@pytest.fixture
def sample_creatures(sample_skill):
    """サンプルのCreatureリストを作成（3体）"""
    creatures = []
    for i in range(3):
        stats = Stats(
            hp=100,
            attack=80.0,
            defence=70.0,
            sp_attack=60.0,
            sp_defence=60.0,
            speed=70.0,
        )
        creature = Creature(
            name=f"Creature{i+1}",
            types=[Type.NORMAL],
            base_stats=stats,
            skills=[sample_skill],
        )
        creatures.append(creature)
    return creatures


def test_player_initialization(sample_creatures):
    """Playerの初期化テスト"""
    player = Player(name="Ash", creatures=sample_creatures)

    assert player.name == "Ash"
    assert len(player.creatures) == 3
    assert player.current_creature_index == 0


def test_player_empty_creatures():
    """空のCreatureリストでの初期化失敗テスト"""
    with pytest.raises(ValueError, match="Creatures list cannot be empty"):
        Player(name="Ash", creatures=[])


def test_player_too_many_creatures(sample_creatures):
    """7体以上のCreatureでの初期化失敗テスト"""
    too_many = sample_creatures * 3  # 9体
    with pytest.raises(ValueError, match="Cannot have more than 6 creatures"):
        Player(name="Ash", creatures=too_many)


def test_get_current_creature(sample_creatures):
    """現在のCreature取得テスト"""
    player = Player(name="Ash", creatures=sample_creatures)

    current = player.get_current_creature()
    assert current == sample_creatures[0]
    assert current.name == "Creature1"


def test_switch_creature(sample_creatures):
    """Creature切り替えテスト"""
    player = Player(name="Ash", creatures=sample_creatures)

    # Creature2に切り替え
    result = player.switch_creature(1)
    assert result is True
    assert player.current_creature_index == 1
    assert player.get_current_creature().name == "Creature2"

    # Creature3に切り替え
    result = player.switch_creature(2)
    assert result is True
    assert player.current_creature_index == 2


def test_switch_creature_same_index(sample_creatures):
    """同じCreatureへの切り替え失敗テスト"""
    player = Player(name="Ash", creatures=sample_creatures)

    result = player.switch_creature(0)
    assert result is False
    assert player.current_creature_index == 0


def test_switch_creature_invalid_index(sample_creatures):
    """無効なインデックスでの切り替え失敗テスト"""
    player = Player(name="Ash", creatures=sample_creatures)

    # 負の値
    result = player.switch_creature(-1)
    assert result is False

    # 範囲外
    result = player.switch_creature(10)
    assert result is False

    assert player.current_creature_index == 0


def test_switch_creature_to_fainted(sample_creatures):
    """倒れているCreatureへの切り替え失敗テスト"""
    player = Player(name="Ash", creatures=sample_creatures)

    # Creature2を倒す
    sample_creatures[1].take_damage(1000)
    assert sample_creatures[1].is_fainted()

    # 倒れているCreatureに切り替えできない
    result = player.switch_creature(1)
    assert result is False
    assert player.current_creature_index == 0


def test_has_available_creatures(sample_creatures):
    """使用可能なCreature判定テスト"""
    player = Player(name="Ash", creatures=sample_creatures)

    assert player.has_available_creatures() is True

    # 全て倒す
    for creature in sample_creatures:
        creature.take_damage(1000)

    assert player.has_available_creatures() is False


def test_get_available_creatures(sample_creatures):
    """使用可能なCreatureリスト取得テスト"""
    player = Player(name="Ash", creatures=sample_creatures)

    available = player.get_available_creatures()
    assert len(available) == 3

    # 1体倒す
    sample_creatures[1].take_damage(1000)

    available = player.get_available_creatures()
    assert len(available) == 2
    assert sample_creatures[1] not in available


def test_get_fainted_count(sample_creatures):
    """倒れているCreature数の取得テスト"""
    player = Player(name="Ash", creatures=sample_creatures)

    assert player.get_fainted_count() == 0

    # 1体倒す
    sample_creatures[0].take_damage(1000)
    assert player.get_fainted_count() == 1

    # 2体目も倒す
    sample_creatures[1].take_damage(1000)
    assert player.get_fainted_count() == 2


def test_is_defeated(sample_creatures):
    """全滅判定テスト"""
    player = Player(name="Ash", creatures=sample_creatures)

    assert player.is_defeated() is False

    # 全て倒す
    for creature in sample_creatures:
        creature.take_damage(1000)

    assert player.is_defeated() is True


def test_reset_all_creatures(sample_creatures):
    """全Creatureリセットテスト"""
    player = Player(name="Ash", creatures=sample_creatures)

    # ダメージを与える
    sample_creatures[0].take_damage(50)
    sample_creatures[1].take_damage(1000)  # 倒す

    # Creatureを切り替える
    player.switch_creature(2)

    assert sample_creatures[0].battle_stats.current_hp == 50
    assert sample_creatures[1].is_fainted()
    assert player.current_creature_index == 2

    # リセット
    player.reset_all_creatures()

    assert sample_creatures[0].battle_stats.current_hp == 100
    assert sample_creatures[1].is_fainted() is False
    assert player.current_creature_index == 0
