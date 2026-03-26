# Streamlit統合計画

**Phase 6: Streamlit UI**の詳細実装計画

## 🎯 目的

- バトルシミュレーションのWebベースUI提供
- データ分析・可視化の実現
- デモ・プレゼンテーション用のツール
- BigQueryデータの可視化

---

## 📦 必要な追加ライブラリ

### pyproject.toml への追加

```toml
dependencies = [
    "pydantic>=2.9.0",
    "google-cloud-bigquery>=3.25.0",
    "google-auth>=2.34.0",
    "streamlit>=1.35.0",          # 追加
    "plotly>=5.22.0",             # 追加（グラフ）
    "pandas>=2.2.0",              # 追加（データ処理）
]
```

---

## 📁 ディレクトリ構造

```
creature-duel/
├── streamlit_app/
│   ├── app.py                      # メインアプリ（ホーム）
│   │
│   ├── pages/                      # マルチページアプリ
│   │   ├── 1_🎮_battle.py         # バトル実行ページ
│   │   ├── 2_📊_analytics.py      # 統計分析ページ
│   │   ├── 3_📚_master_data.py    # マスタデータブラウザ
│   │   └── 4_📜_battle_logs.py    # バトルログビューワー
│   │
│   ├── utils/                      # ヘルパー関数
│   │   ├── __init__.py
│   │   ├── visualization.py        # グラフ作成
│   │   ├── formatters.py          # データフォーマット
│   │   └── battle_helpers.py      # バトル関連ヘルパー
│   │
│   └── .streamlit/                 # Streamlit設定
│       └── config.toml             # テーマ設定等
│
└── src/creature_duel/              # 既存のコードはそのまま
```

---

## 🎨 画面設計

### 1. ホーム（app.py）

```python
import streamlit as st

st.set_page_config(
    page_title="Creature Duel",
    page_icon="⚔️",
    layout="wide"
)

st.title("⚔️ Creature Duel")
st.markdown("ポケモン風バトルシミュレーションシステム")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("総バトル数", "1,234")

with col2:
    st.metric("登録クリーチャー", "10")

with col3:
    st.metric("スキル数", "29")

st.info("左サイドバーからページを選択してください")
```

### 2. バトル実行ページ（1_🎮_battle.py）

#### レイアウト
- サイドバー: クリーチャー選択
- メインエリア: バトル実行ボタン、結果表示
- グラフエリア: HP推移グラフ

#### 機能
```python
import streamlit as st
from creature_duel.infrastructure.data.loader import MasterDataLoader
from creature_duel.battle.battle_engine import BattleEngine

st.title("🎮 バトル実行")

loader = MasterDataLoader()

# サイドバー: クリーチャー選択
with st.sidebar:
    st.header("Player 1")
    creature1_id = st.selectbox(
        "クリーチャー選択",
        loader.list_creatures(),
        key="p1"
    )

    st.header("Player 2")
    creature2_id = st.selectbox(
        "クリーチャー選択",
        loader.list_creatures(),
        key="p2"
    )

# メインエリア
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Player 1: {creature1_id}")
    creature1 = loader.get_creature(creature1_id)
    st.write(f"HP: {creature1.base_stats.hp}")
    # 詳細情報表示

with col2:
    st.subheader(f"Player 2: {creature2_id}")
    creature2 = loader.get_creature(creature2_id)
    st.write(f"HP: {creature2.base_stats.hp}")
    # 詳細情報表示

# バトル実行
if st.button("⚔️ バトル開始", type="primary", use_container_width=True):
    with st.spinner("バトル実行中..."):
        engine = BattleEngine()
        result = engine.execute_battle(creature1, creature2)

    # 結果表示
    if result['winner'] == 'player1':
        st.success(f"🏆 Player 1 ({creature1.name}) の勝利！")
    else:
        st.success(f"🏆 Player 2 ({creature2.name}) の勝利！")

    st.metric("総ターン数", result['total_turns'])

    # ログ表示
    with st.expander("📜 バトルログを見る"):
        for log in result['logs']:
            st.json(log)

    # グラフ表示
    st.subheader("HP推移")
    # Plotlyでグラフ作成（後述）
```

### 3. 統計分析ページ（2_📊_analytics.py）

#### 機能
- BigQueryからデータ取得
- 勝率分析（クリーチャー別、タイプ別）
- ダメージ統計
- 平均ターン数

```python
import streamlit as st
import plotly.express as px
import pandas as pd

st.title("📊 統計分析")

# タブ分け
tab1, tab2, tab3 = st.tabs(["勝率分析", "ダメージ統計", "ターン分析"])

with tab1:
    st.subheader("クリーチャー別勝率")
    # BigQueryからデータ取得（仮のデータで説明）
    data = {
        'creature': ['Charizard', 'Blastoise', 'Pikachu'],
        'win_rate': [0.65, 0.58, 0.42]
    }
    df = pd.DataFrame(data)

    fig = px.bar(df, x='creature', y='win_rate',
                 title="クリーチャー別勝率")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("平均ダメージ")
    # グラフ表示

with tab3:
    st.subheader("平均ターン数")
    # グラフ表示
```

### 4. マスタデータブラウザ（3_📚_master_data.py）

#### 機能
- クリーチャー一覧（フィルタリング可能）
- スキル詳細表示
- タイプ相性表

