#!/usr/bin/env python3
"""
シンプルなバトルのデモスクリプト

2体のクリーチャーによる1対1のバトルを実行し、結果を表示します。
"""

import json
from creature_duel import (
    Creature,
    Skill,
    Stats,
    Type,
    MoveCategory,
    BattleEngine,
)


def create_charizard() -> Creature:
    """リザードンを作成"""
    flamethrower = Skill(
        name="Flamethrower",
        type=Type.FIRE,
        category=MoveCategory.SPECIAL,
        power=90,
        accuracy=1.0,
        max_pp=15,
    )

    fire_blast = Skill(
        name="Fire Blast",
        type=Type.FIRE,
        category=MoveCategory.SPECIAL,
        power=110,
        accuracy=0.85,
        max_pp=5,
    )

    dragon_claw = Skill(
        name="Dragon Claw",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=80,
        accuracy=1.0,
        max_pp=15,
    )

    air_slash = Skill(
        name="Air Slash",
        type=Type.NORMAL,
        category=MoveCategory.SPECIAL,
        power=75,
        accuracy=0.95,
        max_pp=15,
    )

    stats = Stats(
        hp=150,
        attack=84.0,
        defence=78.0,
        sp_attack=109.0,
        sp_defence=85.0,
        speed=100.0,
    )

    return Creature(
        name="Charizard",
        types=[Type.FIRE],
        base_stats=stats,
        skills=[flamethrower, fire_blast, dragon_claw, air_slash],
    )


def create_blastoise() -> Creature:
    """カメックスを作成"""
    hydro_pump = Skill(
        name="Hydro Pump",
        type=Type.WATER,
        category=MoveCategory.SPECIAL,
        power=110,
        accuracy=0.80,
        max_pp=5,
    )

    surf = Skill(
        name="Surf",
        type=Type.WATER,
        category=MoveCategory.SPECIAL,
        power=90,
        accuracy=1.0,
        max_pp=15,
    )

    ice_beam = Skill(
        name="Ice Beam",
        type=Type.ICE,
        category=MoveCategory.SPECIAL,
        power=90,
        accuracy=1.0,
        max_pp=10,
    )

    earthquake = Skill(
        name="Earthquake",
        type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        power=100,
        accuracy=1.0,
        max_pp=10,
    )

    stats = Stats(
        hp=158,
        attack=83.0,
        defence=100.0,
        sp_attack=85.0,
        sp_defence=105.0,
        speed=78.0,
    )

    return Creature(
        name="Blastoise",
        types=[Type.WATER],
        base_stats=stats,
        skills=[hydro_pump, surf, ice_beam, earthquake],
    )


def print_battle_summary(result: dict):
    """バトル結果のサマリーを表示"""
    print("\n" + "=" * 60)
    print("バトル結果")
    print("=" * 60)
    print(f"勝者: {result['winner']}")
    print(f"総ターン数: {result['total_turns']}")
    print("\n最終状態:")
    print(f"  Player1 ({result['final_state']['player1']['creature']}): "
          f"HP {result['final_state']['player1']['hp']} "
          f"{'(倒れた)' if result['final_state']['player1']['fainted'] else ''}")
    print(f"  Player2 ({result['final_state']['player2']['creature']}): "
          f"HP {result['final_state']['player2']['hp']} "
          f"{'(倒れた)' if result['final_state']['player2']['fainted'] else ''}")
    print("=" * 60)


def print_battle_log(result: dict):
    """バトルログを表示"""
    print("\n" + "=" * 60)
    print("バトルログ")
    print("=" * 60)

    for log in result['logs']:
        event_type = log.get('event_type')

        if event_type == 'battle_start':
            print(f"\nバトル開始！")
            print(f"  {log['player1_creature']} vs {log['player2_creature']}")

        elif event_type == 'turn_start':
            print(f"\n--- ターン {log['turn']} ---")
            print(f"  Player1 HP: {log['player1_hp']}")
            print(f"  Player2 HP: {log['player2_hp']}")

        elif event_type == 'skill_used':
            print(f"  {log['attacker']} の {log['creature']} が {log['skill']} を使った！ "
                  f"(残りPP: {log['pp_remaining']})")

        elif event_type == 'skill_missed':
            print(f"    しかし外れた！")

        elif event_type == 'damage_dealt':
            print(f"    {log['defender']} に {log['damage']} ダメージ！ "
                  f"(残りHP: {log['remaining_hp']})")

        elif event_type == 'creature_fainted':
            print(f"  {log['player']} の {log['creature']} は倒れた！")

        elif event_type == 'battle_end':
            print(f"\nバトル終了！ {log['winner']} の勝利！")

    print("=" * 60)


def save_battle_log(result: dict, filename: str = "battle_log.json"):
    """バトルログをJSONファイルに保存"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\nバトルログを {filename} に保存しました")


def main():
    """メイン処理"""
    print("Creature Duel - シンプルバトルデモ")
    print("=" * 60)

    # クリーチャーを作成
    charizard = create_charizard()
    blastoise = create_blastoise()

    print(f"\nPlayer1: {charizard.name} (HP: {charizard.base_stats.hp})")
    print(f"  タイプ: {[t.value for t in charizard.types]}")
    print(f"  技: {[s.name for s in charizard.skills]}")

    print(f"\nPlayer2: {blastoise.name} (HP: {blastoise.base_stats.hp})")
    print(f"  タイプ: {[t.value for t in blastoise.types]}")
    print(f"  技: {[s.name for s in blastoise.skills]}")

    # バトル実行
    print("\nバトル開始...")
    engine = BattleEngine()
    result = engine.execute_battle(charizard, blastoise)

    # 結果を表示
    print_battle_summary(result)
    print_battle_log(result)

    # ログをファイルに保存
    save_battle_log(result)


if __name__ == "__main__":
    main()
