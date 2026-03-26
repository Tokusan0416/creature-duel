import pytest
from pathlib import Path
from creature_duel.infrastructure.data.loader import MasterDataLoader
from creature_duel.domain.entities.creature import Creature
from creature_duel.domain.entities.skill import Skill
from creature_duel.domain.value_objects.type import Type
from creature_duel.domain.enums.move_category import MoveCategory


@pytest.fixture
def loader():
    """ローダーのフィクスチャ"""
    # デフォルトのデータディレクトリを使用
    return MasterDataLoader()


def test_load_skills(loader):
    """スキル読み込みのテスト"""
    skills = loader.load_skills()

    # スキルが読み込まれているか
    assert len(skills) > 0
    assert "flamethrower" in skills
    assert "thunderbolt" in skills

    # Flamethrowerの詳細チェック
    flamethrower = skills["flamethrower"]
    assert flamethrower.name == "Flamethrower"
    assert flamethrower.type == Type.FIRE
    assert flamethrower.category == MoveCategory.SPECIAL
    assert flamethrower.power == 90
    assert flamethrower.accuracy == 1.0
    assert flamethrower.max_pp == 15


def test_load_creatures(loader):
    """クリーチャー読み込みのテスト"""
    creatures = loader.load_creatures()

    # クリーチャーが読み込まれているか
    assert len(creatures) > 0
    assert "charizard" in creatures
    assert "pikachu" in creatures

    # Charizardの詳細チェック
    charizard = creatures["charizard"]
    assert charizard.name == "Charizard"
    assert Type.FIRE in charizard.types
    assert charizard.base_stats.hp == 150
    assert len(charizard.skills) == 4


def test_load_abilities(loader):
    """アビリティ読み込みのテスト"""
    abilities = loader.load_abilities()

    # アビリティが読み込まれているか
    assert len(abilities) > 0
    assert "blaze" in abilities
    assert "intimidate" in abilities

    # Blazeの詳細チェック
    blaze = abilities["blaze"]
    assert blaze.name == "Blaze"
    assert blaze.trigger.value == "on_attack"
    assert blaze.is_type_boost() is True


def test_load_type_chart(loader):
    """タイプ相性表読み込みのテスト"""
    type_chart = loader.load_type_chart()

    # タイプ相性表が読み込まれているか
    assert "fire" in type_chart
    assert "water" in type_chart

    # Fire vs Waterの相性チェック
    assert type_chart["fire"]["water"] == 0.5
    # Fire vs Grassの相性チェック
    assert type_chart["fire"]["grass"] == 2.0


def test_get_creature(loader):
    """クリーチャー取得のテスト"""
    charizard = loader.get_creature("charizard")
    assert charizard.name == "Charizard"
    assert isinstance(charizard, Creature)


def test_get_creature_not_found(loader):
    """存在しないクリーチャー取得のテスト"""
    with pytest.raises(KeyError):
        loader.get_creature("nonexistent")


def test_get_skill(loader):
    """スキル取得のテスト"""
    flamethrower = loader.get_skill("flamethrower")
    assert flamethrower.name == "Flamethrower"
    assert isinstance(flamethrower, Skill)


def test_get_skill_not_found(loader):
    """存在しないスキル取得のテスト"""
    with pytest.raises(KeyError):
        loader.get_skill("nonexistent")


def test_list_creatures(loader):
    """クリーチャーリスト取得のテスト"""
    creature_ids = loader.list_creatures()
    assert len(creature_ids) > 0
    assert "charizard" in creature_ids
    assert "blastoise" in creature_ids


def test_list_skills(loader):
    """スキルリスト取得のテスト"""
    skill_ids = loader.list_skills()
    assert len(skill_ids) > 0
    assert "flamethrower" in skill_ids
    assert "thunderbolt" in skill_ids


def test_list_abilities(loader):
    """アビリティリスト取得のテスト"""
    ability_ids = loader.list_abilities()
    assert len(ability_ids) > 0
    assert "blaze" in ability_ids
    assert "intimidate" in ability_ids


def test_cache_works(loader):
    """キャッシュが動作するかのテスト"""
    # 1回目の読み込み
    skills1 = loader.load_skills()
    # 2回目の読み込み（キャッシュから）
    skills2 = loader.load_skills()

    # 同じオブジェクトが返されるか
    assert skills1 is skills2
