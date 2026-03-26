"""能力値補正サービス

能力ランクの変更やHP依存の補正など、ステータスに関する計算を提供します。
"""

from creature_duel.domain.entities.creature import Creature
from creature_duel.domain.value_objects.stats import BattleStats


class StatModifierService:
    """能力値補正サービス

    能力ランクの変更、HP依存の補正計算など、
    ステータスに関する計算を一元管理します。
    """

    @staticmethod
    def modify_stat_stage(
        battle_stats: BattleStats, stat_name: str, change: int
    ) -> int:
        """能力ランクを変更する

        Args:
            battle_stats: 変更対象のBattleStats
            stat_name: 能力名 ("attack", "defence", "sp_attack", "sp_defence", "speed", "evasion", "accuracy")
            change: 変化量（-6 ~ +6）

        Returns:
            実際に変化した量

        Notes:
            - ランクは-6から+6の範囲に制限される
            - 上限・下限に達している場合は変化しない
        """
        return battle_stats.modify_stage(stat_name, change)

    @staticmethod
    def get_hp_boost_multiplier(creature: Creature) -> float:
        """HP依存の攻撃力補正倍率を取得

        Args:
            creature: 対象のCreature

        Returns:
            補正倍率（1.0, 1.25, 1.5のいずれか）

        Notes:
            - HP 50%以下: 1.25倍
            - HP 25%以下: 1.5倍
            - それ以外: 1.0倍（補正なし）

        処理フロー:
            1. CreatureのHP残量割合を取得
            2. HP割合に応じた補正倍率を返す
        """
        hp_percentage = creature.get_hp_percentage()

        if hp_percentage <= 0.25:
            return 1.5
        elif hp_percentage <= 0.5:
            return 1.25
        else:
            return 1.0

    @staticmethod
    def apply_status_ailment_modifiers(
        creature: Creature, attack_value: float
    ) -> float:
        """状態異常による能力補正を適用

        Args:
            creature: 対象のCreature
            attack_value: 元の攻撃力

        Returns:
            補正後の攻撃力

        Notes:
            - 火傷状態: 物理攻撃が半減（0.5倍）
            - 麻痺状態: 素早さが1/4（0.25倍）

        処理フロー:
            1. 状態異常があるかチェック
            2. 状態異常のタイプに応じて補正を適用
            3. 補正後の値を返す
        """
        if not creature.has_status_ailment():
            return attack_value

        assert creature.status_ailment is not None

        # 火傷状態: 攻撃力が半減
        if creature.status_ailment.affects_attack():
            return attack_value * 0.5

        return attack_value

    @staticmethod
    def get_effective_speed(creature: Creature) -> float:
        """実効的な素早さを取得

        Args:
            creature: 対象のCreature

        Returns:
            補正後の素早さ

        Notes:
            - 麻痺状態: 素早さが1/4
            - 能力ランク補正を適用
            - 状態異常補正を適用

        処理フロー:
            1. 基本素早さを取得
            2. 能力ランク補正を適用
            3. 状態異常補正を適用（麻痺で1/4）
            4. 最終的な素早さを返す
        """
        base_speed = creature.battle_stats.speed
        stage_multiplier = creature.battle_stats.get_speed_multiplier()

        effective_speed = base_speed * stage_multiplier

        # 麻痺状態: 素早さが1/4
        if creature.has_status_ailment():
            assert creature.status_ailment is not None
            if creature.status_ailment.affects_speed():
                effective_speed *= 0.25

        return effective_speed

    @staticmethod
    def reset_stat_stages(battle_stats: BattleStats) -> None:
        """全ての能力ランクを0にリセット

        Args:
            battle_stats: リセット対象のBattleStats

        処理フロー:
            1. 全ての能力ランクを0に設定
        """
        battle_stats.attack_stage = 0
        battle_stats.defence_stage = 0
        battle_stats.sp_attack_stage = 0
        battle_stats.sp_defence_stage = 0
        battle_stats.speed_stage = 0
        battle_stats.evasion_stage = 0
        battle_stats.accuracy_stage = 0
