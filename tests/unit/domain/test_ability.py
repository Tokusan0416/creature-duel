"""Abilityのテスト"""

from creature_duel.domain.entities.ability import Ability, AbilityTrigger


def test_ability_from_dict_type_boost():
    """タイプ強化特性の作成テスト"""
    data = {
        "id": "blaze",
        "name": "Blaze",
        "description": "HP 1/3以下で炎タイプの技威力1.5倍",
        "trigger": "on_attack",
        "effect_config": {
            "type": "type_boost",
            "boosted_type": "fire",
            "multiplier": 1.5,
            "hp_threshold": 0.33,
        },
    }

    ability = Ability.from_dict(data)

    assert ability.id == "blaze"
    assert ability.name == "Blaze"
    assert ability.trigger == AbilityTrigger.ON_ATTACK
    assert ability.effect_config["type"] == "type_boost"
    assert ability.effect_config["boosted_type"] == "fire"
    assert ability.effect_config["multiplier"] == 1.5


def test_ability_from_dict_stat_change():
    """能力変化特性の作成テスト"""
    data = {
        "id": "intimidate",
        "name": "Intimidate",
        "description": "場に出た時、相手のAttackを1段階下げる",
        "trigger": "on_switch_in",
        "effect_config": {
            "type": "stat_change",
            "target": "opponent",
            "stat": "attack",
            "stages": -1,
        },
    }

    ability = Ability.from_dict(data)

    assert ability.id == "intimidate"
    assert ability.trigger == AbilityTrigger.ON_SWITCH_IN
    assert ability.effect_config["type"] == "stat_change"
    assert ability.effect_config["stages"] == -1


def test_ability_from_dict_ailment_immunity():
    """状態異常無効特性の作成テスト"""
    data = {
        "id": "insomnia",
        "name": "Insomnia",
        "description": "眠り状態にならない",
        "trigger": "passive",
        "effect_config": {"type": "ailment_immunity", "immune_to": ["asleep"]},
    }

    ability = Ability.from_dict(data)

    assert ability.id == "insomnia"
    assert ability.trigger == AbilityTrigger.PASSIVE
    assert ability.effect_config["type"] == "ailment_immunity"
    assert "asleep" in ability.effect_config["immune_to"]


def test_ability_from_dict_ailment_inflict():
    """状態異常付与特性の作成テスト"""
    data = {
        "id": "static",
        "name": "Static",
        "description": "接触技を受けた時、30%で相手を麻痺",
        "trigger": "on_hit",
        "effect_config": {
            "type": "ailment_inflict",
            "ailment": "paralyzed",
            "chance": 0.3,
            "contact_only": True,
        },
    }

    ability = Ability.from_dict(data)

    assert ability.id == "static"
    assert ability.trigger == AbilityTrigger.ON_HIT
    assert ability.effect_config["type"] == "ailment_inflict"
    assert ability.effect_config["chance"] == 0.3


def test_get_effect_type():
    """効果タイプ取得のテスト"""
    data = {
        "id": "blaze",
        "name": "Blaze",
        "description": "HP 1/3以下で炎タイプの技威力1.5倍",
        "trigger": "on_attack",
        "effect_config": {"type": "type_boost", "boosted_type": "fire"},
    }

    ability = Ability.from_dict(data)
    assert ability.get_effect_type() == "type_boost"


def test_is_type_boost():
    """タイプ強化判定のテスト"""
    data1 = {
        "id": "blaze",
        "name": "Blaze",
        "description": "Test",
        "trigger": "on_attack",
        "effect_config": {"type": "type_boost"},
    }

    data2 = {
        "id": "intimidate",
        "name": "Intimidate",
        "description": "Test",
        "trigger": "on_switch_in",
        "effect_config": {"type": "stat_change"},
    }

    ability1 = Ability.from_dict(data1)
    ability2 = Ability.from_dict(data2)

    assert ability1.is_type_boost() is True
    assert ability2.is_type_boost() is False


def test_is_stat_change():
    """能力変化判定のテスト"""
    data = {
        "id": "intimidate",
        "name": "Intimidate",
        "description": "Test",
        "trigger": "on_switch_in",
        "effect_config": {"type": "stat_change"},
    }

    ability = Ability.from_dict(data)
    assert ability.is_stat_change() is True


def test_is_ailment_immunity():
    """状態異常無効判定のテスト"""
    data = {
        "id": "insomnia",
        "name": "Insomnia",
        "description": "Test",
        "trigger": "passive",
        "effect_config": {"type": "ailment_immunity"},
    }

    ability = Ability.from_dict(data)
    assert ability.is_ailment_immunity() is True


def test_is_ailment_inflict():
    """状態異常付与判定のテスト"""
    data = {
        "id": "static",
        "name": "Static",
        "description": "Test",
        "trigger": "on_hit",
        "effect_config": {"type": "ailment_inflict"},
    }

    ability = Ability.from_dict(data)
    assert ability.is_ailment_inflict() is True
