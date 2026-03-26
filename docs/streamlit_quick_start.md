# Streamlit クイックスタートガイド

Phase 6で実装するStreamlit UIの簡単なガイド

## 🚀 インストール（Phase 6で実施）

```bash
# Streamlit関連パッケージをインストール
pip install -e ".[streamlit]"

# または全部入り
pip install -e ".[dev,streamlit]"
```

## 📦 インストールされるパッケージ

- **streamlit** (>=1.35.0) - メインフレームワーク
- **plotly** (>=5.22.0) - インタラクティブグラフ
- **pandas** (>=2.2.0) - データ処理

## 🎮 使い方

### 1. アプリを起動

```bash
streamlit run streamlit_app/app.py
```

ブラウザで `http://localhost:8501` が自動的に開きます。

### 2. ページを切り替え

サイドバーから以下のページを選択：
- 🎮 **Battle** - バトル実行
- 📊 **Analytics** - 統計分析
- 📚 **Master Data** - マスタデータ参照
- 📜 **Battle Logs** - ログビューワー

### 3. バトル実行

1. サイドバーでクリーチャーを2体選択
2. 「バトル開始」ボタンをクリック
3. 結果とHP推移グラフを表示

## 🎨 カスタマイズ

### テーマ変更

`.streamlit/config.toml` を編集：

```toml
[theme]
primaryColor = "#FF4B4B"  # メインカラー
backgroundColor = "#0E1117"  # 背景色
```

### ポート変更

```bash
streamlit run streamlit_app/app.py --server.port 8080
```

## 📝 開発のポイント

### ホットリロード

ファイルを保存すると自動的にブラウザが再読み込みされます。

### デバッグ

```python
import streamlit as st

# デバッグ情報を表示
st.write("Debug:", variable)
st.json(data)
```

### セッション管理

```python
# セッションステートに保存
if 'battle_count' not in st.session_state:
    st.session_state.battle_count = 0

st.session_state.battle_count += 1
```

## 🔗 既存コードとの連携

既存のコードはそのまま使えます：

```python
# Streamlitアプリ内
from creature_duel.infrastructure.data.loader import MasterDataLoader
from creature_duel.battle.battle_engine import BattleEngine

# ローダー初期化
loader = MasterDataLoader()

# クリーチャー取得
creature = loader.get_creature("charizard")

# バトル実行
engine = BattleEngine()
result = engine.execute_battle(creature1, creature2)

# 結果を表示
st.success(f"勝者: {result['winner']}")
```

## 📚 参考リンク

- [Streamlit公式ドキュメント](https://docs.streamlit.io/)
- [Streamlit APIリファレンス](https://docs.streamlit.io/library/api-reference)
- [Plotly Python](https://plotly.com/python/)

## 💡 Tips

### パフォーマンス

```python
# キャッシュを使う
@st.cache_data
def load_data():
    return loader.load_creatures()
```

### レイアウト

```python
# カラム分割
col1, col2 = st.columns(2)

with col1:
    st.write("左側")

with col2:
    st.write("右側")
```

### プログレスバー

```python
with st.spinner("処理中..."):
    # 重い処理
    result = engine.execute_battle(c1, c2)
```

---

Phase 6で実装する際に、このガイドを参照してください！
