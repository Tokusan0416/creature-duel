"""特性（Ability）のエンティティ"""

from dataclasses import dataclass
from typing import Any, Dict
from enum import Enum


class AbilityTrigger(Enum):
    """特性の発動タイミング

    Attributes:
        ON_ATTACK: 攻撃時に発動
        ON_HIT: 攻撃を受けた時に発動
        ON_SWITCH_IN: 場に出た時に発動
        PASSIVE: 常時発動（パッシブ）
    """

    ON_ATTACK = "on_attack"
    ON_HIT = "on_hit"
    ON_SWITCH_IN = "on_switch_in"
    PASSIVE = "passive"


@dataclass
class Ability:
    """特性（Ability）

    Attributes:
        id: 特性ID
        name: 表示名
        description: 説明
        trigger: 発動タイミング
        effect_config: 効果の設定（辞書形式）
    """

    id: str
    name: str
    description: str
    trigger: AbilityTrigger
    effect_config: Dict[str, Any]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Ability":
        """辞書からAbilityを作成

        Args:
            data: JSONから読み込んだ辞書

        Returns:
            Abilityインスタンス

        処理フロー:
            1. triggerを文字列からEnumに変換
            2. Abilityインスタンスを作成して返す
        """
        return Ability(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            trigger=AbilityTrigger(data["trigger"]),
            effect_config=data["effect_config"],
        )

    def get_effect_type(self) -> str:
        """効果のタイプを取得

        Returns:
            効果のタイプ（"type_boost", "stat_change", "ailment_immunity", "ailment_inflict"等）
        """
        return self.effect_config.get("type", "unknown")

    def is_type_boost(self) -> bool:
        """タイプ強化の特性かどうか

        Returns:
            タイプ強化の場合True
        """
        return self.get_effect_type() == "type_boost"

    def is_stat_change(self) -> bool:
        """能力変化の特性かどうか

        Returns:
            能力変化の場合True
        """
        return self.get_effect_type() == "stat_change"

    def is_ailment_immunity(self) -> bool:
        """状態異常無効の特性かどうか

        Returns:
            状態異常無効の場合True
        """
        return self.get_effect_type() == "ailment_immunity"

    def is_ailment_inflict(self) -> bool:
        """状態異常付与の特性かどうか

        Returns:
            状態異常付与の場合True
        """
        return self.get_effect_type() == "ailment_inflict"
