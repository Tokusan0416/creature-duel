"""DamageCalculatorのテスト"""

from creature_duel.application.services.damage_calculator import (
    calculate_damage,
    check_critical_hit,
)
from creature_duel.domain.entities.creature import Creature
from creature_duel.domain.entities.skill import Skill
from creature_duel.domain.value_objects.stats import Stats
from creature_duel.domain.value_objects.status_ailment import StatusAilment
from creature_duel.domain.value_objects.type import Type
from creature_duel.domain.enums.ailment_type import AilmentType
from creature_duel.domain.enums.move_category import MoveCategory


def test_calculate_damage_basic():
    """基本的なダメージ計算のテスト"""
    # 攻撃側
    attacker_stats = Stats(
        hp=100, attack=100.0, defence=70.0, sp_attack=100.0, sp_defence=70.0, speed=70.0
    )
    attacker_skill = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    attacker = Creature(
        name="Attacker", types=[Type.NORMAL], base_stats=attacker_stats, skills=[attacker_skill]
    )

    # 防御側
    defender_stats = Stats(
        hp=100, attack=70.0, defence=100.0, sp_attack=70.0, sp_defence=100.0, speed=70.0
    )
    defender_skill = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    defender = Creature(
        name="Defender", types=[Type.NORMAL], base_stats=defender_stats, skills=[defender_skill]
    )

    damage = calculate_damage(attacker, defender, attacker_skill)

    # 基本ダメージ = 100 * 40 / 100 = 40
    # STAB = 1.5倍（同タイプ）
    # 最終ダメージ = 40 * 1.5 = 60（クリティカル、HP依存の変動あり）
    assert damage > 0


def test_calculate_damage_type_effectiveness():
    """タイプ相性のテスト"""
    # 炎タイプの攻撃側
    attacker_stats = Stats(
        hp=100, attack=80.0, defence=70.0, sp_attack=110.0, sp_defence=70.0, speed=70.0
    )
    fire_skill = Skill(
        name="Flamethrower",
        type=Type.FIRE,
        category=MoveCategory.SPECIAL,
        power=90,
        accuracy=1.0,
        max_pp=15,
    )
    attacker = Creature(
        name="FireMon", types=[Type.FIRE], base_stats=attacker_stats, skills=[fire_skill]
    )

    # 草タイプの防御側（炎に弱い）
    defender_stats = Stats(
        hp=100, attack=70.0, defence=70.0, sp_attack=70.0, sp_defence=70.0, speed=70.0
    )
    defender_skill = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    defender = Creature(
        name="GrassMon", types=[Type.GRASS], base_stats=defender_stats, skills=[defender_skill]
    )

    damage = calculate_damage(attacker, defender, fire_skill)

    # タイプ相性2.0倍 + STAB1.5倍で高ダメージ
    assert damage > 100


def test_calculate_damage_with_stat_stages():
    """能力ランク補正のテスト"""
    attacker_stats = Stats(
        hp=100, attack=100.0, defence=70.0, sp_attack=100.0, sp_defence=70.0, speed=70.0
    )
    attacker_skill = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    attacker = Creature(
        name="Attacker", types=[Type.NORMAL], base_stats=attacker_stats, skills=[attacker_skill]
    )

    defender_stats = Stats(
        hp=100, attack=70.0, defence=100.0, sp_attack=70.0, sp_defence=100.0, speed=70.0
    )
    defender_skill = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    defender = Creature(
        name="Defender", types=[Type.NORMAL], base_stats=defender_stats, skills=[defender_skill]
    )

    # クリティカル率を0にして安定化
    attacker.battle_stats.critical_rate = 0.0

    # 通常ダメージ
    damage_normal = calculate_damage(attacker, defender, attacker_skill)

    # 攻撃ランク+2
    attacker.battle_stats.attack_stage = 2
    damage_boosted = calculate_damage(attacker, defender, attacker_skill)

    # +2段階で2.0倍なのでダメージが増加
    assert damage_boosted > damage_normal


