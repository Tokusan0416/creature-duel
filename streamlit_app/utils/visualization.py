"""可視化ヘルパー"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List
import pandas as pd


def create_hp_timeline_chart(battle_log: Dict[str, Any]) -> go.Figure:
    """
    HP推移グラフを作成

    Args:
        battle_log: バトルログ

    Returns:
        Plotlyフィギュア
    """
    # ターン毎のHPを抽出
    turns = []
    player1_hp = []
    player2_hp = []

    # 初期HP
    player1_max_hp = None
    player2_max_hp = None

    current_turn = 0
    p1_hp = 0
    p2_hp = 0

    for event in battle_log["logs"]:
        event_type = event.get("event_type")

        # ターン開始時にHPを記録
        if event_type == "turn_start":
            current_turn = event.get("turn", 0)
            p1_hp = event.get("player1_hp", 0)
            p2_hp = event.get("player2_hp", 0)

            turns.append(current_turn)
            player1_hp.append(p1_hp)
            player2_hp.append(p2_hp)

            # 最大HPを記録（最初のターンから）
            if player1_max_hp is None:
                player1_max_hp = p1_hp
                player2_max_hp = p2_hp

    # グラフ作成
    fig = go.Figure()

    # Player1のHP
    fig.add_trace(go.Scatter(
        x=turns,
        y=player1_hp,
        mode='lines+markers',
        name='Player 1',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=8),
    ))

    # Player2のHP
    fig.add_trace(go.Scatter(
        x=turns,
        y=player2_hp,
        mode='lines+markers',
        name='Player 2',
        line=dict(color='#4ECDC4', width=3),
        marker=dict(size=8),
    ))

    # レイアウト設定
    fig.update_layout(
        title="HP推移",
        xaxis_title="ターン",
        yaxis_title="HP",
        hovermode='x unified',
        template='plotly_white',
        height=400,
    )

    return fig


def create_damage_breakdown_chart(battle_log: Dict[str, Any]) -> go.Figure:
    """
    ダメージ内訳グラフを作成

    Args:
        battle_log: バトルログ

    Returns:
        Plotlyフィギュア
    """
    # ダメージを集計
    player1_damage = 0
    player2_damage = 0
    player1_critical = 0
    player2_critical = 0

    for event in battle_log["logs"]:
        if event.get("event_type") == "damage_dealt":
            damage = event.get("damage", 0)
            attacker = event.get("attacker", "")
            is_critical = event.get("critical", False)

            if attacker == "player1":
                player1_damage += damage
                if is_critical:
                    player1_critical += damage
            elif attacker == "player2":
                player2_damage += damage
                if is_critical:
                    player2_critical += damage

    # データ準備
    categories = ["Player 1", "Player 2"]
    total_damage = [player1_damage, player2_damage]
    critical_damage = [player1_critical, player2_critical]
    normal_damage = [player1_damage - player1_critical, player2_damage - player2_critical]

    # グラフ作成
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='通常ダメージ',
        x=categories,
        y=normal_damage,
        marker_color='#95E1D3',
    ))

    fig.add_trace(go.Bar(
        name='クリティカルダメージ',
        x=categories,
        y=critical_damage,
        marker_color='#F38181',
    ))

    # レイアウト設定
    fig.update_layout(
        title="総ダメージ内訳",
        xaxis_title="プレイヤー",
        yaxis_title="ダメージ",
        barmode='stack',
        template='plotly_white',
        height=400,
    )

    return fig


def create_win_rate_chart(stats: Dict[str, Any]) -> go.Figure:
    """
    勝率チャートを作成

    Args:
        stats: 統計データ

    Returns:
        Plotlyフィギュア
    """
    # データ準備
    labels = ['Player 1', 'Player 2', 'Draw']
    values = [
        stats.get('player1_wins', 0),
        stats.get('player2_wins', 0),
        stats.get('draws', 0),
    ]
    colors = ['#FF6B6B', '#4ECDC4', '#95E1D3']

    # グラフ作成
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hole=0.3,
    )])

    # レイアウト設定
    fig.update_layout(
        title="勝敗分布",
        template='plotly_white',
        height=400,
    )

    return fig


def create_creature_win_rate_chart(creature_stats: Dict[str, Dict[str, Any]]) -> go.Figure:
    """
    クリーチャー別勝率チャートを作成

    Args:
        creature_stats: クリーチャー別統計

    Returns:
        Plotlyフィギュア
    """
    # データ準備
    creatures = list(creature_stats.keys())
    win_rates = [data.get('win_rate', 0) * 100 for data in creature_stats.values()]
    battles = [data.get('battles', 0) for data in creature_stats.values()]

    # 勝率でソート
    sorted_data = sorted(zip(creatures, win_rates, battles), key=lambda x: x[1], reverse=True)
    creatures, win_rates, battles = zip(*sorted_data) if sorted_data else ([], [], [])

    # グラフ作成
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=list(creatures),
        y=list(win_rates),
        text=[f"{rate:.1f}%<br>({n}戦)" for rate, n in zip(win_rates, battles)],
        textposition='outside',
        marker_color='#4ECDC4',
    ))

    # レイアウト設定
    fig.update_layout(
        title="クリーチャー別勝率",
        xaxis_title="クリーチャー",
        yaxis_title="勝率 (%)",
        template='plotly_white',
        height=500,
        yaxis=dict(range=[0, 100]),
    )

    return fig


def create_type_matchup_heatmap(type_chart: Dict[str, Dict[str, float]]) -> go.Figure:
    """
    タイプ相性ヒートマップを作成

    Args:
        type_chart: タイプ相性表

    Returns:
        Plotlyフィギュア
    """
    # データ準備
    types = list(type_chart.keys())
    matrix = []

    for attacker in types:
        row = []
        for defender in types:
            effectiveness = type_chart[attacker].get(defender, 1.0)
            row.append(effectiveness)
        matrix.append(row)

    # グラフ作成
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=types,
        y=types,
        colorscale=[
            [0, '#F38181'],      # 0.0 (効果なし)
            [0.25, '#FFA07A'],   # 0.25 (効果いまひとつ)
            [0.5, '#FFE66D'],    # 0.5 (効果いまひとつ)
            [0.75, '#95E1D3'],   # 1.0 (通常)
            [1, '#4ECDC4'],      # 2.0-4.0 (効果抜群)
        ],
        text=[[f"{val}×" for val in row] for row in matrix],
        texttemplate="%{text}",
        textfont={"size": 12},
        colorbar=dict(title="倍率"),
    ))

    # レイアウト設定
    fig.update_layout(
        title="タイプ相性表（攻撃側 × 防御側）",
        xaxis_title="防御側タイプ",
        yaxis_title="攻撃側タイプ",
        template='plotly_white',
        height=500,
        width=600,
    )

    return fig


def create_turn_distribution_chart(logs: List[Dict[str, Any]]) -> go.Figure:
    """
    ターン数分布チャートを作成

    Args:
        logs: バトルログのリスト

    Returns:
        Plotlyフィギュア
    """
    # ターン数を抽出
    turns = [log["total_turns"] for log in logs]

    # グラフ作成
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=turns,
        nbinsx=20,
        marker_color='#95E1D3',
    ))

    # レイアウト設定
    fig.update_layout(
        title="バトルターン数分布",
        xaxis_title="ターン数",
        yaxis_title="バトル数",
        template='plotly_white',
        height=400,
    )

    return fig


def create_damage_stats_chart(logs: List[Dict[str, Any]]) -> go.Figure:
    """
    ダメージ統計チャートを作成

    Args:
        logs: バトルログのリスト

    Returns:
        Plotlyフィギュア
    """
    # バトル毎の総ダメージを抽出
    battle_damages = []

    for log in logs:
        total_damage = 0
        for event in log["logs"]:
            if event.get("event_type") == "damage_dealt":
                total_damage += event.get("damage", 0)
        battle_damages.append(total_damage)

    # グラフ作成
    fig = go.Figure()

    fig.add_trace(go.Box(
        y=battle_damages,
        name="総ダメージ",
        marker_color='#F38181',
        boxmean='sd',  # 平均と標準偏差を表示
    ))

    # レイアウト設定
    fig.update_layout(
        title="バトル毎の総ダメージ分布",
        yaxis_title="総ダメージ",
        template='plotly_white',
        height=400,
    )

    return fig
