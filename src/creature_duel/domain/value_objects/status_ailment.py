"""状態異常のValue Object"""

from dataclasses import dataclass
from typing import Optional

from creature_duel.domain.enums.ailment_type import AilmentType


@dataclass
class StatusAilment:
    """状態異常の状態

    Attributes:
        ailment_type: 状態異常のタイプ
        turns_remaining: 残りターン数（None=無期限）
        is_active: 現在有効かどうか
    """

    ailment_type: AilmentType
    turns_remaining: Optional[int] = None
    is_active: bool = True

    def tick(self) -> bool:
        """ターン経過処理

        Returns:
            状態異常が解除された場合True

        処理フロー:
            1. turns_remainingがNoneの場合は何もしない
            2. turns_remainingを1減らす
            3. 0になったら状態異常を解除
        """
        if self.turns_remaining is None:
            return False

        self.turns_remaining -= 1
        if self.turns_remaining <= 0:
            self.is_active = False
            return True

        return False

    def deactivate(self) -> None:
        """状態異常を解除する"""
        self.is_active = False

    def get_damage_ratio(self) -> float:
        """ターン終了時のダメージ割合を取得

        Returns:
            最大HPに対するダメージ割合（0.0 ~ 1.0）

        Notes:
            - POISON: 1/8 (0.125)
            - BURN: 1/16 (0.0625)
            - その他: 0.0
        """
        if not self.is_active:
            return 0.0

        if self.ailment_type == AilmentType.POISON:
            return 0.125
        elif self.ailment_type == AilmentType.BURN:
            return 0.0625

        return 0.0

    def prevents_action(self) -> bool:
        """行動不能かどうかを判定

        Returns:
            行動不能の場合True

        Notes:
            - FREEZE: 常に行動不能
            - SLEEP: 常に行動不能
            - その他: False（PARALYSISとCONFUSIONは確率判定なのでここでは判定しない）
        """
        if not self.is_active:
            return False

        return self.ailment_type in (AilmentType.FREEZE, AilmentType.SLEEP)

    def affects_attack(self) -> bool:
        """攻撃力に影響するかどうかを判定

        Returns:
            攻撃力が半減する場合True

        Notes:
            - BURN: 物理攻撃が半減
        """
        if not self.is_active:
            return False

        return self.ailment_type == AilmentType.BURN

    def affects_speed(self) -> bool:
        """素早さに影響するかどうかを判定

        Returns:
            素早さが低下する場合True

        Notes:
            - PARALYSIS: 素早さが1/4になる
        """
        if not self.is_active:
            return False

        return self.ailment_type == AilmentType.PARALYSIS

    def __repr__(self) -> str:
        """文字列表現"""
        if not self.is_active:
            return "No ailment"

        if self.turns_remaining is not None:
            return f"{self.ailment_type.value} ({self.turns_remaining} turns)"
        return f"{self.ailment_type.value}"