def test_calculate_damage_with_burn():
    """火傷状態のテスト（物理攻撃半減）"""
    attacker_stats = Stats(
        hp=100, attack=100.0, defence=70.0, sp_attack=100.0, sp_defence=70.0, speed=70.0
    )
    physical_skill = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    attacker = Creature(
        name="Attacker",
        types=[Type.NORMAL],
        base_stats=attacker_stats,
        skills=[physical_skill],
    )

    defender_stats = Stats(
        hp=100, attack=70.0, defence=100.0, sp_attack=70.0, sp_defence=100.0, speed=70.0
    )
    defender_skill = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    defender = Creature(
        name="Defender", types=[Type.NORMAL], base_stats=defender_stats, skills=[defender_skill]
    )

    # 通常ダメージ
    damage_normal = calculate_damage(attacker, defender, physical_skill)

    # 火傷状態を適用
    burn_ailment = StatusAilment(AilmentType.BURN)
    attacker.apply_status_ailment(burn_ailment)

    # 火傷状態でのダメージ
    damage_burned = calculate_damage(attacker, defender, physical_skill)

    # 火傷で物理攻撃が半減
    assert damage_burned < damage_normal
    # 約半分になる（完全に半分にはならないのでマージンを持たせる）
    assert damage_burned <= damage_normal * 0.6


def test_calculate_damage_with_ability_blaze():
    """もうか特性のテスト（HP 1/3以下で炎技威力1.5倍）"""
    attacker_stats = Stats(
        hp=150, attack=84.0, defence=78.0, sp_attack=109.0, sp_defence=85.0, speed=100.0
    )
    fire_skill = Skill(
        name="Flamethrower",
        type=Type.FIRE,
        category=MoveCategory.SPECIAL,
        power=90,
        accuracy=1.0,
        max_pp=15,
    )
    attacker = Creature(
        name="Charizard",
        types=[Type.FIRE],
        base_stats=attacker_stats,
        skills=[fire_skill],
        ability="blaze",  # もうか特性
    )

    defender_stats = Stats(
        hp=100, attack=70.0, defence=70.0, sp_attack=70.0, sp_defence=70.0, speed=70.0
    )
    defender_skill = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    defender = Creature(
        name="Defender", types=[Type.NORMAL], base_stats=defender_stats, skills=[defender_skill]
    )

    # HP満タン時
    damage_full_hp = calculate_damage(attacker, defender, fire_skill)

    # HPを1/3以下にする
    attacker.take_damage(100)  # 残りHP 50 (33%)

    # もうか発動時
    damage_blaze = calculate_damage(attacker, defender, fire_skill)

    # もうかでダメージ増加（1.5倍）
    assert damage_blaze > damage_full_hp


def test_calculate_damage_status_skill():
    """変化技のテスト（ダメージ0）"""
    attacker_stats = Stats(
        hp=100, attack=100.0, defence=70.0, sp_attack=100.0, sp_defence=70.0, speed=70.0
    )
    status_skill = Skill(
        name="Growl",
        type=Type.NORMAL,
        category=MoveCategory.STATUS,
        power=0,
        accuracy=1.0,
        max_pp=40,
    )
    attacker = Creature(
        name="Attacker", types=[Type.NORMAL], base_stats=attacker_stats, skills=[status_skill]
    )

    defender_stats = Stats(
        hp=100, attack=70.0, defence=100.0, sp_attack=70.0, sp_defence=100.0, speed=70.0
    )
    defender_skill = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    defender = Creature(
        name="Defender", types=[Type.NORMAL], base_stats=defender_stats, skills=[defender_skill]
    )

    damage = calculate_damage(attacker, defender, status_skill)
    assert damage == 0


def test_check_critical_hit():
    """クリティカルヒット判定のテスト"""
    stats = Stats(
        hp=100, attack=80.0, defence=70.0, sp_attack=60.0, sp_defence=60.0, speed=70.0
    )
    skill = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    creature = Creature(name="Test", types=[Type.NORMAL], base_stats=stats, skills=[skill])

    # クリティカル率を設定
    creature.battle_stats.critical_rate = 0.1

    # 100回試行してクリティカルが発生することを確認
    critical_count = sum(check_critical_hit(creature) for _ in range(100))

    # 確率的に0より大きいはず
    assert critical_count > 0
