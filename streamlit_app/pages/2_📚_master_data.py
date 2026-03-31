"""マスタデータブラウザ"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.formatters import (
    format_type,
    format_skill_category,
    format_pp,
    format_percentage,
    format_ability_effect,
    get_type_color,
)
from utils.visualization import create_type_matchup_heatmap
from creature_duel.infrastructure.data.loader import MasterDataLoader

# ページ設定
st.set_page_config(page_title="Master Data", page_icon="📚", layout="wide")

# タイトル
st.title("📚 マスタデータブラウザ")
st.markdown("クリーチャー、技、特性、タイプ相性のデータを閲覧できます")

# 初期化
if "loader" not in st.session_state:
    st.session_state.loader = MasterDataLoader()

loader = st.session_state.loader

# タブ
tab1, tab2, tab3, tab4 = st.tabs(["🐉 クリーチャー", "⚔️ 技", "✨ 特性", "🔄 タイプ相性"])

# クリーチャータブ
with tab1:
    st.markdown("## 🐉 クリーチャー一覧")

    creature_names = loader.list_creatures()

    # 検索とフィルター
    col1, col2 = st.columns([2, 1])

    with col1:
        search_query = st.text_input("🔍 クリーチャー名で検索", "")

    with col2:
        type_filter = st.selectbox(
            "タイプでフィルター",
            ["すべて", "fire", "water", "grass", "electric", "ice", "normal"],
        )

    # フィルタリング
    filtered_creatures = creature_names

    if search_query:
        filtered_creatures = [
            name for name in filtered_creatures
            if search_query.lower() in name.lower()
        ]

    if type_filter != "すべて":
        # タイプでフィルターする場合、各クリーチャーをロードして確認
        filtered_by_type = []
        for name in filtered_creatures:
            creature = loader.get_creature(name)
            if any(t.value == type_filter for t in creature.types):
                filtered_by_type.append(name)
        filtered_creatures = filtered_by_type

    # クリーチャー表示
    st.markdown(f"**表示中**: {len(filtered_creatures)} / {len(creature_names)} 体")

    for creature_name in filtered_creatures:
        creature = loader.get_creature(creature_name)

        with st.expander(f"**{creature.name}** - {', '.join([t.value.capitalize() for t in creature.types])}"):
            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown("### 基本情報")
                st.markdown(f"**名前**: {creature.name}")
                st.markdown(f"**タイプ**: {', '.join([format_type(t) for t in creature.types])}")
                st.markdown(f"**特性**: {creature.ability if creature.ability else 'なし'}")

                st.markdown("### ステータス")
                stats = creature.base_stats
                st.metric("HP", stats.hp)
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("攻撃", int(stats.attack))
                    st.metric("特攻", int(stats.sp_attack))
                    st.metric("素早さ", int(stats.speed))
                with col_b:
                    st.metric("防御", int(stats.defence))
                    st.metric("特防", int(stats.sp_defence))

            with col2:
                st.markdown("### 覚える技")

                # 技をDataFrameに変換
                skills_data = []
                for skill in creature.skills:
                    skills_data.append({
                        "技名": skill.name,
                        "タイプ": skill.type.value.capitalize(),
                        "分類": skill.category.value.capitalize(),
                        "威力": skill.power if skill.power > 0 else "-",
                        "命中": f"{int(skill.accuracy * 100)}%",
                        "PP": f"{skill.current_pp}/{skill.max_pp}",
                    })

                df = pd.DataFrame(skills_data)
                st.dataframe(df, use_container_width=True, hide_index=True)

# 技タブ
with tab2:
    st.markdown("## ⚔️ 技一覧")

    skill_names = loader.list_skills()

    # 検索とフィルター
    col1, col2, col3 = st.columns(3)

    with col1:
        search_query_skill = st.text_input("🔍 技名で検索", "", key="skill_search")

    with col2:
        type_filter_skill = st.selectbox(
            "タイプでフィルター",
            ["すべて", "fire", "water", "grass", "electric", "ice", "normal"],
            key="skill_type_filter",
        )

    with col3:
        category_filter = st.selectbox(
            "分類でフィルター",
            ["すべて", "physical", "special", "status"],
        )

    # フィルタリング
    filtered_skills = skill_names

    if search_query_skill:
        filtered_skills = [
            name for name in filtered_skills
            if search_query_skill.lower() in name.lower()
        ]

    if type_filter_skill != "すべて" or category_filter != "すべて":
        # タイプまたは分類でフィルターする場合、各技をロードして確認
        filtered_by_attrs = []
        for name in filtered_skills:
            skill = loader.get_skill(name)
            type_match = type_filter_skill == "すべて" or skill.type.value == type_filter_skill
            category_match = category_filter == "すべて" or skill.category.value == category_filter
            if type_match and category_match:
                filtered_by_attrs.append(name)
        filtered_skills = filtered_by_attrs

    # 技表示
    st.markdown(f"**表示中**: {len(filtered_skills)} / {len(skill_names)} 技")

    # DataFrameで一覧表示
    skills_data = []
    for skill_name in filtered_skills:
        skill = loader.get_skill(skill_name)

        # Effects情報
        effects_str = ""
        if skill.effects:
            effect_descriptions = []
            for effect in skill.effects:
                if effect["type"] == "ailment":
                    effect_descriptions.append(
                        f"{effect['ailment']} ({int(effect['chance']*100)}%)"
                    )
                elif effect["type"] == "stat_change":
                    effect_descriptions.append(
                        f"{effect['stat']} {effect['stages']:+d}"
                    )
            effects_str = ", ".join(effect_descriptions)

        skills_data.append({
            "技名": skill.name,
            "タイプ": skill.type.value.capitalize(),
            "分類": skill.category.value.capitalize(),
            "威力": skill.power if skill.power > 0 else "-",
            "命中": f"{int(skill.accuracy * 100)}%",
            "PP": skill.max_pp,
            "追加効果": effects_str if effects_str else "-",
        })

    df_skills = pd.DataFrame(skills_data)
    st.dataframe(df_skills, use_container_width=True, hide_index=True, height=600)

# 特性タブ
with tab3:
    st.markdown("## ✨ 特性一覧")

    ability_ids = loader.list_abilities()

    # 特性表示
    st.markdown(f"**登録数**: {len(ability_ids)} 種類")

    for ability_id in ability_ids:
        ability = loader.get_ability(ability_id)

        with st.expander(f"**{ability.name}**"):
            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown("### 基本情報")
                st.markdown(f"**ID**: {ability.id}")
                st.markdown(f"**名前**: {ability.name}")
                st.markdown(f"**発動**: {ability.trigger.value}")

            with col2:
                st.markdown("### 効果")
                st.markdown(f"**説明**: {ability.description}")
                st.markdown(f"**効果**: {format_ability_effect(ability)}")

                if ability.effect_config:
                    st.markdown("**詳細設定**:")
                    st.json(ability.effect_config)

# タイプ相性タブ
with tab4:
    st.markdown("## 🔄 タイプ相性表")

    # タイプ相性表を読み込み
    type_chart = loader.load_type_chart()

    # ヒートマップ表示
    st.markdown("### 相性マップ（攻撃側 × 防御側）")
    st.markdown("**読み方**: 行（攻撃側）のタイプが、列（防御側）のタイプに対してどれだけ効果的か")

    heatmap = create_type_matchup_heatmap(type_chart)
    st.plotly_chart(heatmap, use_container_width=True)

    # 相性解説
    st.markdown("---")
    st.markdown("### 📖 相性解説")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **効果抜群（2.0×〜4.0×）**
        - 🔥 炎 → 🌿 草、❄️ 氷
        - 💧 水 → 🔥 炎
        - 🌿 草 → 💧 水
        - ⚡ 電気 → 💧 水
        - ❄️ 氷 → 🌿 草
        """)

    with col2:
        st.markdown("""
        **効果いまひとつ（0.5×〜0.25×）**
        - 🔥 炎 → 💧 水、🔥 炎
        - 💧 水 → 🌿 草、💧 水
        - 🌿 草 → 🔥 炎、🌿 草
        - ❄️ 氷 → 💧 水、❄️ 氷
        """)

    # インタラクティブ相性チェック
    st.markdown("---")
    st.markdown("### 🎯 相性チェッカー")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        attack_type = st.selectbox(
            "攻撃側のタイプ",
            list(type_chart.keys()),
            format_func=lambda x: x.capitalize(),
        )

    with col2:
        defend_type = st.selectbox(
            "防御側のタイプ",
            list(type_chart.keys()),
            format_func=lambda x: x.capitalize(),
        )

    with col3:
        effectiveness = type_chart[attack_type][defend_type]
        st.metric(
            "相性倍率",
            f"×{effectiveness}",
            delta="効果抜群" if effectiveness > 1.0 else ("効果いまひとつ" if effectiveness < 1.0 else "通常"),
        )

# サイドバー
with st.sidebar:
    st.markdown("## 📚 マスタデータ")

    st.markdown("### 📊 データ統計")
    creatures_count = len(loader.list_creatures())
    skills_count = len(loader.list_skills())
    abilities_count = len(loader.list_abilities())

    st.metric("クリーチャー", f"{creatures_count}体")
    st.metric("技", f"{skills_count}種類")
    st.metric("特性", f"{abilities_count}種類")
    st.metric("タイプ", "6種類")

    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.info("""
    - **クリーチャー**: 展開して詳細を確認
    - **技**: 追加効果をチェック
    - **特性**: 発動条件を確認
    - **タイプ相性**: ヒートマップで一目瞭然
    """)
