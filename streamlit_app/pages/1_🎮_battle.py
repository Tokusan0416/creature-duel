"""バトル実行ページ"""

import streamlit as st
import sys
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.battle_runner import BattleRunner
from utils.formatters import (
    format_creature_name,
    format_hp,
    format_battle_log_event,
    get_hp_color,
)
from utils.visualization import (
    create_hp_timeline_chart,
    create_damage_breakdown_chart,
)
from creature_duel.infrastructure.data.loader import MasterDataLoader

# ページ設定
st.set_page_config(page_title="Battle", page_icon="🎮", layout="wide")

# タイトル
st.title("🎮 バトル実行")
st.markdown("2体のクリーチャーを選んでバトルを開始しましょう！")

# 初期化
if "battle_runner" not in st.session_state:
    st.session_state.battle_runner = BattleRunner()
    st.session_state.loader = MasterDataLoader()

battle_runner = st.session_state.battle_runner
loader = st.session_state.loader

# クリーチャーリストを取得
creature_names = loader.list_creatures()

# クリーチャー選択UI
st.markdown("---")
st.markdown("## ⚔️ クリーチャー選択")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👤 Player 1")
    player1_creature = st.selectbox(
        "クリーチャーを選択",
        creature_names,
        key="player1",
        index=0,
    )

    # クリーチャー情報表示
    if player1_creature:
        creature = loader.get_creature(player1_creature)
        st.markdown(f"**名前**: {creature.name}")
        st.markdown(f"**タイプ**: {', '.join([t.value.capitalize() for t in creature.types])}")
        st.markdown(f"**HP**: {creature.base_stats.hp}")
        st.markdown(f"**特性**: {creature.ability if creature.ability else 'なし'}")

        # スキル一覧
        st.markdown("**技**:")
        for skill in creature.skills:
            st.markdown(f"- {skill.name} ({skill.type.value}/{skill.category.value})")

with col2:
    st.markdown("### 👤 Player 2")
    player2_creature = st.selectbox(
        "クリーチャーを選択",
        creature_names,
        key="player2",
        index=1 if len(creature_names) > 1 else 0,
    )

    # クリーチャー情報表示
    if player2_creature:
        creature = loader.get_creature(player2_creature)
        st.markdown(f"**名前**: {creature.name}")
        st.markdown(f"**タイプ**: {', '.join([t.value.capitalize() for t in creature.types])}")
        st.markdown(f"**HP**: {creature.base_stats.hp}")
        st.markdown(f"**特性**: {creature.ability if creature.ability else 'なし'}")

        # スキル一覧
        st.markdown("**技**:")
        for skill in creature.skills:
            st.markdown(f"- {skill.name} ({skill.type.value}/{skill.category.value})")

# バトル実行ボタン
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    battle_button = st.button(
        "⚔️ バトル開始",
        type="primary",
        use_container_width=True,
    )

# バトル実行
if battle_button:
    if player1_creature == player2_creature:
        st.warning("⚠️ 同じクリーチャーは選択できません！")
    else:
        with st.spinner("⚔️ バトル実行中..."):
            # バトル実行
            result = battle_runner.execute_battle(
                player1_creature,
                player2_creature,
                save_log=True,
            )

            # 結果を保存
            st.session_state.last_battle_result = result

        st.success("✅ バトル完了！")