```python
import streamlit as st
import pandas as pd

st.title("📚 マスタデータブラウザ")

loader = MasterDataLoader()

# タブ分け
tab1, tab2, tab3 = st.tabs(["クリーチャー", "スキル", "タイプ相性"])

with tab1:
    st.subheader("クリーチャー一覧")

    # フィルター
    type_filter = st.multiselect(
        "タイプで絞り込み",
        ["fire", "water", "grass", "electric", "ice", "normal"]
    )

    # テーブル表示
    creatures = loader.load_creatures()
    # DataFrameに変換して表示

with tab2:
    st.subheader("スキル一覧")
    # スキルテーブル

with tab3:
    st.subheader("タイプ相性表")
    # ヒートマップで表示
```

### 5. バトルログビューワー（4_📜_battle_logs.py）

#### 機能
- 過去のバトルログ検索
- ログの詳細表示
- 再生機能（アニメーション）

---

## 🛠️ ヘルパー関数

### visualization.py

```python
"""グラフ作成のヘルパー関数"""

import plotly.graph_objects as go
from typing import List, Dict

def create_hp_timeline(logs: List[Dict]) -> go.Figure:
    """
    HP推移のグラフを作成

    Args:
        logs: バトルログ

    Returns:
        Plotlyのグラフオブジェクト
    """
    # ターン毎のHPを抽出
    turns = []
    player1_hp = []
    player2_hp = []

    for log in logs:
        if log['event_type'] == 'turn_start':
            turns.append(log.get('turn', 0))
            player1_hp.append(log.get('player1_hp', 0))
            player2_hp.append(log.get('player2_hp', 0))

    # グラフ作成
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=turns,
        y=player1_hp,
        mode='lines+markers',
        name='Player 1',
        line=dict(color='red', width=3)
    ))

    fig.add_trace(go.Scatter(
        x=turns,
        y=player2_hp,
        mode='lines+markers',
        name='Player 2',
        line=dict(color='blue', width=3)
    ))

    fig.update_layout(
        title="HP推移",
        xaxis_title="ターン",
        yaxis_title="HP",
        hovermode='x unified'
    )

    return fig


def create_type_effectiveness_heatmap(type_chart: Dict) -> go.Figure:
    """タイプ相性のヒートマップを作成"""
    # 実装
    pass


def create_damage_distribution(damages: List[int]) -> go.Figure:
    """ダメージ分布のヒストグラムを作成"""
    # 実装
    pass
```

### formatters.py

```python
"""データフォーマット用のヘルパー関数"""

from creature_duel.domain.entities.creature import Creature

def format_creature_info(creature: Creature) -> str:
    """
    クリーチャー情報を整形

    Returns:
        Markdown形式の文字列
    """
    info = f"""
    ### {creature.name}

    **タイプ**: {', '.join([t.value for t in creature.types])}

    **ステータス**:
    - HP: {creature.base_stats.hp}
    - Attack: {creature.base_stats.attack}
    - Defence: {creature.base_stats.defence}
    - Sp.Attack: {creature.base_stats.sp_attack}
    - Sp.Defence: {creature.base_stats.sp_defence}
    - Speed: {creature.base_stats.speed}

    **技**:
    {', '.join([s.name for s in creature.skills])}
    """
    return info
```

---

## ⚙️ Streamlit設定

### .streamlit/config.toml

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
```

---

## 🚀 起動方法

### 開発環境

```bash
# 依存関係インストール（初回のみ）
pip install -e ".[dev]"

# Streamlitアプリ起動
streamlit run streamlit_app/app.py

# ブラウザで http://localhost:8501 が自動で開く
```

### 本番環境（将来）

```bash
# Docker化（将来）
docker build -t creature-duel-ui .
docker run -p 8501:8501 creature-duel-ui

# Cloud Runへのデプロイ（将来）
gcloud run deploy creature-duel --source .
```

---

## ✅ 既存コードへの変更

### **変更不要！**

既存のコードは**一切変更不要**です。Streamlitは以下のように既存コードをそのまま呼び出します：

```python
# 既存のコードをそのまま使用
from creature_duel.infrastructure.data.loader import MasterDataLoader
from creature_duel.battle.battle_engine import BattleEngine

loader = MasterDataLoader()
engine = BattleEngine()
```

### オプションの追加（推奨）

既存コードに影響を与えない追加：

```python
# streamlit_app/utils/battle_helpers.py（新規作成）

def format_battle_result_for_ui(result: dict) -> dict:
    """バトル結果をUI表示用に整形"""
    # 追加のフォーマット処理
    return formatted_result
```

---

## 📊 実装の優先順位

### フェーズ1（Week 8前半）- MVP
1. ✅ pyproject.toml更新
2. ✅ 基本的なホーム画面
3. ✅ バトル実行ページ（シンプル版）
4. ✅ 結果表示

### フェーズ2（Week 8後半）- 可視化
1. ✅ HP推移グラフ
2. ✅ ログビューワー
3. ✅ マスタデータブラウザ

### フェーズ3（Week 9）- 分析機能
1. ✅ BigQuery連携
2. ✅ 統計分析ページ
3. ✅ 高度なグラフ

---

## 🎓 学習リソース

- [Streamlit公式ドキュメント](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)
- [Streamlit Gallery](https://streamlit.io/gallery) - 参考例

---

## 📝 メモ

### Streamlitの利点
- ✅ Pythonだけで完結
- ✅ リアルタイム再読み込み（開発効率UP）
- ✅ 既存コードをそのまま使える
- ✅ デプロイが簡単
- ✅ 無料でStreamlit Cloudにホスティング可能

### 注意点
- ステートレス（セッション管理が必要）
- 大量データには不向き（→BigQueryで集計）
- カスタムCSSは限定的

---

これでStreamlit統合の準備が整いました！🎉
