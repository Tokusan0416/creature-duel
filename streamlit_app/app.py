"""Creature Duel - Streamlit UI メインアプリ"""

import streamlit as st
import sys
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# ページ設定
st.set_page_config(
    page_title="Creature Duel",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF6B6B;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #4ECDC4;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: #262730;
    }
    .feature-box h4 {
        color: #262730;
        margin-top: 0;
    }
    .feature-box ul {
        margin-bottom: 0;
    }
    .feature-box li {
        color: #262730;
        margin-bottom: 0.5rem;
    }
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.875rem;
    }
    .status-completed {
        background-color: #4CAF50;
        color: white;
    }
    .status-in-progress {
        background-color: #FF9800;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown('<div class="main-header">⚔️ Creature Duel ⚔️</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">ポケモン風バトルシミュレーションシステム</div>',
    unsafe_allow_html=True
)

# イントロダクション
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🎮 バトルシステム")
    st.markdown("""
    - 6タイプのクリーチャー
    - 29種類の技
    - 10種類の特性
    - タイプ相性・状態異常
    """)

with col2:
    st.markdown("### 📊 データ分析")
    st.markdown("""
    - バトルログ記録
    - 勝率分析
    - ダメージ統計
    - ターン数分析
    """)

with col3:
    st.markdown("### 🎨 インタラクティブUI")
    st.markdown("""
    - リアルタイムバトル表示
    - HP推移グラフ
    - マスタデータブラウザ
    - ログビューワー
    """)

# プロジェクトステータス
st.markdown("---")
st.markdown("## 📈 プロジェクトステータス")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="feature-box">
        <h4>✅ 実装済み機能（Phase 1-4）</h4>
        <ul>
            <li><b>ドメインモデル</b>: Creature, Skill, Ability, Player, StatusAilment</li>
            <li><b>バトルシステム</b>: ダメージ計算、命中判定、Effect適用、ターン処理</li>
            <li><b>計算ロジック</b>: タイプ相性、能力ランク、HP依存、状態異常補正</li>
            <li><b>テスト</b>: 103テスト（100%成功）</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-box">
        <h4>🎨 Phase 5（現在のPhase）</h4>
        <ul>
            <li><b>Streamlit UI</b>: バトル実行、マスタデータ閲覧、ログビューワー</li>
            <li><b>統計・分析</b>: ローカルデータの集計・可視化</li>
            <li><b>リアルタイム表示</b>: バトルログのアニメーション表示</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.metric(label="総テスト数", value="103", delta="100%")
    st.metric(label="完了Phase", value="4/7", delta="57%")
    st.metric(label="クリーチャー", value="10体")
    st.metric(label="技", value="29種類")
    st.metric(label="特性", value="10種類")

# クイックスタート
st.markdown("---")
st.markdown("## 🚀 クイックスタート")

tab1, tab2, tab3 = st.tabs(["💻 セットアップ", "🎮 使い方", "📚 機能一覧"])

with tab1:
    st.markdown("""
    ### インストール

    ```bash
    # 依存関係をインストール
    pip install -e ".[streamlit]"

    # Streamlitアプリを起動
    streamlit run streamlit_app/app.py
    ```

    ### 動作環境
    - Python 3.11+
    - Streamlit 1.35.0+
    - Plotly 5.22.0+
    """)

with tab2:
    st.markdown("""
    ### ページ一覧

    左サイドバーから各ページに移動できます：

    1. **🎮 Battle** - バトル実行ページ
       - 2体のクリーチャーを選択
       - バトル実行とログ表示
       - HP推移グラフ

    2. **📚 Master Data** - マスタデータブラウザ
       - クリーチャー一覧
       - 技一覧
       - 特性一覧
       - タイプ相性表

    3. **📜 Battle Logs** - バトルログビューワー
       - 過去のバトルログ表示
       - ターン毎の詳細
       - JSON出力

    4. **📊 Analytics** - 統計・分析
       - 勝率分析
       - ダメージ統計
       - ターン数分析
    """)

with tab3:
    st.markdown("""
    ### 実装機能

    #### バトルシステム
    - ✅ タイプ相性（6タイプ）
    - ✅ 状態異常（毒、火傷、氷、眠り、麻痺、混乱）
    - ✅ 特性システム（10種類）
    - ✅ 能力ランク（-6～+6段階）
    - ✅ HP依存補正
    - ✅ クリティカルヒット

    #### データ管理
    - ✅ JSONマスタデータ
    - ✅ バトルログ記録
    - ✅ ローカルストレージ

    #### UI機能
    - 🎨 リアルタイムバトル表示
    - 🎨 インタラクティブなグラフ
    - 🎨 データテーブル
    - 🎨 フィルタリング・検索
    """)

# フッター
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.875rem;">
    <p>Creature Duel v0.1.0 | Phase 5: Streamlit UI</p>
    <p>Built with Streamlit, Plotly, and Python</p>
</div>
""", unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.markdown("## 📋 ナビゲーション")
    st.markdown("""
    左側のページリストから
    各機能にアクセスできます。
    """)

    st.markdown("---")
    st.markdown("### 🎯 推奨順序")
    st.markdown("""
    1. **Master Data** - データを確認
    2. **Battle** - バトルを実行
    3. **Battle Logs** - ログを確認
    4. **Analytics** - 統計を分析
    """)

    st.markdown("---")
    st.markdown("### ℹ️ システム情報")
    st.info("""
    **Phase**: 5/7 (Streamlit UI)

    **Status**: 開発中

    **Tests**: 103/103 ✅
    """)
