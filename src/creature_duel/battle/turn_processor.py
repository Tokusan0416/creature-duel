import random
from typing import Tuple

from creature_duel.battle.battle_state import BattleState
from creature_duel.domain.entities.creature import Creature
from creature_duel.domain.entities.skill import Skill
from creature_duel.application.services.damage_calculator import calculate_damage
from creature_duel.application.services.accuracy_calculator import check_hit


class TurnProcessor:
    """ターン処理を管理するクラス"""

    def process_turn(self, battle_state: BattleState) -> bool:
        """
        1ターンの処理を実行

        Args:
            battle_state: バトル状態

        Returns:
            バトルが終了した場合True

        処理フロー:
            1. ターン開始ログ
            2. Speed順の決定
            3. 各クリーチャーのスキル実行
            4. 戦闘不能チェック
        """
        battle_state.add_log({
            "event_type": "turn_start",
            "player1_hp": battle_state.player1_creature.battle_stats.current_hp,
            "player2_hp": battle_state.player2_creature.battle_stats.current_hp,
        })

        # Speed順の決定
        first, second = self._determine_turn_order(
            battle_state.player1_creature,
            battle_state.player2_creature
        )

        # 1番目のクリーチャーの行動
        first_fainted = self._execute_action(first[0], second[0], first[1], battle_state)
        if first_fainted:
            return True

        # 2番目のクリーチャーの行動（1番目が倒されていない場合）
        if not second[0].is_fainted():
            second_fainted = self._execute_action(second[0], first[0], second[1], battle_state)
            if second_fainted:
                return True

        battle_state.next_turn()
        return False

    def _determine_turn_order(
        self, creature1: Creature, creature2: Creature
    ) -> Tuple[Tuple[Creature, str], Tuple[Creature, str]]:
        """
        Speed順を決定

        Args:
            creature1: プレイヤー1のクリーチャー
            creature2: プレイヤー2のクリーチャー

        Returns:
            (先攻, 後攻)のタプル（各要素は(クリーチャー, プレイヤー名)）
        """
        speed1 = creature1.battle_stats.speed * creature1.battle_stats.get_speed_multiplier()
        speed2 = creature2.battle_stats.speed * creature2.battle_stats.get_speed_multiplier()

        if speed1 > speed2:
            return (creature1, "player1"), (creature2, "player2")
        elif speed2 > speed1:
            return (creature2, "player2"), (creature1, "player1")
        else:
            # 同速の場合はランダム
            if random.random() < 0.5:
                return (creature1, "player1"), (creature2, "player2")
            else:
                return (creature2, "player2"), (creature1, "player1")

    def _execute_action(
        self, attacker: Creature, defender: Creature, attacker_name: str, battle_state: BattleState
    ) -> bool:
        """
        クリーチャーの行動を実行

        Args:
            attacker: 攻撃側
            defender: 防御側
            attacker_name: 攻撃側の名前（"player1" or "player2"）
            battle_state: バトル状態

        Returns:
            防御側が倒れた場合True
        """
        # 使用可能な技からランダムに選択
        available_skills = attacker.get_available_skills()
        if not available_skills:
            battle_state.add_log({
                "event_type": "no_pp",
                "attacker": attacker_name,
                "creature": attacker.name,
            })
            return False

        skill = random.choice(available_skills)
        skill.use()

        battle_state.add_log({
            "event_type": "skill_used",
            "attacker": attacker_name,
            "creature": attacker.name,
            "skill": skill.name,
            "pp_remaining": skill.current_pp,
        })

        # 命中判定
        if not check_hit(attacker, defender, skill):
            battle_state.add_log({
                "event_type": "skill_missed",
                "attacker": attacker_name,
                "skill": skill.name,
            })
            return False

        # ダメージ計算
        damage = calculate_damage(attacker, defender, skill)
        defender.take_damage(damage)

        battle_state.add_log({
            "event_type": "damage_dealt",
            "attacker": attacker_name,
            "defender": "player1" if attacker_name == "player2" else "player2",
            "damage": damage,
            "remaining_hp": defender.battle_stats.current_hp,
        })

        # 戦闘不能チェック
        if defender.is_fainted():
            battle_state.add_log({
                "event_type": "creature_fainted",
                "creature": defender.name,
                "player": "player1" if attacker_name == "player2" else "player2",
            })
            return True

        return False
