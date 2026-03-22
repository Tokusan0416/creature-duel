from dataclasses import dataclass
from typing import List
from entities.creature import Creature

@dataclass
class BattleState:
    turn: int
    player1: Creature
    player2: Creature
    logs: List[dict]

    def add_log(self, event: dict):
        self.logs.append(event)