# バトル結果表示
if "last_battle_result" in st.session_state:
    result = st.session_state.last_battle_result

    st.markdown("---")
    st.markdown("## 📊 バトル結果")

    # 勝者表示
    winner = result["winner"]
    if winner == "draw":
        st.info("🤝 引き分け")
    elif winner == "player1":
        st.success(f"🎉 {result['final_state']['player1']['creature']} の勝利！")
    else:
        st.success(f"🎉 {result['final_state']['player2']['creature']} の勝利！")

    # サマリー
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("総ターン数", result["total_turns"])

    with col2:
        st.metric("総イベント数", result["summary"]["total_events"])

    with col3:
        p1_hp = result["final_state"]["player1"]["hp"]
        p1_fainted = result["final_state"]["player1"]["fainted"]
        st.metric(
            "Player 1 HP",
            p1_hp,
            delta="倒れた" if p1_fainted else None,
            delta_color="off" if p1_fainted else "normal",
        )

    with col4:
        p2_hp = result["final_state"]["player2"]["hp"]
        p2_fainted = result["final_state"]["player2"]["fainted"]
        st.metric(
            "Player 2 HP",
            p2_hp,
            delta="倒れた" if p2_fainted else None,
            delta_color="off" if p2_fainted else "normal",
        )

    # グラフ表示
    st.markdown("---")
    st.markdown("### 📈 HP推移")

    col1, col2 = st.columns(2)

    with col1:
        # HP推移グラフ
        hp_chart = create_hp_timeline_chart(result)
        st.plotly_chart(hp_chart, use_container_width=True)

    with col2:
        # ダメージ内訳グラフ
        damage_chart = create_damage_breakdown_chart(result)
        st.plotly_chart(damage_chart, use_container_width=True)

    # バトルログ表示
    st.markdown("---")
    st.markdown("### 📜 バトルログ")

    # ログをターン毎にグループ化
    logs_by_turn = {}
    current_turn = 0

    for event in result["logs"]:
        turn = event.get("turn", 0)
        if turn not in logs_by_turn:
            logs_by_turn[turn] = []
        logs_by_turn[turn].append(event)

    # ターン毎に表示
    for turn in sorted(logs_by_turn.keys()):
        with st.expander(f"ターン {turn}", expanded=(turn <= 2)):
            for event in logs_by_turn[turn]:
                # イベントをフォーマット
                event_text = format_battle_log_event(event)

                # イベントタイプに応じてアイコンと色を変更
                event_type = event.get("event_type", "")

                if event_type == "battle_start":
                    st.info(event_text)
                elif event_type == "turn_start":
                    st.markdown(f"**{event_text}**")
                elif event_type == "skill_used":
                    st.markdown(event_text)
                elif event_type == "skill_missed":
                    st.warning(event_text)
                elif event_type == "damage_dealt":
                    if event.get("critical"):
                        st.error(f"💥 {event_text}")
                    else:
                        st.markdown(event_text)
                elif event_type == "effect_applied":
                    st.info(event_text)
                elif event_type == "ailment_damage":
                    st.warning(event_text)
                elif event_type == "cannot_move":
                    st.warning(event_text)
                elif event_type == "no_pp":
                    st.error(event_text)
                elif event_type == "creature_fainted":
                    st.error(event_text)
                elif event_type == "battle_end":
                    st.success(event_text)
                else:
                    st.text(event_text)

    # 最終ステータス
    st.markdown("---")
    st.markdown("### 🏁 最終ステータス")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Player 1")
        p1_state = result["final_state"]["player1"]
        st.markdown(f"**クリーチャー**: {p1_state['creature']}")
        st.markdown(f"**HP**: {p1_state['hp']}")
        st.markdown(f"**状態**: {'💀 倒れた' if p1_state['fainted'] else '✅ 生存'}")

    with col2:
        st.markdown("#### Player 2")
        p2_state = result["final_state"]["player2"]
        st.markdown(f"**クリーチャー**: {p2_state['creature']}")
        st.markdown(f"**HP**: {p2_state['hp']}")
        st.markdown(f"**状態**: {'💀 倒れた' if p2_state['fainted'] else '✅ 生存'}")

    # JSON出力
    st.markdown("---")
    st.markdown("### 📄 JSON出力")

    with st.expander("JSONデータを表示"):
        st.json(result)

# サイドバー
with st.sidebar:
    st.markdown("## 🎮 バトル実行")
    st.markdown("""
    ### 使い方
    1. Player 1とPlayer 2のクリーチャーを選択
    2. 「バトル開始」ボタンをクリック
    3. バトル結果とログを確認

    ### 機能
    - HP推移グラフ
    - ダメージ内訳
    - ターン毎のログ表示
    - JSON出力
    """)

    st.markdown("---")
    st.info("""
    💡 **Tips**

    - クリーチャーをクリックして詳細を確認
    - ターンをクリックして詳細ログを表示
    - JSON出力でデータ構造を確認
    """)
