"""SkillExecutorのテスト"""

from creature_duel.battle.skill_executor import SkillExecutor, SkillResult
from creature_duel.domain.entities.creature import Creature
from creature_duel.domain.entities.skill import Skill
from creature_duel.domain.value_objects.stats import Stats
from creature_duel.domain.value_objects.type import Type
from creature_duel.domain.enums.move_category import MoveCategory
from creature_duel.domain.enums.ailment_type import AilmentType


def test_execute_skill_basic():
    """基本的なスキル実行のテスト"""
    executor = SkillExecutor()

    # 攻撃側
    attacker_stats = Stats(
        hp=100, attack=100.0, defence=70.0, sp_attack=100.0, sp_defence=70.0, speed=70.0
    )
    skill = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
        effects=[],
    )
    attacker = Creature(
        name="Attacker", types=[Type.NORMAL], base_stats=attacker_stats, skills=[skill]
    )

    # 防御側
    defender_stats = Stats(
        hp=100, attack=70.0, defence=100.0, sp_attack=70.0, sp_defence=100.0, speed=70.0
    )
    defender = Creature(
        name="Defender", types=[Type.NORMAL], base_stats=defender_stats, skills=[skill]
    )

    # クリティカル率を0にして安定化
    attacker.battle_stats.critical_rate = 0.0

    result = executor.execute_skill(attacker, defender, skill)

    assert result.hit is True
    assert result.damage > 0
    assert result.target_fainted is False
    assert skill.current_pp == 34  # PP消費


def test_execute_skill_miss():
    """技が外れた場合のテスト"""
    executor = SkillExecutor()

    attacker_stats = Stats(
        hp=100, attack=100.0, defence=70.0, sp_attack=100.0, sp_defence=70.0, speed=70.0
    )
    # 命中率0の技
    skill = Skill(
        name="Miss Move",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=0.0,  # 必ず外れる
        max_pp=35,
        effects=[],
    )
    attacker = Creature(
        name="Attacker", types=[Type.NORMAL], base_stats=attacker_stats, skills=[skill]
    )

    defender_stats = Stats(
        hp=100, attack=70.0, defence=100.0, sp_attack=70.0, sp_defence=100.0, speed=70.0
    )
    defender = Creature(
        name="Defender", types=[Type.NORMAL], base_stats=defender_stats, skills=[skill]
    )

    result = executor.execute_skill(attacker, defender, skill)

    assert result.hit is False
    assert result.damage == 0
    assert defender.battle_stats.current_hp == 100  # ダメージなし


def test_execute_skill_faint_target():
    """対象を倒すテスト"""
    executor = SkillExecutor()

    attacker_stats = Stats(
        hp=100, attack=200.0, defence=70.0, sp_attack=200.0, sp_defence=70.0, speed=70.0
    )
    skill = Skill(
        name="Hyper Beam",
        type=Type.NORMAL,
        category=MoveCategory.SPECIAL,
        power=150,
        accuracy=1.0,
        max_pp=5,
        effects=[],
    )
    attacker = Creature(
        name="Attacker", types=[Type.NORMAL], base_stats=attacker_stats, skills=[skill]
    )

    defender_stats = Stats(
        hp=50, attack=70.0, defence=70.0, sp_attack=70.0, sp_defence=70.0, speed=70.0
    )
    defender = Creature(
        name="Defender", types=[Type.NORMAL], base_stats=defender_stats, skills=[skill]
    )

    # クリティカル率を0にして安定化
    attacker.battle_stats.critical_rate = 0.0

    result = executor.execute_skill(attacker, defender, skill)

    assert result.hit is True
    assert result.damage > 0
    assert result.target_fainted is True
    assert defender.is_fainted()


