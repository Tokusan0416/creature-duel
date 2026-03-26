"""StatusAilmentのテスト"""

from creature_duel.domain.enums.ailment_type import AilmentType
from creature_duel.domain.value_objects.status_ailment import StatusAilment


def test_status_ailment_creation():
    """状態異常の生成テスト"""
    ailment = StatusAilment(AilmentType.POISON)
    assert ailment.ailment_type == AilmentType.POISON
    assert ailment.turns_remaining is None
    assert ailment.is_active is True


def test_status_ailment_with_duration():
    """ターン制限付き状態異常のテスト"""
    ailment = StatusAilment(AilmentType.SLEEP, turns_remaining=3)
    assert ailment.turns_remaining == 3
    assert ailment.is_active is True


def test_tick_reduces_turns():
    """tick()でターン数が減少するテスト"""
    ailment = StatusAilment(AilmentType.SLEEP, turns_remaining=3)

    # 1ターン目
    removed = ailment.tick()
    assert removed is False
    assert ailment.turns_remaining == 2
    assert ailment.is_active is True

    # 2ターン目
    removed = ailment.tick()
    assert removed is False
    assert ailment.turns_remaining == 1
    assert ailment.is_active is True

    # 3ターン目（解除）
    removed = ailment.tick()
    assert removed is True
    assert ailment.turns_remaining == 0
    assert ailment.is_active is False


def test_tick_with_no_duration():
    """無期限状態異常のtick()テスト"""
    ailment = StatusAilment(AilmentType.POISON)
    removed = ailment.tick()
    assert removed is False
    assert ailment.turns_remaining is None
    assert ailment.is_active is True


def test_deactivate():
    """状態異常の解除テスト"""
    ailment = StatusAilment(AilmentType.BURN)
    assert ailment.is_active is True

    ailment.deactivate()
    assert ailment.is_active is False


def test_get_damage_ratio_poison():
    """毒のダメージ割合テスト"""
    ailment = StatusAilment(AilmentType.POISON)
    assert ailment.get_damage_ratio() == 0.125


def test_get_damage_ratio_burn():
    """火傷のダメージ割合テスト"""
    ailment = StatusAilment(AilmentType.BURN)
    assert ailment.get_damage_ratio() == 0.0625


def test_get_damage_ratio_other():
    """その他の状態異常のダメージ割合テスト"""
    ailment = StatusAilment(AilmentType.FREEZE)
    assert ailment.get_damage_ratio() == 0.0

    ailment = StatusAilment(AilmentType.SLEEP)
    assert ailment.get_damage_ratio() == 0.0


def test_get_damage_ratio_inactive():
    """非アクティブ状態のダメージ割合テスト"""
    ailment = StatusAilment(AilmentType.POISON)
    ailment.deactivate()
    assert ailment.get_damage_ratio() == 0.0


def test_prevents_action_freeze():
    """氷状態の行動不能テスト"""
    ailment = StatusAilment(AilmentType.FREEZE)
    assert ailment.prevents_action() is True


def test_prevents_action_sleep():
    """眠り状態の行動不能テスト"""
    ailment = StatusAilment(AilmentType.SLEEP)
    assert ailment.prevents_action() is True


def test_prevents_action_other():
    """その他の状態異常の行動可能テスト"""
    assert StatusAilment(AilmentType.POISON).prevents_action() is False
    assert StatusAilment(AilmentType.BURN).prevents_action() is False
    assert StatusAilment(AilmentType.PARALYSIS).prevents_action() is False
    assert StatusAilment(AilmentType.CONFUSION).prevents_action() is False


def test_affects_attack_burn():
    """火傷による攻撃力低下テスト"""
    ailment = StatusAilment(AilmentType.BURN)
    assert ailment.affects_attack() is True


def test_affects_attack_other():
    """その他の状態異常は攻撃力に影響しないテスト"""
    assert StatusAilment(AilmentType.POISON).affects_attack() is False
    assert StatusAilment(AilmentType.FREEZE).affects_attack() is False


def test_affects_speed_paralysis():
    """麻痺による素早さ低下テスト"""
    ailment = StatusAilment(AilmentType.PARALYSIS)
    assert ailment.affects_speed() is True


def test_affects_speed_other():
    """その他の状態異常は素早さに影響しないテスト"""
    assert StatusAilment(AilmentType.POISON).affects_speed() is False
    assert StatusAilment(AilmentType.BURN).affects_speed() is False


def test_repr():
    """文字列表現のテスト"""
    # ターン制限なし
    ailment1 = StatusAilment(AilmentType.POISON)
    assert repr(ailment1) == "poison"

    # ターン制限あり
    ailment2 = StatusAilment(AilmentType.SLEEP, turns_remaining=3)
    assert repr(ailment2) == "sleep (3 turns)"

    # 非アクティブ
    ailment3 = StatusAilment(AilmentType.BURN)
    ailment3.deactivate()
    assert repr(ailment3) == "No ailment"
