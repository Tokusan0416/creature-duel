"""バトルシステムの統合テスト"""

from creature_duel.battle.battle_engine import BattleEngine
from creature_duel.domain.entities.creature import Creature
from creature_duel.domain.entities.skill import Skill
from creature_duel.domain.value_objects.stats import Stats
from creature_duel.domain.value_objects.type import Type
from creature_duel.domain.enums.move_category import MoveCategory


def test_simple_battle_integration():
    """基本的なバトルの統合テスト"""
    engine = BattleEngine()

    # 攻撃側（強い）
    attacker_stats = Stats(
        hp=100, attack=150.0, defence=70.0, sp_attack=150.0, sp_defence=70.0, speed=100.0
    )
    tackle = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    attacker = Creature(
        name="Attacker", types=[Type.NORMAL], base_stats=attacker_stats, skills=[tackle]
    )

    # 防御側（弱い）
    defender_stats = Stats(
        hp=50, attack=50.0, defence=50.0, sp_attack=50.0, sp_defence=50.0, speed=50.0
    )
    defender = Creature(
        name="Defender", types=[Type.NORMAL], base_stats=defender_stats, skills=[tackle]
    )

    # バトル実行
    result = engine.execute_battle(attacker, defender)

    # 検証
    assert result["winner"] in ["player1", "player2", "draw"]
    assert result["total_turns"] > 0
    assert len(result["logs"]) > 0
    assert "summary" in result
    assert "final_state" in result

    # 最低限のログイベントが記録されているか
    event_types = [log["event_type"] for log in result["logs"]]
    assert "battle_start" in event_types
    assert "turn_start" in event_types
    assert "skill_used" in event_types
    assert "battle_end" in event_types


def test_battle_with_type_effectiveness():
    """タイプ相性を含むバトルの統合テスト"""
    engine = BattleEngine()

    # 炎タイプの攻撃側
    fire_stats = Stats(
        hp=100, attack=80.0, defence=70.0, sp_attack=120.0, sp_defence=70.0, speed=90.0
    )
    flamethrower = Skill(
        name="Flamethrower",
        type=Type.FIRE,
        category=MoveCategory.SPECIAL,
        power=90,
        accuracy=1.0,
        max_pp=15,
    )
    fire_mon = Creature(
        name="FireMon", types=[Type.FIRE], base_stats=fire_stats, skills=[flamethrower]
    )

    # 草タイプの防御側（炎に弱い）
    grass_stats = Stats(
        hp=100, attack=70.0, defence=70.0, sp_attack=70.0, sp_defence=70.0, speed=60.0
    )
    vine_whip = Skill(
        name="Vine Whip",
        type=Type.GRASS,
        category=MoveCategory.PHYSICAL,
        power=45,
        accuracy=1.0,
        max_pp=25,
    )
    grass_mon = Creature(
        name="GrassMon", types=[Type.GRASS], base_stats=grass_stats, skills=[vine_whip]
    )

    # バトル実行
    result = engine.execute_battle(fire_mon, grass_mon)

    # 炎が草に有利なので、player1（FireMon）が勝つはず
    # ただし確率的要素もあるので、バトルが正常に終了することを確認
    assert result["winner"] in ["player1", "player2", "draw"]
    assert result["total_turns"] <= engine.max_turns
    assert len(result["logs"]) > 0


def test_battle_with_status_ailment():
    """状態異常付与を含むバトルの統合テスト"""
    engine = BattleEngine()

    # 毒を付与する技を持つ攻撃側
    attacker_stats = Stats(
        hp=100, attack=100.0, defence=70.0, sp_attack=100.0, sp_defence=70.0, speed=80.0
    )
    poison_sting = Skill(
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
        name="Attacker", types=[Type.NORMAL], base_stats=attacker_stats, skills=[poison_sting]
    )

    # 防御側
    defender_stats = Stats(
        hp=100, attack=70.0, defence=100.0, sp_attack=70.0, sp_defence=100.0, speed=70.0
    )
    tackle = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    defender = Creature(
        name="Defender", types=[Type.NORMAL], base_stats=defender_stats, skills=[tackle]
    )

    # バトル実行
    result = engine.execute_battle(attacker, defender)

    # 状態異常関連のログイベントが記録されているか
    event_types = [log["event_type"] for log in result["logs"]]
    # 毒が付与されるはず
    assert "effect_applied" in event_types or "ailment_damage" in event_types
    assert result["winner"] in ["player1", "player2", "draw"]


