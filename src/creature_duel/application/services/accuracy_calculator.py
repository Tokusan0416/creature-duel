import random
from creature_duel.domain.entities.creature import Creature
from creature_duel.domain.entities.skill import Skill


def check_hit(attacker: Creature, defender: Creature, skill: Skill) -> bool:
    """
    技が命中するかチェック

    Args:
        attacker: 攻撃側のクリーチャー
        defender: 防御側のクリーチャー
        skill: 使用する技

    Returns:
        命中する場合True

    Notes:
        最終命中率 = 技の命中率 * (1 + 攻撃側命中補正) * (1 - 防御側回避補正)
        例：
        - 技命中率90%、攻撃側命中+10%、防御側回避+20%
        - 0.9 * 1.1 * 0.8 = 0.792 (79.2%)
    """
    # 必中技の場合
    if skill.accuracy >= 1.0:
        return True

    # 最終命中率の計算
    attacker_accuracy_mod = 1.0 + attacker.battle_stats.accuracy
    defender_evasion_mod = 1.0 - defender.battle_stats.evasion

    final_accuracy = skill.accuracy * attacker_accuracy_mod * defender_evasion_mod

    # 命中率の下限・上限（10% ~ 100%）
    final_accuracy = max(0.1, min(1.0, final_accuracy))

    return random.random() < final_accuracy