def test_execute_skill_with_ailment_effect():
    """状態異常付与Effectのテスト"""
    executor = SkillExecutor()

    attacker_stats = Stats(
        hp=100, attack=100.0, defence=70.0, sp_attack=100.0, sp_defence=70.0, speed=70.0
    )
    # 毒を付与する技
    skill = Skill(
        name="Poison Sting",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=15,
        accuracy=1.0,
        max_pp=35,
        effects=[
            {
                "type": "ailment",
                "ailment": "poison",
                "target": "opponent",
                "chance": 1.0,  # 100%発動
            }
        ],
    )
    attacker = Creature(
        name="Attacker", types=[Type.NORMAL], base_stats=attacker_stats, skills=[skill]
    )

    defender_stats = Stats(
        hp=100, attack=70.0, defence=100.0, sp_attack=70.0, sp_defence=100.0, speed=70.0
    )
    defender = Creature(
        name="Defender", types=[Type.NORMAL], base_stats=defender_stats, skills=[skill]
    )

    # クリティカル率を0にして安定化
    attacker.battle_stats.critical_rate = 0.0

    result = executor.execute_skill(attacker, defender, skill)

    assert result.hit is True
    assert len(result.effects_applied) == 1
    assert result.effects_applied[0]["type"] == "ailment"
    assert result.effects_applied[0]["ailment"] == "poison"
    assert defender.has_status_ailment()
    assert defender.status_ailment.ailment_type == AilmentType.POISON


def test_execute_skill_with_stat_change_effect():
    """能力変化Effectのテスト"""
    executor = SkillExecutor()

    attacker_stats = Stats(
        hp=100, attack=100.0, defence=70.0, sp_attack=100.0, sp_defence=70.0, speed=70.0
    )
    # 攻撃を下げる技
    skill = Skill(
        name="Growl",
        type=Type.NORMAL,
        category=MoveCategory.STATUS,
        power=0,
        accuracy=1.0,
        max_pp=40,
        effects=[
            {
                "type": "stat_change",
                "stat": "attack",
                "stages": -1,
                "target": "opponent",
                "chance": 1.0,
            }
        ],
    )
    attacker = Creature(
        name="Attacker", types=[Type.NORMAL], base_stats=attacker_stats, skills=[skill]
    )

    defender_stats = Stats(
        hp=100, attack=70.0, defence=100.0, sp_attack=70.0, sp_defence=100.0, speed=70.0
    )
    defender = Creature(
        name="Defender", types=[Type.NORMAL], base_stats=defender_stats, skills=[skill]
    )

    result = executor.execute_skill(attacker, defender, skill)

    assert result.hit is True
    assert result.damage == 0  # 変化技なのでダメージなし
    assert len(result.effects_applied) == 1
    assert result.effects_applied[0]["type"] == "stat_change"
    assert result.effects_applied[0]["stat"] == "attack"
    assert result.effects_applied[0]["stages"] == -1
    assert defender.battle_stats.attack_stage == -1


def test_execute_skill_status_move():
    """変化技のテスト（ダメージなし）"""
    executor = SkillExecutor()

    attacker_stats = Stats(
        hp=100, attack=100.0, defence=70.0, sp_attack=100.0, sp_defence=70.0, speed=70.0
    )
    skill = Skill(
        name="Growl",
        type=Type.NORMAL,
        category=MoveCategory.STATUS,
        power=0,
        accuracy=1.0,
        max_pp=40,
        effects=[],
    )
    attacker = Creature(
        name="Attacker", types=[Type.NORMAL], base_stats=attacker_stats, skills=[skill]
    )

    defender_stats = Stats(
        hp=100, attack=70.0, defence=100.0, sp_attack=70.0, sp_defence=100.0, speed=70.0
    )
    defender = Creature(
        name="Defender", types=[Type.NORMAL], base_stats=defender_stats, skills=[skill]
    )

    result = executor.execute_skill(attacker, defender, skill)

    assert result.hit is True
    assert result.damage == 0
    assert defender.battle_stats.current_hp == 100  # ダメージなし