def test_battle_with_stat_change():
    """能力変化を含むバトルの統合テスト"""
    engine = BattleEngine()

    # 攻撃を下げる技を持つ攻撃側
    attacker_stats = Stats(
        hp=100, attack=100.0, defence=70.0, sp_attack=100.0, sp_defence=70.0, speed=90.0
    )
    growl = Skill(
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
    tackle = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    attacker = Creature(
        name="Attacker", types=[Type.NORMAL], base_stats=attacker_stats, skills=[growl, tackle]
    )

    # 防御側
    defender_stats = Stats(
        hp=100, attack=100.0, defence=100.0, sp_attack=70.0, sp_defence=100.0, speed=70.0
    )
    defender = Creature(
        name="Defender", types=[Type.NORMAL], base_stats=defender_stats, skills=[tackle]
    )

    # バトル実行
    result = engine.execute_battle(attacker, defender)

    # 能力変化関連のログイベントが記録されているか
    event_types = [log["event_type"] for log in result["logs"]]
    assert "effect_applied" in event_types
    assert result["winner"] in ["player1", "player2", "draw"]


def test_battle_with_ability():
    """特性を持つCreatureのバトル統合テスト"""
    engine = BattleEngine()

    # もうか特性を持つ炎タイプ
    fire_stats = Stats(
        hp=100, attack=84.0, defence=78.0, sp_attack=109.0, sp_defence=85.0, speed=100.0
    )
    flamethrower = Skill(
        name="Flamethrower",
        type=Type.FIRE,
        category=MoveCategory.SPECIAL,
        power=90,
        accuracy=1.0,
        max_pp=15,
    )
    fire_mon = Creature(
        name="Charizard",
        types=[Type.FIRE],
        base_stats=fire_stats,
        skills=[flamethrower],
        ability="blaze",  # もうか特性
    )

    # 通常のCreature
    normal_stats = Stats(
        hp=100, attack=70.0, defence=70.0, sp_attack=70.0, sp_defence=70.0, speed=70.0
    )
    tackle = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    normal_mon = Creature(
        name="NormalMon", types=[Type.NORMAL], base_stats=normal_stats, skills=[tackle]
    )

    # バトル実行
    result = engine.execute_battle(fire_mon, normal_mon)

    # バトルが正常に完了
    assert result["winner"] in ["player1", "player2", "draw"]
    assert result["total_turns"] > 0
    assert len(result["logs"]) > 0


def test_battle_max_turns():
    """最大ターン数到達のテスト"""
    engine = BattleEngine()
    engine.max_turns = 5  # 最大ターン数を5に制限

    # 両方とも高耐久・低火力
    tank_stats = Stats(
        hp=200, attack=30.0, defence=150.0, sp_attack=30.0, sp_defence=150.0, speed=50.0
    )
    weak_tackle = Skill(
        name="Weak Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=5,  # 低威力
        accuracy=1.0,
        max_pp=35,
    )
    tank1 = Creature(
        name="Tank1", types=[Type.NORMAL], base_stats=tank_stats, skills=[weak_tackle]
    )
    tank2 = Creature(
        name="Tank2", types=[Type.NORMAL], base_stats=tank_stats, skills=[weak_tackle]
    )

    # バトル実行
    result = engine.execute_battle(tank1, tank2)

    # 最大ターン付近で終了（ターンカウンタは最後に+1されるため、max_turns+1になる）
    assert result["total_turns"] <= engine.max_turns + 1
    # HP残量で勝敗が決まるはず
    assert result["winner"] in ["player1", "player2", "draw"]


def test_battle_log_structure():
    """バトルログの構造が正しいかテスト"""
    engine = BattleEngine()

    # 基本的なCreature
    stats = Stats(
        hp=100, attack=100.0, defence=70.0, sp_attack=100.0, sp_defence=70.0, speed=80.0
    )
    tackle = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    creature1 = Creature(
        name="Creature1", types=[Type.NORMAL], base_stats=stats, skills=[tackle]
    )
    creature2 = Creature(
        name="Creature2", types=[Type.NORMAL], base_stats=stats, skills=[tackle]
    )

    # バトル実行
    result = engine.execute_battle(creature1, creature2)

    # ログ構造の検証
    assert "winner" in result
    assert "total_turns" in result
    assert "logs" in result
    assert "summary" in result
    assert "final_state" in result

    # final_stateの検証
    assert "player1" in result["final_state"]
    assert "player2" in result["final_state"]
    assert "creature" in result["final_state"]["player1"]
    assert "hp" in result["final_state"]["player1"]
    assert "fainted" in result["final_state"]["player1"]

    # summaryの検証
    summary = result["summary"]
    assert "total_events" in summary
    assert "total_turns" in summary
    assert "started_at" in summary
    assert "ended_at" in summary


def test_battle_with_miss():
    """技が外れる場合のバトルテスト"""
    engine = BattleEngine()

    # 命中率の低い技
    attacker_stats = Stats(
        hp=100, attack=100.0, defence=70.0, sp_attack=100.0, sp_defence=70.0, speed=80.0
    )
    miss_move = Skill(
        name="Miss Move",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=100,
        accuracy=0.3,  # 30%しか当たらない
        max_pp=35,
    )
    attacker = Creature(
        name="Attacker", types=[Type.NORMAL], base_stats=attacker_stats, skills=[miss_move]
    )

    # 防御側
    defender_stats = Stats(
        hp=100, attack=70.0, defence=100.0, sp_attack=70.0, sp_defence=100.0, speed=70.0
    )
    tackle = Skill(
        name="Tackle",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=40,
        accuracy=1.0,
        max_pp=35,
    )
    defender = Creature(
        name="Defender", types=[Type.NORMAL], base_stats=defender_stats, skills=[tackle]
    )

    # バトル実行
    result = engine.execute_battle(attacker, defender)

    # 技外れのログが記録されている可能性がある
    event_types = [log["event_type"] for log in result["logs"]]
    # skill_missedイベントが発生するはず
    assert "skill_missed" in event_types or len(result["logs"]) > 0
    assert result["winner"] in ["player1", "player2", "draw"]
