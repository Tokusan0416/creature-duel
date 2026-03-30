import random
from typing import Tuple

from creature_duel.battle.battle_state import BattleState
from creature_duel.battle.skill_executor import SkillExecutor
from creature_duel.domain.entities.creature import Creature
from creature_duel.domain.entities.skill import Skill
from creature_duel.application.services.stat_modifier_service import StatModifierService


class TurnProcessor:
    """ターン処理を管理するクラス"""

    def __init__(self):
        self.skill_executor = SkillExecutor()
        self.stat_modifier_service = StatModifierService()

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
            4. ターン終了時処理（状態異常ダメージ）
            5. 戦闘不能チェック
        """
        battle_state.add_log({
            "event_type": "turn_start",
            "turn": battle_state.turn,
            "player1_hp": battle_state.player1_creature.battle_stats.current_hp,
            "player2_hp": battle_state.player2_creature.battle_stats.current_hp,
        })

        # Speed順の決定（状態異常による素早さ補正も考慮）
        first, second = self._determine_turn_order(
            battle_state.player1_creature,
            battle_state.player2_creature
        )

        # 1番目のクリーチャーの行動
        first_fainted = self._execute_action(first[0], second[0], first[1], battle_state)
        if first_fainted:
            # ターン終了時処理
            self._process_turn_end(battle_state)
            return True

        # 2番目のクリーチャーの行動（1番目が倒されていない場合）
        if not second[0].is_fainted():
            second_fainted = self._execute_action(second[0], first[0], second[1], battle_state)
            if second_fainted:
                # ターン終了時処理
                self._process_turn_end(battle_state)
                return True

        # ターン終了時処理（状態異常ダメージ等）
        battle_ended = self._process_turn_end(battle_state)
        if battle_ended:
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

        Notes:
            状態異常による素早さ補正も考慮します（麻痺で1/4）
        """
        # StatModifierServiceで実効素早さを計算
        speed1 = self.stat_modifier_service.get_effective_speed(creature1)
        speed2 = self.stat_modifier_service.get_effective_speed(creature2)

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

        処理フロー:
            1. 状態異常による行動不能チェック
            2. スキル選択
            3. スキル実行（SkillExecutor使用）
            4. ログ記録
        """
        defender_name = "player1" if attacker_name == "player2" else "player2"

        # 状態異常による行動不能チェック
        if attacker.has_status_ailment():
            assert attacker.status_ailment is not None
            if attacker.status_ailment.prevents_action():
                battle_state.add_log({
                    "event_type": "cannot_move",
                    "attacker": attacker_name,
                    "creature": attacker.name,
                    "reason": attacker.status_ailment.ailment_type.value,
                })
                return False

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

        # スキル実行（SkillExecutor使用）
        result = self.skill_executor.execute_skill(attacker, defender, skill)

        # スキル使用ログ
        battle_state.add_log({
            "event_type": "skill_used",
            "attacker": attacker_name,
            "creature": attacker.name,
            "skill": skill.name,
            "pp_remaining": skill.current_pp,
        })

        # 命中判定ログ
        if not result.hit:
            battle_state.add_log({
                "event_type": "skill_missed",
                "attacker": attacker_name,
                "skill": skill.name,
            })
            return False

        # ダメージログ
        if result.damage > 0:
            battle_state.add_log({
                "event_type": "damage_dealt",
                "attacker": attacker_name,
                "defender": defender_name,
                "damage": result.damage,
                "critical": result.critical,
                "remaining_hp": defender.battle_stats.current_hp,
            })

        # Effectログ
        for effect in result.effects_applied:
            battle_state.add_log({
                "event_type": "effect_applied",
                "effect_type": effect["type"],
                "target": effect["target"],
                **{k: v for k, v in effect.items() if k not in ["type", "target"]},
            })

        # 戦闘不能チェック
        if result.target_fainted:
            battle_state.add_log({
                "event_type": "creature_fainted",
                "creature": defender.name,
                "player": defender_name,
            })
            return True

        return False

    def _process_turn_end(self, battle_state: BattleState) -> bool:
        """
        ターン終了時の処理

        Args:
            battle_state: バトル状態

        Returns:
            バトルが終了した場合True

        処理フロー:
            1. 各Creatureの状態異常ダメージ処理
            2. 戦闘不能チェック
        """
        # Player1の状態異常処理
        if battle_state.player1_creature.has_status_ailment():
            damage = battle_state.player1_creature.process_status_ailment_turn_end()
            if damage > 0:
                battle_state.add_log({
                    "event_type": "ailment_damage",
                    "player": "player1",
                    "creature": battle_state.player1_creature.name,
                    "ailment": battle_state.player1_creature.status_ailment.ailment_type.value,
                    "damage": damage,
                    "remaining_hp": battle_state.player1_creature.battle_stats.current_hp,
                })

            # 戦闘不能チェック
            if battle_state.player1_creature.is_fainted():
                battle_state.add_log({
                    "event_type": "creature_fainted",
                    "creature": battle_state.player1_creature.name,
                    "player": "player1",
                    "reason": "ailment_damage",
                })
                return True

        # Player2の状態異常処理
        if battle_state.player2_creature.has_status_ailment():
            damage = battle_state.player2_creature.process_status_ailment_turn_end()
            if damage > 0:
                battle_state.add_log({
                    "event_type": "ailment_damage",
                    "player": "player2",
                    "creature": battle_state.player2_creature.name,
                    "ailment": battle_state.player2_creature.status_ailment.ailment_type.value,
                    "damage": damage,
                    "remaining_hp": battle_state.player2_creature.battle_stats.current_hp,
                })

            # 戦闘不能チェック
            if battle_state.player2_creature.is_fainted():
                battle_state.add_log({
                    "event_type": "creature_fainted",
                    "creature": battle_state.player2_creature.name,
                    "player": "player2",
                    "reason": "ailment_damage",
                })
                return True

        return False
