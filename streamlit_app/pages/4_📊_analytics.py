"""統計・分析ページ"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.battle_runner import BattleRunner
from utils.visualization import (
    create_win_rate_chart,
    create_creature_win_rate_chart,
    create_turn_distribution_chart,
    create_damage_stats_chart,
)

# ページ設定
st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

# タイトル
st.title("📊 統計・分析")
st.markdown("バトルログから統計情報を分析します（ローカルデータ）")

# 初期化
if "battle_runner" not in st.session_state:
    st.session_state.battle_runner = BattleRunner()

battle_runner = st.session_state.battle_runner

# バトルログを読み込み
logs = battle_runner.load_battle_logs()

if not logs:
    st.info("📭 バトルログがありません。まずはバトルを実行してください！")
    st.markdown("👉 [バトル実行ページへ](🎮_battle)")
    st.stop()

# 統計情報を取得
stats = battle_runner.get_battle_statistics(logs)

# 全体統計
st.markdown("---")
st.markdown("## 📈 全体統計")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("総バトル数", stats["total_battles"])

with col2:
    st.metric(
        "Player 1 勝率",
        f"{stats['win_rate_player1'] * 100:.1f}%",
        delta=f"{stats['player1_wins']}勝",
    )

with col3:
    st.metric(
        "Player 2 勝率",
        f"{stats['win_rate_player2'] * 100:.1f}%",
        delta=f"{stats['player2_wins']}勝",
    )

with col4:
    st.metric(
        "引き分け率",
        f"{stats['draw_rate'] * 100:.1f}%",
        delta=f"{stats['draws']}戦",
    )

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("平均ターン数", f"{stats['avg_turns']:.1f}")

with col2:
    st.metric("総ダメージ", f"{stats['total_damage']:,}")

with col3:
    st.metric("平均ダメージ/バトル", f"{stats['avg_damage_per_battle']:.1f}")

# 勝敗分布
st.markdown("---")
st.markdown("## 🎯 勝敗分布")

col1, col2 = st.columns(2)

with col1:
    win_rate_chart = create_win_rate_chart(stats)
    st.plotly_chart(win_rate_chart, use_container_width=True)

with col2:
    # 勝敗の詳細
    st.markdown("### 詳細")
    st.markdown(f"**Player 1 勝利**: {stats['player1_wins']}戦 ({stats['win_rate_player1'] * 100:.1f}%)")
    st.markdown(f"**Player 2 勝利**: {stats['player2_wins']}戦 ({stats['win_rate_player2'] * 100:.1f}%)")
    st.markdown(f"**引き分け**: {stats['draws']}戦 ({stats['draw_rate'] * 100:.1f}%)")

    st.markdown("### 考察")
    if stats["win_rate_player1"] > stats["win_rate_player2"]:
        diff = (stats["win_rate_player1"] - stats["win_rate_player2"]) * 100
        st.info(f"💡 Player 1が{diff:.1f}%有利です")
    elif stats["win_rate_player2"] > stats["win_rate_player1"]:
        diff = (stats["win_rate_player2"] - stats["win_rate_player1"]) * 100
        st.info(f"💡 Player 2が{diff:.1f}%有利です")
    else:
        st.info("💡 両者互角です")

# クリーチャー別統計
st.markdown("---")
st.markdown("## 🐉 クリーチャー別統計")

creature_stats = stats["creature_stats"]

if creature_stats:
    # 勝率チャート
    creature_chart = create_creature_win_rate_chart(creature_stats)
    st.plotly_chart(creature_chart, use_container_width=True)

    # テーブル表示
    st.markdown("### 詳細データ")

    # DataFrameに変換
    creature_data = []
    for creature, data in creature_stats.items():
        creature_data.append({
            "クリーチャー": creature,
            "バトル数": data["battles"],
            "勝利": data["wins"],
            "敗北": data["losses"],
            "引き分け": data["draws"],
            "勝率": f"{data['win_rate'] * 100:.1f}%",
        })

    df_creatures = pd.DataFrame(creature_data)
    df_creatures = df_creatures.sort_values("勝率", ascending=False)
    st.dataframe(df_creatures, use_container_width=True, hide_index=True)

    # トップ3
    st.markdown("### 🏆 トップ3")
    sorted_creatures = sorted(
        creature_stats.items(),
        key=lambda x: x[1]["win_rate"],
        reverse=True
    )

    col1, col2, col3 = st.columns(3)

    for idx, (creature, data) in enumerate(sorted_creatures[:3]):
        with [col1, col2, col3][idx]:
            medal = ["🥇", "🥈", "🥉"][idx]
            st.markdown(f"### {medal} {creature}")
            st.metric("勝率", f"{data['win_rate'] * 100:.1f}%")
            st.markdown(f"{data['wins']}勝 {data['losses']}敗 {data['draws']}分")
else:
    st.info("クリーチャー別統計データがありません")

# ターン数分布
st.markdown("---")
st.markdown("## ⏱️ ターン数分析")

col1, col2 = st.columns([2, 1])

with col1:
    turn_dist_chart = create_turn_distribution_chart(logs)
    st.plotly_chart(turn_dist_chart, use_container_width=True)

with col2:
    st.markdown("### 統計")
    st.metric("平均ターン数", f"{stats['avg_turns']:.1f}")

    turn_counts = [log["total_turns"] for log in logs]
    st.metric("最大ターン数", max(turn_counts))
    st.metric("最小ターン数", min(turn_counts))

    st.markdown("### 考察")
    if stats["avg_turns"] < 5:
        st.info("💡 速攻型のバトルが多いです")
    elif stats["avg_turns"] > 10:
        st.info("💡 持久戦型のバトルが多いです")
    else:
        st.info("💡 バランスの取れたバトルです")

# ダメージ統計
st.markdown("---")
st.markdown("## 💥 ダメージ統計")

col1, col2 = st.columns([2, 1])

with col1:
    damage_chart = create_damage_stats_chart(logs)
    st.plotly_chart(damage_chart, use_container_width=True)

with col2:
    st.markdown("### 統計")
    st.metric("総ダメージ", f"{stats['total_damage']:,}")
    st.metric("平均ダメージ/バトル", f"{stats['avg_damage_per_battle']:.1f}")

    # ダメージ/ターン
    avg_damage_per_turn = stats['total_damage'] / (stats['avg_turns'] * stats['total_battles'])
    st.metric("平均ダメージ/ターン", f"{avg_damage_per_turn:.1f}")

    st.markdown("### 考察")
    if stats['avg_damage_per_battle'] > 200:
        st.info("💡 高火力のバトルが多いです")
    elif stats['avg_damage_per_battle'] < 100:
        st.info("💡 低火力のバトルが多いです")
    else:
        st.info("💡 標準的な火力です")

# タイプ別統計
st.markdown("---")
st.markdown("## 🔥 タイプ別統計")

type_stats = stats["type_stats"]

if type_stats and len(type_stats) > 1:
    # タイプ別データ
    type_data = []
    for type_, data in type_stats.items():
        if type_ != "unknown":
            type_data.append({
                "タイプ": type_.capitalize(),
                "バトル数": data["battles"],
                "勝利": data["wins"],
                "敗北": data["losses"],
                "引き分け": data["draws"],
                "勝率": f"{data['win_rate'] * 100:.1f}%",
            })

    df_types = pd.DataFrame(type_data)
    df_types = df_types.sort_values("勝率", ascending=False)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.dataframe(df_types, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("### 🏆 最強タイプ")
        if not df_types.empty:
            top_type = df_types.iloc[0]
            st.metric(top_type["タイプ"], top_type["勝率"])
            st.markdown(f"{top_type['勝利']}勝 {top_type['敗北']}敗")

        st.markdown("### 考察")
        st.info("💡 タイプ相性が戦況に影響しています")
else:
    st.info("タイプ別統計データが不足しています（より多くのバトルが必要）")

# データエクスポート
st.markdown("---")
st.markdown("## 📥 データエクスポート")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### クリーチャー別統計")
    if creature_stats:
        csv_creatures = pd.DataFrame([
            {
                "creature": k,
                "battles": v["battles"],
                "wins": v["wins"],
                "losses": v["losses"],
                "draws": v["draws"],
                "win_rate": v["win_rate"],
            }
            for k, v in creature_stats.items()
        ])
        csv_str = csv_creatures.to_csv(index=False)
        st.download_button(
            label="📥 CSVダウンロード",
            data=csv_str,
            file_name="creature_stats.csv",
            mime="text/csv",
        )

with col2:
    st.markdown("### タイプ別統計")
    if type_stats:
        csv_types = pd.DataFrame([
            {
                "type": k,
                "battles": v["battles"],
                "wins": v["wins"],
                "losses": v["losses"],
                "draws": v["draws"],
                "win_rate": v["win_rate"],
            }
            for k, v in type_stats.items()
        ])
        csv_str = csv_types.to_csv(index=False)
        st.download_button(
            label="📥 CSVダウンロード",
            data=csv_str,
            file_name="type_stats.csv",
            mime="text/csv",
        )

# サイドバー
with st.sidebar:
    st.markdown("## 📊 統計・分析")

    st.markdown("### 📈 データソース")
    st.info(f"""
    **ローカルデータ**

    バトル数: {len(logs)}件

    Phase 6でBigQuery連携を追加予定
    """)

    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.success("""
    - **全体統計**: 勝率とターン数を確認
    - **クリーチャー別**: 最強クリーチャーを発見
    - **ダメージ統計**: 火力傾向を分析
    - **CSVエクスポート**: データを保存
    """)

    st.markdown("---")
    st.markdown("### 🔮 Coming Soon")
    st.warning("""
    **Phase 6で追加予定:**
    - BigQueryからのデータ取得
    - 長期的なトレンド分析
    - より詳細な統計情報
    """)
