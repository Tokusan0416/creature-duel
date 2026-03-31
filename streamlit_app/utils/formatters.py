"""フォーマット関数"""

from typing import List, Dict, Any
from creature_duel.domain.entities.creature import Creature
from creature_duel.domain.entities.skill import Skill
from creature_duel.domain.entities.ability import Ability
from creature_duel.domain.value_objects.type import Type


def format_creature_name(creature: Creature) -> str:
    """
    クリーチャー名をフォーマット

    Args:
        creature: Creatureエンティティ

    Returns:
        フォーマットされた名前
    """
    types_str = "/".join([t.value.capitalize() for t in creature.types])
    return f"{creature.name} ({types_str})"


def format_hp(current: int, max_hp: int) -> str:
    """
    HPをフォーマット

    Args:
        current: 現在のHP
        max_hp: 最大HP

    Returns:
        フォーマットされたHP
    """
    percentage = (current / max_hp * 100) if max_hp > 0 else 0
    return f"{current}/{max_hp} ({percentage:.1f}%)"


def format_type(type_: Type) -> str:
    """
    タイプをフォーマット

    Args:
        type_: Type

    Returns:
        フォーマットされたタイプ
    """
    type_colors = {
        "normal": "⚪",
        "fire": "🔥",
        "water": "💧",
        "grass": "🌿",
        "electric": "⚡",
        "ice": "❄️",
    }
    emoji = type_colors.get(type_.value, "")
    return f"{emoji} {type_.value.capitalize()}"


def format_skill_category(category: str) -> str:
    """
    技カテゴリをフォーマット

    Args:
        category: カテゴリ名

    Returns:
        フォーマットされたカテゴリ
    """
    category_icons = {
        "physical": "⚔️",
        "special": "✨",
        "status": "📊",
    }
    icon = category_icons.get(category.lower(), "")
    return f"{icon} {category.capitalize()}"


def format_pp(current: int, max_pp: int) -> str:
    """
    PPをフォーマット

    Args:
        current: 現在のPP
        max_pp: 最大PP

    Returns:
        フォーマットされたPP
    """
    return f"{current}/{max_pp}"


def format_stat_stage(stage: int) -> str:
    """
    能力ランクをフォーマット

    Args:
        stage: 能力ランク (-6 ~ +6)

    Returns:
        フォーマットされた能力ランク
    """
    if stage > 0:
        return f"+{stage}"
    elif stage < 0:
        return f"{stage}"
    else:
        return "±0"


def format_ailment(ailment_type: str) -> str:
    """
    状態異常をフォーマット

    Args:
        ailment_type: 状態異常タイプ

    Returns:
        フォーマットされた状態異常
    """
    ailment_icons = {
        "poison": "🟣",
        "burn": "🔥",
        "freeze": "❄️",
        "sleep": "💤",
        "paralysis": "⚡",
        "confusion": "😵",
    }
    icon = ailment_icons.get(ailment_type.lower(), "")
    return f"{icon} {ailment_type.capitalize()}"


def format_percentage(value: float) -> str:
    """
    パーセンテージをフォーマット

    Args:
        value: 値 (0.0 ~ 1.0)

    Returns:
        フォーマットされたパーセンテージ
    """
    return f"{value * 100:.1f}%"


def format_multiplier(value: float) -> str:
    """
    倍率をフォーマット

    Args:
        value: 倍率

    Returns:
        フォーマットされた倍率
    """
    return f"×{value:.2f}"


def format_battle_log_event(event: Dict[str, Any]) -> str:
    """
    バトルログイベントをテキスト形式にフォーマット

    Args:
        event: ログイベント

    Returns:
        フォーマットされたテキスト
    """
    event_type = event.get("event_type", "unknown")

    if event_type == "battle_start":
        return (
            f"⚔️ バトル開始: {event['player1_creature']} vs {event['player2_creature']}"
        )

    elif event_type == "turn_start":
        return f"🔄 ターン {event['turn']} 開始"

    elif event_type == "skill_used":
        return f"💥 {event['creature']} が {event['skill']} を使用！"

    elif event_type == "skill_missed":
        return f"💨 {event['creature']} の {event['skill']} は外れた！"

    elif event_type == "damage_dealt":
        critical = " クリティカルヒット！" if event.get("critical") else ""
        return f"⚡ {event['damage']}ダメージ！{critical}"

    elif event_type == "effect_applied":
        effect_type = event.get("effect_type", "")
        if effect_type == "ailment":
            ailment = event.get("ailment", "")
            return f"🟣 {event['target']} は {ailment} 状態になった！"
        elif effect_type == "stat_change":
            stat = event.get("stat", "")
            stages = event.get("stages", 0)
            return f"📊 {event['target']} の {stat} が {stages} 段階変化！"

    elif event_type == "ailment_damage":
        return f"🩸 {event['creature']} は {event['ailment']} のダメージ {event['damage']}！"

    elif event_type == "cannot_move":
        reason = event.get("reason", "")
        return f"😵 {event['creature']} は {reason} で動けない！"

    elif event_type == "no_pp":
        return f"💔 {event['creature']} の技のPPが足りない！"

    elif event_type == "creature_fainted":
        return f"💀 {event['creature']} は倒れた！"

    elif event_type == "battle_end":
        winner = event.get("winner", "")
        if winner == "draw":
            return "🤝 引き分け"
        else:
            return f"🎉 {winner} の勝利！"

    return f"❓ {event_type}"


def get_hp_color(hp_percentage: float) -> str:
    """
    HPパーセンテージに応じた色を取得

    Args:
        hp_percentage: HPパーセンテージ (0.0 ~ 1.0)

    Returns:
        色コード
    """
    if hp_percentage > 0.5:
        return "#4CAF50"  # Green
    elif hp_percentage > 0.2:
        return "#FF9800"  # Orange
    else:
        return "#F44336"  # Red


def get_type_color(type_: Type) -> str:
    """
    タイプに応じた色を取得

    Args:
        type_: Type

    Returns:
        色コード
    """
    type_colors = {
        Type.NORMAL: "#A8A878",
        Type.FIRE: "#F08030",
        Type.WATER: "#6890F0",
        Type.GRASS: "#78C850",
        Type.ELECTRIC: "#F8D030",
        Type.ICE: "#98D8D8",
    }
    return type_colors.get(type_, "#A8A878")


def format_ability_effect(ability: Ability) -> str:
    """
    特性の効果をフォーマット

    Args:
        ability: Abilityエンティティ

    Returns:
        フォーマットされた効果説明
    """
    effect_type = ability.get_effect_type()

    if effect_type == "type_boost":
        config = ability.effect_config
        boosted_type = config.get("boosted_type", "")
        multiplier = config.get("multiplier", 1.0)
        hp_threshold = config.get("hp_threshold", 0.0)
        return f"{boosted_type.capitalize()}タイプの技が{multiplier}倍（HP {hp_threshold*100:.0f}%以下）"

    elif effect_type == "stat_change":
        config = ability.effect_config
        stat = config.get("stat", "")
        stages = config.get("stages", 0)
        return f"{stat} を {stages} 段階変化"

    elif effect_type == "ailment_immunity":
        config = ability.effect_config
        immune_to = config.get("immune_to", [])
        return f"{', '.join(immune_to)} 無効"

    elif effect_type == "ailment_inflict":
        config = ability.effect_config
        ailment = config.get("ailment", "")
        chance = config.get("chance", 0.0)
        return f"接触時 {ailment} 付与 ({chance*100:.0f}%)"

    return ability.description
