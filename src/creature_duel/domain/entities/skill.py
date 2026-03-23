from dataclasses import dataclass
from typing import Optional, Callable

from creature_duel.domain.enums.move_category import MoveCategory
from creature_duel.domain.value_objects.type import Type


@dataclass
class Skill:
    """技（スキル）"""
    name: str
    type: Type
    category: MoveCategory
    power: int
    accuracy: float  # 0.0 ~ 1.0
    max_pp: int
    current_pp: int = 0
    effect: Optional[Callable] = None  # 追加効果（状態異常、能力変化等）

    def __post_init__(self):
        """初期化後の処理"""
        if self.current_pp == 0:
            self.current_pp = self.max_pp

    def can_use(self) -> bool:
        """技が使用可能か"""
        return self.current_pp > 0

    def use(self) -> bool:
        """
        技を使用する（PPを消費）

        Returns:
            使用できた場合True
        """
        if not self.can_use():
            return False

        self.current_pp -= 1
        return True

    def reset_pp(self):
        """PPを最大値にリセット"""
        self.current_pp = self.max_pp
