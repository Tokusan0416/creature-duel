#!/usr/bin/env python3
"""
マスタデータからクリーチャーを読み込んでバトルを実行するデモスクリプト

JSONマスタデータを使用した実践的なバトル例
"""

import json
from creature_duel.infrastructure.data.loader import MasterDataLoader
from creature_duel.battle.battle_engine import BattleEngine


def print_creature_info(creature_id: str, loader: MasterDataLoader):
    """クリーチャー情報を表示"""
    creature = loader.get_creature(creature_id)
    print(f"\n{creature.name} ({creature_id})")
    print(f"  タイプ: {[t.value for t in creature.types]}")
    print(f"  特性: {creature.ability}")
    print(f"  HP: {creature.base_stats.hp}")
    print(f"  Attack: {creature.base_stats.attack}")
    print(f"  Defence: {creature.base_stats.defence}")
    print(f"  Sp.Attack: {creature.base_stats.sp_attack}")
    print(f"  Sp.Defence: {creature.base_stats.sp_defence}")
    print(f"  Speed: {creature.base_stats.speed}")
    print(f"  技: {[s.name for s in creature.skills]}")


def print_battle_summary(result: dict, creature1_name: str, creature2_name: str):
    """バトル結果のサマリーを表示"""
    print("\n" + "=" * 60)
    print("バトル結果")
    print("=" * 60)
    print(f"勝者: {result['winner']}")
    print(f"総ターン数: {result['total_turns']}")
    print("\n最終状態:")
    print(f"  Player1 ({creature1_name}): "
          f"HP {result['final_state']['player1']['hp']} "
          f"{'(倒れた)' if result['final_state']['player1']['fainted'] else ''}")
    print(f"  Player2 ({creature2_name}): "
          f"HP {result['final_state']['player2']['hp']} "
          f"{'(倒れた)' if result['final_state']['player2']['fainted'] else ''}")
    print("=" * 60)


def save_battle_log(result: dict, filename: str = "battle_log.json"):
    """バトルログをJSONファイルに保存"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\nバトルログを {filename} に保存しました")


def main():
    """メイン処理"""
    print("Creature Duel - マスタデータバトルデモ")
    print("=" * 60)

    # ローダーの初期化
    loader = MasterDataLoader()

    # 利用可能なクリーチャーを表示
    print("\n利用可能なクリーチャー:")
    for creature_id in loader.list_creatures():
        print(f"  - {creature_id}")

    # バトルするクリーチャーを選択
    creature1_id = "charizard"
    creature2_id = "blastoise"

    # クリーチャー情報を表示
    print("\n" + "=" * 60)
    print("バトル参加者")
    print("=" * 60)
    print_creature_info(creature1_id, loader)
    print_creature_info(creature2_id, loader)

    # クリーチャーを読み込み
    creature1 = loader.get_creature(creature1_id)
    creature2 = loader.get_creature(creature2_id)

    # バトル実行
    print("\n" + "=" * 60)
    print("バトル開始！")
    print("=" * 60)

    engine = BattleEngine()
    result = engine.execute_battle(creature1, creature2)

    # 結果を表示
    print_battle_summary(result, creature1.name, creature2.name)

    # ログをファイルに保存
    save_battle_log(result, "battle_log_master.json")

    # 別の組み合わせでもう一度バトル
    print("\n\n" + "=" * 60)
    print("2回目のバトル")
    print("=" * 60)

    creature3_id = "pikachu"
    creature4_id = "vaporeon"

    print_creature_info(creature3_id, loader)
    print_creature_info(creature4_id, loader)

    creature3 = loader.get_creature(creature3_id)
    creature4 = loader.get_creature(creature4_id)

    print("\nバトル開始！")
    result2 = engine.execute_battle(creature3, creature4)
    print_battle_summary(result2, creature3.name, creature4.name)


if __name__ == "__main__":
    main()
