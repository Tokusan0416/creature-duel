"""プレイヤーのエンティティ"""

from dataclasses import dataclass
from typing import List, Optional

from creature_duel.domain.entities.creature import Creature


@dataclass
class Player:
    """プレイヤー

    Attributes:
        name: プレイヤー名
        creatures: 所持しているCreatureのリスト（最大6体）
        current_creature_index: 現在出ているCreatureのインデックス
    """

    name: str
    creatures: List[Creature]
    current_creature_index: int = 0

    def __post_init__(self):
        """初期化後の処理

        Raises:
            ValueError: Creatureが0体または7体以上の場合
        """
        if len(self.creatures) == 0:
            raise ValueError("Creatures list cannot be empty")
        if len(self.creatures) > 6:
            raise ValueError("Cannot have more than 6 creatures")

    def get_current_creature(self) -> Creature:
        """現在出ているCreatureを取得

        Returns:
            現在出ているCreature
        """
        return self.creatures[self.current_creature_index]

    def switch_creature(self, index: int) -> bool:
        """Creatureを切り替える

        Args:
            index: 切り替え先のCreatureのインデックス

        Returns:
            切り替えに成功した場合True

        Notes:
            - 既に倒れているCreatureには切り替えできない
            - 現在と同じCreatureには切り替えできない
            - インデックスが範囲外の場合は失敗
        """
        # インデックスの範囲チェック
        if index < 0 or index >= len(self.creatures):
            return False

        # 現在と同じCreatureチェック
        if index == self.current_creature_index:
            return False

        # 倒れているCreatureチェック
        if self.creatures[index].is_fainted():
            return False

        self.current_creature_index = index
        return True

    def has_available_creatures(self) -> bool:
        """使用可能なCreatureがいるかどうか

        Returns:
            使用可能なCreatureがいる場合True
        """
        return any(not creature.is_fainted() for creature in self.creatures)

    def get_available_creatures(self) -> List[Creature]:
        """使用可能なCreatureのリストを取得

        Returns:
            倒れていないCreatureのリスト
        """
        return [creature for creature in self.creatures if not creature.is_fainted()]

    def get_fainted_count(self) -> int:
        """倒れているCreatureの数を取得

        Returns:
            倒れているCreatureの数
        """
        return sum(1 for creature in self.creatures if creature.is_fainted())

    def is_defeated(self) -> bool:
        """全てのCreatureが倒れているかどうか

        Returns:
            全て倒れている場合True
        """
        return not self.has_available_creatures()

    def reset_all_creatures(self) -> None:
        """全てのCreatureをリセット

        処理フロー:
            1. 全てのCreatureに対してreset()を呼び出す
            2. current_creature_indexを0に戻す
        """
        for creature in self.creatures:
            creature.reset()
        self.current_creature_index = 0
