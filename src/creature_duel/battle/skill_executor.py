"""スキル実行エンジン

スキルの実行、Effect適用、ログ記録を管理します。
"""

import random
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from creature_duel.domain.entities.creature import Creature
from creature_duel.domain.entities.skill import Skill
from creature_duel.domain.value_objects.status_ailment import StatusAilment
from creature_duel.domain.enums.ailment_type import AilmentType
from creature_duel.domain.enums.move_category import MoveCategory
from creature_duel.application.services.damage_calculator import calculate_damage
from creature_duel.application.services.accuracy_calculator import check_hit
from creature_duel.application.services.stat_modifier_service import StatModifierService


@dataclass
class SkillResult:
    """スキル実行の結果

    Attributes:
        hit: 命中したかどうか
        damage: 与えたダメージ（0の場合もあり）
        critical: クリティカルヒットだったか
        effectiveness: タイプ相性倍率
        effects_applied: 適用されたEffectのリスト
        target_fainted: 対象が倒れたか
    """

    hit: bool
    damage: int = 0
    critical: bool = False
    effectiveness: float = 1.0
    effects_applied: List[Dict[str, Any]] = None
    target_fainted: bool = False

    def __post_init__(self):
        if self.effects_applied is None:
            self.effects_applied = []


class SkillExecutor:
    """スキル実行エンジン

    スキルの実行全体を管理し、Effect適用とログ記録を行います。
    """

    def __init__(self):
        self.stat_modifier_service = StatModifierService()

    def execute_skill(
        self,
        attacker: Creature,
        defender: Creature,
        skill: Skill,
    ) -> SkillResult:
        """スキルを実行

        Args:
            attacker: 攻撃側のCreature
            defender: 防御側のCreature
            skill: 使用する技

        Returns:
            スキル実行結果

        処理フロー:
            1. PP消費
            2. 命中判定
            3. ダメージ計算・適用（攻撃技の場合）
            4. Effect適用
            5. 戦闘不能チェック
            6. 結果を返す
        """
        # PP消費
        skill.use()

        # 命中判定
        hit = check_hit(attacker, defender, skill)
        if not hit:
            return SkillResult(hit=False)

        # ダメージ計算（攻撃技の場合）
        damage = 0
        critical = False
        if skill.category != MoveCategory.STATUS:
            damage = calculate_damage(attacker, defender, skill)
            # クリティカルヒット判定（簡易版）
            critical = random.random() < attacker.battle_stats.critical_rate
            if critical:
                damage = int(damage * 2.0)

            defender.take_damage(damage)

        # Effect適用
        effects_applied = self._apply_effects(attacker, defender, skill)

        # 戦闘不能チェック
        target_fainted = defender.is_fainted()

        return SkillResult(
            hit=True,
            damage=damage,
            critical=critical,
            effects_applied=effects_applied,
            target_fainted=target_fainted,
        )

    def _apply_effects(
        self,
        attacker: Creature,
        defender: Creature,
        skill: Skill,
    ) -> List[Dict[str, Any]]:
        """Effectを適用

        Args:
            attacker: 攻撃側のCreature
            defender: 防御側のCreature
            skill: 使用した技

        Returns:
            適用されたEffectのリスト

        Notes:
            現在のskills.jsonではeffectsは空配列ですが、
            将来の拡張に備えてシステムを実装します。

            Effectの形式:
            {
                "type": "ailment" | "stat_change" | "heal",
                "target": "opponent" | "self",
                "chance": 0.0-1.0,
                ... (type別のパラメータ)
            }
        """
        effects_applied = []

        # スキルのeffectsを処理
        for effect in skill.effects:
            # 発動確率判定
            chance = effect.get("chance", 1.0)
            if random.random() > chance:
                continue

            effect_type = effect.get("type")
            target = effect.get("target", "opponent")

            # 対象の決定
            target_creature = defender if target == "opponent" else attacker

            # Effectタイプ別の処理
            if effect_type == "ailment":
                applied = self._apply_ailment_effect(target_creature, effect)
                if applied:
                    effects_applied.append(applied)

            elif effect_type == "stat_change":
                applied = self._apply_stat_change_effect(target_creature, effect)
                if applied:
                    effects_applied.append(applied)

        return effects_applied

    def _apply_ailment_effect(
        self,
        target: Creature,
        effect: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """状態異常Effectを適用

        Args:
            target: 対象のCreature
            effect: Effectの定義

        Returns:
            適用された場合、その情報を返す

        Effect形式:
        {
            "type": "ailment",
            "ailment": "poison" | "burn" | "freeze" | "sleep" | "paralysis" | "confusion",
            "turns": int (optional, 眠り・混乱の場合),
            "chance": float
        }
        """
        ailment_name = effect.get("ailment", "")

        # 状態異常タイプにマッピング
        ailment_map = {
            "poison": AilmentType.POISON,
            "burn": AilmentType.BURN,
            "freeze": AilmentType.FREEZE,
            "sleep": AilmentType.SLEEP,
            "paralysis": AilmentType.PARALYSIS,
            "confusion": AilmentType.CONFUSION,
        }

        ailment_type = ailment_map.get(ailment_name)
        if not ailment_type:
            return None

        # ターン制限がある場合
        turns = effect.get("turns")

        # 状態異常を作成
        ailment = StatusAilment(ailment_type, turns_remaining=turns)

        # 適用
        success = target.apply_status_ailment(ailment)
        if success:
            return {
                "type": "ailment",
                "ailment": ailment_name,
                "target": target.name,
            }

        return None

    def _apply_stat_change_effect(
        self,
        target: Creature,
        effect: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """能力変化Effectを適用

        Args:
            target: 対象のCreature
            effect: Effectの定義

        Returns:
            適用された場合、その情報を返す

        Effect形式:
        {
            "type": "stat_change",
            "stat": "attack" | "defence" | "sp_attack" | "sp_defence" | "speed" | "evasion" | "accuracy",
            "stages": int (-6 ~ +6),
            "chance": float
        }
        """
        stat_name = effect.get("stat", "")
        stages = effect.get("stages", 0)

        if not stat_name or stages == 0:
            return None

        # 能力ランクを変更
        actual_change = self.stat_modifier_service.modify_stat_stage(
            target.battle_stats, stat_name, stages
        )

        if actual_change != 0:
            return {
                "type": "stat_change",
                "stat": stat_name,
                "stages": actual_change,
                "target": target.name,
            }

        return None
