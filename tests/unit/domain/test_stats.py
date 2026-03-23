import pytest
from creature_duel.domain.value_objects.stats import Stats, BattleStats


def test_stats_creation():
    """Stats作成のテスト"""
    stats = Stats(
        hp=100,
        attack=80.0,
        defence=70.0,
        sp_attack=90.0,
        sp_defence=80.0,
        speed=85.0,
    )

    assert stats.hp == 100
    assert stats.attack == 80.0


def test_battle_stats_stage_multiplier():
    """能力ランクの倍率計算テスト"""
    battle_stats = BattleStats(
        current_hp=100,
        max_hp=100,
        attack=100.0,
        defence=100.0,
        sp_attack=100.0,
        sp_defence=100.0,
        speed=100.0,
    )

    # ランク0: 1.0倍
    assert battle_stats.get_attack_multiplier() == 1.0

    # ランク+1: 1.5倍
    battle_stats.attack_stage = 1
    assert battle_stats.get_attack_multiplier() == 1.5

    # ランク+2: 2.0倍
    battle_stats.attack_stage = 2
    assert battle_stats.get_attack_multiplier() == 2.0

    # ランク+6: 4.0倍
    battle_stats.attack_stage = 6
    assert battle_stats.get_attack_multiplier() == 4.0

    # ランク-1: 0.67倍（約）
    battle_stats.attack_stage = -1
    assert abs(battle_stats.get_attack_multiplier() - 0.6666666) < 0.001

    # ランク-2: 0.5倍
    battle_stats.attack_stage = -2
    assert battle_stats.get_attack_multiplier() == 0.5

    # ランク-6: 0.25倍
    battle_stats.attack_stage = -6
    assert battle_stats.get_attack_multiplier() == 0.25


def test_modify_stage():
    """能力ランク変更のテスト"""
    battle_stats = BattleStats(
        current_hp=100,
        max_hp=100,
        attack=100.0,
        defence=100.0,
        sp_attack=100.0,
        sp_defence=100.0,
        speed=100.0,
    )

    # +2段階上昇
    change = battle_stats.modify_stage("attack", 2)
    assert change == 2
    assert battle_stats.attack_stage == 2

    # さらに+3段階上昇（合計+5）
    change = battle_stats.modify_stage("attack", 3)
    assert change == 3
    assert battle_stats.attack_stage == 5

    # さらに+3段階上昇を試みる（上限+6で止まる）
    change = battle_stats.modify_stage("attack", 3)
    assert change == 1
    assert battle_stats.attack_stage == 6

    # -4段階下降
    change = battle_stats.modify_stage("defence", -4)
    assert change == -4
    assert battle_stats.defence_stage == -4

    # さらに-4段階下降を試みる（下限-6で止まる）
    change = battle_stats.modify_stage("defence", -4)
    assert change == -2
    assert battle_stats.defence_stage == -6


def test_battle_stats_default_values():
    """BattleStatsのデフォルト値テスト"""
    battle_stats = BattleStats(
        current_hp=100,
        max_hp=100,
        attack=100.0,
        defence=100.0,
        sp_attack=100.0,
        sp_defence=100.0,
        speed=100.0,
    )

    assert battle_stats.evasion == 0.0
    assert battle_stats.accuracy == 0.0
    assert battle_stats.critical_rate == 0.1
    assert battle_stats.attack_stage == 0
    assert battle_stats.defence_stage == 0
