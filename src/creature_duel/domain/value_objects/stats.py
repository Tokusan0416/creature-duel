from dataclasses import dataclass


@dataclass
class Stats:
    """クリーチャーの基本ステータス"""
    hp: int
    attack: float
    defence: float
    sp_attack: float
    sp_defence: float
    speed: float


@dataclass
class BattleStats:
    """バトル中のステータス（変動する値を含む）"""
    # 基本ステータス
    current_hp: int
    max_hp: int
    attack: float
    defence: float
    sp_attack: float
    sp_defence: float
    speed: float

    # バトル開始時のデフォルト値
    evasion: float = 0.0          # 回避率: -50% ~ +50%
    accuracy: float = 0.0         # 命中: -50% ~ +50%
    critical_rate: float = 0.1    # 急所率: 0% ~ 20%

    # 能力ランク（-6 ~ +6段階）
    attack_stage: int = 0
    defence_stage: int = 0
    sp_attack_stage: int = 0
    sp_defence_stage: int = 0
    speed_stage: int = 0
    evasion_stage: int = 0
    accuracy_stage: int = 0

    def get_attack_multiplier(self) -> float:
        """攻撃ランクの倍率を取得"""
        return self._get_stage_multiplier(self.attack_stage)

    def get_defence_multiplier(self) -> float:
        """防御ランクの倍率を取得"""
        return self._get_stage_multiplier(self.defence_stage)

    def get_sp_attack_multiplier(self) -> float:
        """特攻ランクの倍率を取得"""
        return self._get_stage_multiplier(self.sp_attack_stage)

    def get_sp_defence_multiplier(self) -> float:
        """特防ランクの倍率を取得"""
        return self._get_stage_multiplier(self.sp_defence_stage)

    def get_speed_multiplier(self) -> float:
        """素早さランクの倍率を取得"""
        return self._get_stage_multiplier(self.speed_stage)

    @staticmethod
    def _get_stage_multiplier(stage: int) -> float:
        """
        能力ランクから倍率を計算

        ポケモンの仕様に準拠：
        +6: 4.0倍, +5: 3.5倍, +4: 3.0倍, +3: 2.5倍, +2: 2.0倍, +1: 1.5倍
        0: 1.0倍
        -1: 0.67倍, -2: 0.5倍, -3: 0.4倍, -4: 0.33倍, -5: 0.29倍, -6: 0.25倍
        """
        if stage >= 0:
            return (2 + stage) / 2
        else:
            return 2 / (2 - stage)

    def modify_stage(self, stat_name: str, change: int) -> int:
        """
        能力ランクを変更する

        Args:
            stat_name: "attack", "defence", "sp_attack", "sp_defence", "speed", "evasion", "accuracy"
            change: 変化量（-6 ~ +6）

        Returns:
            実際に変化した量
        """
        stage_attr = f"{stat_name}_stage"
        if not hasattr(self, stage_attr):
            return 0

        current = getattr(self, stage_attr)
        new_stage = max(-6, min(6, current + change))
        actual_change = new_stage - current
        setattr(self, stage_attr, new_stage)

        return actual_change
