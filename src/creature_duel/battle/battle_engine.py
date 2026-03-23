from typing import Dict, Any

from creature_duel.domain.entities.creature import Creature
from creature_duel.battle.battle_state import BattleState
from creature_duel.battle.turn_processor import TurnProcessor


class BattleEngine:
    """バトル全体を制御するエンジン"""

    def __init__(self):
        self.turn_processor = TurnProcessor()
        self.max_turns = 100  # 無限ループ防止

    def execute_battle(
        self, creature1: Creature, creature2: Creature
    ) -> Dict[str, Any]:
        """
        バトルを実行

        Args:
            creature1: プレイヤー1のクリーチャー
            creature2: プレイヤー2のクリーチャー

        Returns:
            バトル結果（勝者、ログ等）

        処理フロー:
            1. バトル初期化
            2. ターン処理のループ
            3. 勝敗判定
            4. バトルログの生成
        """
        # クリーチャーをリセット
        creature1.reset()
        creature2.reset()

        # バトル状態の初期化
        battle_state = BattleState(
            turn=1,
            player1_creature=creature1,
            player2_creature=creature2,
        )

        battle_state.add_log({
            "event_type": "battle_start",
            "player1_creature": creature1.name,
            "player2_creature": creature2.name,
        })

        # ターンループ
        while battle_state.turn <= self.max_turns:
            battle_ended = self.turn_processor.process_turn(battle_state)
            if battle_ended:
                break

        # 勝敗判定
        winner = self._determine_winner(creature1, creature2)

        battle_state.add_log({
            "event_type": "battle_end",
            "winner": winner,
        })

        # 結果をまとめる
        return {
            "winner": winner,
            "total_turns": battle_state.turn,
            "logs": battle_state.logs,
            "summary": battle_state.get_log_summary(),
            "final_state": {
                "player1": {
                    "creature": creature1.name,
                    "hp": creature1.battle_stats.current_hp,
                    "fainted": creature1.is_fainted(),
                },
                "player2": {
                    "creature": creature2.name,
                    "hp": creature2.battle_stats.current_hp,
                    "fainted": creature2.is_fainted(),
                },
            },
        }

    def _determine_winner(self, creature1: Creature, creature2: Creature) -> str:
        """
        勝者を決定

        Args:
            creature1: プレイヤー1のクリーチャー
            creature2: プレイヤー2のクリーチャー

        Returns:
            "player1", "player2", or "draw"
        """
        if creature1.is_fainted() and creature2.is_fainted():
            return "draw"
        elif creature1.is_fainted():
            return "player2"
        elif creature2.is_fainted():
            return "player1"
        else:
            # どちらも倒れていない（最大ターン到達）
            # HP残量で判定
            hp1_percent = creature1.get_hp_percentage()
            hp2_percent = creature2.get_hp_percentage()

            if hp1_percent > hp2_percent:
                return "player1"
            elif hp2_percent > hp1_percent:
                return "player2"
            else:
                return "draw"
