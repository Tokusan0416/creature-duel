"""タイプ相性計算サービス

タイプ相性表（type_chart.json）を使用してダメージ倍率を計算します。
"""

from typing import Dict, List

from creature_duel.domain.value_objects.type import Type
from creature_duel.infrastructure.data.loader import MasterDataLoader


class TypeEffectivenessService:
    """タイプ相性計算サービス

    マスタデータ（type_chart.json）からタイプ相性表を読み込み、
    攻撃タイプと防御タイプからダメージ倍率を計算します。
    """

    def __init__(self, loader: MasterDataLoader | None = None):
        """サービスを初期化

        Args:
            loader: マスタデータローダー（省略時は新規作成）
        """
        self._loader = loader or MasterDataLoader()
        self._type_chart: Dict[str, Dict[str, float]] | None = None

    def _load_type_chart(self) -> Dict[str, Dict[str, float]]:
        """タイプ相性表を読み込み（キャッシュ）

        Returns:
            タイプ相性表の辞書
        """
        if self._type_chart is None:
            self._type_chart = self._loader.load_type_chart()
        return self._type_chart

    def get_type_multiplier(
        self, attack_type: Type, defender_types: List[Type]
    ) -> float:
        """タイプ相性による倍率を計算

        Args:
            attack_type: 攻撃技のタイプ
            defender_types: 防御側のタイプリスト（1~2個）

        Returns:
            ダメージ倍率（0.25, 0.5, 1.0, 2.0, 4.0のいずれか）

        Notes:
            - 2タイプ持ちの場合、両方のタイプ相性を掛け合わせる
            - 例：ほのお技 vs みず/くさ → 0.5 * 2.0 = 1.0倍

        処理フロー:
            1. タイプ相性表をロード（初回のみ）
            2. 攻撃タイプの相性辞書を取得
            3. 防御側の各タイプについて倍率を掛け算
            4. 最終的な倍率を返す
        """
        type_chart = self._load_type_chart()

        # 攻撃タイプの相性辞書を取得
        attack_type_str = attack_type.value
        if attack_type_str not in type_chart:
            return 1.0

        effectiveness = type_chart[attack_type_str]

        # 防御側の各タイプについて倍率を掛け算
        multiplier = 1.0
        for defender_type in defender_types:
            defender_type_str = defender_type.value
            multiplier *= effectiveness.get(defender_type_str, 1.0)

        return multiplier
