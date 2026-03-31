"""バトルログビューワー"""

import streamlit as st
import sys
from pathlib import Path
import json
from datetime import datetime

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.battle_runner import BattleRunner
from utils.formatters import format_battle_log_event
from utils.visualization import (
    create_hp_timeline_chart,
    create_damage_breakdown_chart,
)

# ページ設定
st.set_page_config(page_title="Battle Logs", page_icon="📜", layout="wide")

# タイトル
st.title("📜 バトルログビューワー")
st.markdown("過去のバトルログを閲覧・分析できます")

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

# サマリー
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("総バトル数", len(logs))

with col2:
    player1_wins = sum(1 for log in logs if log["winner"] == "player1")
    st.metric("Player 1 勝利", player1_wins)

with col3:
    player2_wins = sum(1 for log in logs if log["winner"] == "player2")
    st.metric("Player 2 勝利", player2_wins)

with col4:
    draws = sum(1 for log in logs if log["winner"] == "draw")
    st.metric("引き分け", draws)

# ログ一覧
st.markdown("---")
st.markdown("## 📋 バトルログ一覧")

# ソートとフィルター
col1, col2, col3 = st.columns(3)

with col1:
    sort_by = st.selectbox(
        "並び替え",
        ["新しい順", "古い順", "ターン数（多い）", "ターン数（少ない）"],
    )

with col2:
    winner_filter = st.selectbox(
        "勝者でフィルター",
        ["すべて", "Player 1", "Player 2", "引き分け"],
    )

with col3:
    search_creature = st.text_input("🔍 クリーチャー名で検索", "")

# フィルタリング
filtered_logs = logs

if winner_filter != "すべて":
    winner_map = {"Player 1": "player1", "Player 2": "player2", "引き分け": "draw"}
    filtered_logs = [
        log for log in filtered_logs
        if log["winner"] == winner_map[winner_filter]
    ]

if search_creature:
    filtered_logs = [
        log for log in filtered_logs
        if search_creature.lower() in log["final_state"]["player1"]["creature"].lower()
        or search_creature.lower() in log["final_state"]["player2"]["creature"].lower()
    ]

# ソート
if sort_by == "新しい順":
    filtered_logs = sorted(filtered_logs, key=lambda x: x["filename"], reverse=True)
elif sort_by == "古い順":
    filtered_logs = sorted(filtered_logs, key=lambda x: x["filename"])
elif sort_by == "ターン数（多い）":
    filtered_logs = sorted(filtered_logs, key=lambda x: x["total_turns"], reverse=True)
elif sort_by == "ターン数（少ない）":
    filtered_logs = sorted(filtered_logs, key=lambda x: x["total_turns"])

# 表示
st.markdown(f"**表示中**: {len(filtered_logs)} / {len(logs)} 件")

for idx, log in enumerate(filtered_logs):
    # ファイル名から日時を抽出
    filename = log["filename"]
    # battle_20230330_120000_player1.json -> 2023/03/30 12:00:00
    try:
        parts = filename.split("_")
        date_str = parts[1]  # 20230330
        time_str = parts[2]  # 120000
        date = datetime.strptime(date_str, "%Y%m%d").strftime("%Y/%m/%d")
        time = datetime.strptime(time_str, "%H%M%S").strftime("%H:%M:%S")
        datetime_str = f"{date} {time}"
    except:
        datetime_str = filename

    # 対戦カード
    p1_creature = log["final_state"]["player1"]["creature"]
    p2_creature = log["final_state"]["player2"]["creature"]
    matchup = f"{p1_creature} vs {p2_creature}"

    # 勝者
    winner = log["winner"]
    if winner == "draw":
        winner_str = "🤝 引き分け"
    elif winner == "player1":
        winner_str = f"🎉 {p1_creature} の勝利"
    else:
        winner_str = f"🎉 {p2_creature} の勝利"

    # ターン数
    turns = log["total_turns"]

    with st.expander(f"**#{len(filtered_logs) - idx}** {matchup} - {winner_str} ({turns}ターン) - {datetime_str}"):
        # タブで詳細を表示
        tab1, tab2, tab3 = st.tabs(["📊 サマリー", "📜 ログ", "📄 JSON"])

        with tab1:
            # サマリー
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Player 1")
                p1_state = log["final_state"]["player1"]
                st.markdown(f"**クリーチャー**: {p1_state['creature']}")
                st.markdown(f"**HP**: {p1_state['hp']}")
                st.markdown(f"**状態**: {'💀 倒れた' if p1_state['fainted'] else '✅ 生存'}")

            with col2:
                st.markdown("### Player 2")
                p2_state = log["final_state"]["player2"]
                st.markdown(f"**クリーチャー**: {p2_state['creature']}")
                st.markdown(f"**HP**: {p2_state['hp']}")
                st.markdown(f"**状態**: {'💀 倒れた' if p2_state['fainted'] else '✅ 生存'}")

            # グラフ
            col1, col2 = st.columns(2)

            with col1:
                hp_chart = create_hp_timeline_chart(log)
                st.plotly_chart(hp_chart, use_container_width=True)

            with col2:
                damage_chart = create_damage_breakdown_chart(log)
                st.plotly_chart(damage_chart, use_container_width=True)

        with tab2:
            # ログをターン毎にグループ化
            logs_by_turn = {}
            for event in log["logs"]:
                turn = event.get("turn", 0)
                if turn not in logs_by_turn:
                    logs_by_turn[turn] = []
                logs_by_turn[turn].append(event)

            # ターン毎に表示
            for turn in sorted(logs_by_turn.keys()):
                st.markdown(f"**ターン {turn}**")
                for event in logs_by_turn[turn]:
                    event_text = format_battle_log_event(event)
                    st.markdown(f"- {event_text}")
                st.markdown("")

        with tab3:
            # JSON表示
            st.json(log)

            # ダウンロードボタン
            json_str = json.dumps(log, indent=2, ensure_ascii=False)
            st.download_button(
                label="📥 JSONをダウンロード",
                data=json_str,
                file_name=filename,
                mime="application/json",
            )

# サイドバー
with st.sidebar:
    st.markdown("## 📜 バトルログ")

    st.markdown("### 📊 統計")
    if logs:
        avg_turns = sum(log["total_turns"] for log in logs) / len(logs)
        max_turns = max(log["total_turns"] for log in logs)
        min_turns = min(log["total_turns"] for log in logs)

        st.metric("平均ターン数", f"{avg_turns:.1f}")
        st.metric("最大ターン数", max_turns)
        st.metric("最小ターン数", min_turns)

    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.info("""
    - **ソート**: 新しい順、ターン数で並び替え
    - **フィルター**: 勝者やクリーチャーで絞り込み
    - **詳細**: 展開してグラフやログを確認
    - **ダウンロード**: JSONタブからダウンロード
    """)

    st.markdown("---")
    st.markdown("### ⚠️ データ管理")
    st.warning("""
    バトルログは `battle_logs/` ディレクトリに保存されます。

    削除する場合は手動でファイルを削除してください。
    """)
