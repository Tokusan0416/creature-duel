"""TypeEffectivenessServiceのテスト"""

from creature_duel.application.services.type_effectiveness import TypeEffectivenessService
from creature_duel.domain.value_objects.type import Type


def test_type_effectiveness_single_type():
    """単タイプの相性計算のテスト"""
    service = TypeEffectivenessService()

    # 有利な相性（2.0倍）
    assert service.get_type_multiplier(Type.FIRE, [Type.GRASS]) == 2.0
    assert service.get_type_multiplier(Type.WATER, [Type.FIRE]) == 2.0
    assert service.get_type_multiplier(Type.GRASS, [Type.WATER]) == 2.0
    assert service.get_type_multiplier(Type.ELECTRIC, [Type.WATER]) == 2.0
    assert service.get_type_multiplier(Type.ICE, [Type.GRASS]) == 2.0

    # 不利な相性（0.5倍）
    assert service.get_type_multiplier(Type.FIRE, [Type.WATER]) == 0.5
    assert service.get_type_multiplier(Type.WATER, [Type.GRASS]) == 0.5
    assert service.get_type_multiplier(Type.GRASS, [Type.FIRE]) == 0.5
    assert service.get_type_multiplier(Type.ELECTRIC, [Type.GRASS]) == 0.5

    # 等倍（1.0倍）
    assert service.get_type_multiplier(Type.NORMAL, [Type.FIRE]) == 1.0
    assert service.get_type_multiplier(Type.FIRE, [Type.NORMAL]) == 1.0


def test_type_effectiveness_dual_type():
    """複合タイプの相性計算のテスト"""
    service = TypeEffectivenessService()

    # 両方とも有効（2.0 * 2.0 = 4.0倍）
    assert service.get_type_multiplier(Type.FIRE, [Type.GRASS, Type.ICE]) == 4.0

    # 有効と無効が相殺（2.0 * 0.5 = 1.0倍）
    assert service.get_type_multiplier(Type.FIRE, [Type.WATER, Type.GRASS]) == 1.0

    # 両方とも無効（0.5 * 0.5 = 0.25倍）
    assert service.get_type_multiplier(Type.FIRE, [Type.WATER, Type.FIRE]) == 0.25

    # 有効と等倍（2.0 * 1.0 = 2.0倍）
    assert service.get_type_multiplier(Type.FIRE, [Type.GRASS, Type.NORMAL]) == 2.0


def test_type_effectiveness_normal_type():
    """ノーマルタイプの相性計算のテスト"""
    service = TypeEffectivenessService()

    # ノーマルタイプは全て等倍
    assert service.get_type_multiplier(Type.NORMAL, [Type.NORMAL]) == 1.0
    assert service.get_type_multiplier(Type.NORMAL, [Type.FIRE]) == 1.0
    assert service.get_type_multiplier(Type.NORMAL, [Type.WATER]) == 1.0
    assert service.get_type_multiplier(Type.NORMAL, [Type.GRASS]) == 1.0
    assert service.get_type_multiplier(Type.NORMAL, [Type.ELECTRIC]) == 1.0
    assert service.get_type_multiplier(Type.NORMAL, [Type.ICE]) == 1.0


def test_type_effectiveness_cache():
    """タイプ相性表のキャッシュ動作のテスト"""
    service = TypeEffectivenessService()

    # 初回呼び出し
    result1 = service.get_type_multiplier(Type.FIRE, [Type.GRASS])
    # 2回目呼び出し（キャッシュから取得）
    result2 = service.get_type_multiplier(Type.FIRE, [Type.GRASS])

    assert result1 == result2 == 2.0
    assert service._type_chart is not None  # キャッシュされている
