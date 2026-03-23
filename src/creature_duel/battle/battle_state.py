from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime

from creature_duel.domain.entities.creature import Creature


@dataclass
class BattleState:
    """バトルの状態を管理するクラス"""
    turn: int
    player1_creature: Creature
    player2_creature: Creature
    logs: List[Dict[str, Any]] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)

    def add_log(self, event: Dict[str, Any]):
        """
        ログイベントを追加

        Args:
            event: ログイベント（辞書形式）
        """
        event["turn"] = self.turn
        event["timestamp"] = datetime.now().isoformat()
        self.logs.append(event)

    def next_turn(self):
        """次のターンに進む"""
        self.turn += 1

    def get_log_summary(self) -> Dict[str, Any]:
        """
        バトルログのサマリーを取得

        Returns:
            バトルログのサマリー情報
        """
        return {
            "total_turns": self.turn,
            "total_events": len(self.logs),
            "started_at": self.started_at.isoformat(),
            "ended_at": datetime.now().isoformat(),
        }
