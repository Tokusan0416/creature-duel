"""バトル実行ヘルパー"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from creature_duel.battle.battle_engine import BattleEngine
from creature_duel.domain.entities.creature import Creature
from creature_duel.infrastructure.data.loader import MasterDataLoader


class BattleRunner:
    """バトル実行を管理するクラス"""

    def __init__(self, battle_logs_dir: Optional[Path] = None):
        """
        初期化

        Args:
            battle_logs_dir: バトルログ保存ディレクトリ（Noneの場合はデフォルト）
        """
        self.engine = BattleEngine()
        self.loader = MasterDataLoader()

        if battle_logs_dir is None:
            self.battle_logs_dir = Path("battle_logs")
        else:
            self.battle_logs_dir = battle_logs_dir

        # ディレクトリ作成
        self.battle_logs_dir.mkdir(parents=True, exist_ok=True)

    def execute_battle(
        self, creature1_name: str, creature2_name: str, save_log: bool = True
    ) -> Dict[str, Any]:
        """
        バトルを実行

        Args:
            creature1_name: クリーチャー1の名前
            creature2_name: クリーチャー2の名前
            save_log: ログを保存するか

        Returns:
            バトル結果
        """
        # クリーチャーを読み込み
        creature1 = self.loader.get_creature(creature1_name)
        creature2 = self.loader.get_creature(creature2_name)

        # バトル実行
        result = self.engine.execute_battle(creature1, creature2)

        # ログ保存
        if save_log:
            self._save_battle_log(result)

        return result

    def _save_battle_log(self, battle_result: Dict[str, Any]) -> Path:
        """
        バトルログを保存

        Args:
            battle_result: バトル結果

        Returns:
            保存したファイルパス
        """
        # ファイル名生成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        winner = battle_result["winner"]
        filename = f"battle_{timestamp}_{winner}.json"
        filepath = self.battle_logs_dir / filename

        # JSON保存
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(battle_result, f, indent=2, ensure_ascii=False)

        return filepath

    def load_battle_logs(self) -> list[Dict[str, Any]]:
        """
        すべてのバトルログを読み込み

        Returns:
            バトルログのリスト
        """
        logs = []

        if not self.battle_logs_dir.exists():
            return logs

        # JSONファイルを読み込み
        for filepath in sorted(self.battle_logs_dir.glob("battle_*.json"), reverse=True):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    log = json.load(f)
                    log["filepath"] = str(filepath)
                    log["filename"] = filepath.name
                    logs.append(log)
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
                continue

        return logs

    def get_battle_statistics(self, logs: list[Dict[str, Any]]) -> Dict[str, Any]:
        """
        バトルログから統計情報を抽出

        Args:
            logs: バトルログのリスト

        Returns:
            統計情報
        """
        if not logs:
            return {
                "total_battles": 0,
                "player1_wins": 0,
                "player2_wins": 0,
                "draws": 0,
                "avg_turns": 0.0,
                "total_damage": 0,
                "creature_stats": {},
                "type_stats": {},
            }

        # 基本統計
        total_battles = len(logs)
        player1_wins = sum(1 for log in logs if log["winner"] == "player1")
        player2_wins = sum(1 for log in logs if log["winner"] == "player2")
        draws = sum(1 for log in logs if log["winner"] == "draw")

        # 平均ターン数
        total_turns = sum(log["total_turns"] for log in logs)
        avg_turns = total_turns / total_battles if total_battles > 0 else 0.0

        # 総ダメージ
        total_damage = 0
        for log in logs:
            for event in log["logs"]:
                if event.get("event_type") == "damage_dealt":
                    total_damage += event.get("damage", 0)

        # クリーチャー別統計
        creature_stats = self._calculate_creature_stats(logs)

        # タイプ別統計
        type_stats = self._calculate_type_stats(logs)

        return {
            "total_battles": total_battles,
            "player1_wins": player1_wins,
            "player2_wins": player2_wins,
            "draws": draws,
            "win_rate_player1": player1_wins / total_battles if total_battles > 0 else 0.0,
            "win_rate_player2": player2_wins / total_battles if total_battles > 0 else 0.0,
            "draw_rate": draws / total_battles if total_battles > 0 else 0.0,
            "avg_turns": avg_turns,
            "total_damage": total_damage,
            "avg_damage_per_battle": total_damage / total_battles if total_battles > 0 else 0.0,
            "creature_stats": creature_stats,
            "type_stats": type_stats,
        }

    def _calculate_creature_stats(
        self, logs: list[Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        クリーチャー別統計を計算

        Args:
            logs: バトルログのリスト

        Returns:
            クリーチャー別統計
        """
        stats = {}

        for log in logs:
            # Player1のクリーチャー
            p1_creature = log["final_state"]["player1"]["creature"]
            if p1_creature not in stats:
                stats[p1_creature] = {"battles": 0, "wins": 0, "losses": 0, "draws": 0}

            stats[p1_creature]["battles"] += 1
            if log["winner"] == "player1":
                stats[p1_creature]["wins"] += 1
            elif log["winner"] == "player2":
                stats[p1_creature]["losses"] += 1
            else:
                stats[p1_creature]["draws"] += 1

            # Player2のクリーチャー
            p2_creature = log["final_state"]["player2"]["creature"]
            if p2_creature not in stats:
                stats[p2_creature] = {"battles": 0, "wins": 0, "losses": 0, "draws": 0}

            stats[p2_creature]["battles"] += 1
            if log["winner"] == "player2":
                stats[p2_creature]["wins"] += 1
            elif log["winner"] == "player1":
                stats[p2_creature]["losses"] += 1
            else:
                stats[p2_creature]["draws"] += 1

        # 勝率計算
        for creature, data in stats.items():
            if data["battles"] > 0:
                data["win_rate"] = data["wins"] / data["battles"]
            else:
                data["win_rate"] = 0.0

        return stats

    def _calculate_type_stats(self, logs: list[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        タイプ別統計を計算（簡易版）

        Args:
            logs: バトルログのリスト

        Returns:
            タイプ別統計
        """
        # 簡易実装：クリーチャー名からタイプを推測
        # より正確な実装にはマスタデータとの連携が必要
        type_mapping = {
            "Charizard": "fire",
            "Blastoise": "water",
            "Venusaur": "grass",
            "Pikachu": "electric",
            "Articuno": "ice",
            "Snorlax": "normal",
            "Arcanine": "fire",
            "Gyarados": "water",
            "Exeggutor": "grass",
            "Raichu": "electric",
        }

        stats = {}

        for log in logs:
            # Player1
            p1_creature = log["final_state"]["player1"]["creature"]
            p1_type = type_mapping.get(p1_creature, "unknown")

            if p1_type not in stats:
                stats[p1_type] = {"battles": 0, "wins": 0, "losses": 0, "draws": 0}

            stats[p1_type]["battles"] += 1
            if log["winner"] == "player1":
                stats[p1_type]["wins"] += 1
            elif log["winner"] == "player2":
                stats[p1_type]["losses"] += 1
            else:
                stats[p1_type]["draws"] += 1

            # Player2
            p2_creature = log["final_state"]["player2"]["creature"]
            p2_type = type_mapping.get(p2_creature, "unknown")

            if p2_type not in stats:
                stats[p2_type] = {"battles": 0, "wins": 0, "losses": 0, "draws": 0}

            stats[p2_type]["battles"] += 1
            if log["winner"] == "player2":
                stats[p2_type]["wins"] += 1
            elif log["winner"] == "player1":
                stats[p2_type]["losses"] += 1
            else:
                stats[p2_type]["draws"] += 1

        # 勝率計算
        for type_, data in stats.items():
            if data["battles"] > 0:
                data["win_rate"] = data["wins"] / data["battles"]
            else:
                data["win_rate"] = 0.0

        return stats
