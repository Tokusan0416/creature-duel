# Creature Duel

ポケモンに似た対戦バトルシミュレーションシステム。
バトルログをJSON形式で出力し、BigQueryに格納して分析・機械学習に活用できます。

## 🚀 クイックスタート

### インストール

```bash
# 依存関係のインストール
pip install -e ".[dev]"
```

### デモ実行

```bash
# シンプルなバトルを実行
python examples/simple_battle.py
```

### テスト実行

```bash
# 全テストを実行
pytest tests/ -v

# カバレッジ付きで実行
pytest tests/ --cov=src --cov-report=html
```

## 📁 プロジェクト構造

```
creature-duel/
├── src/creature_duel/       # メインソースコード
│   ├── domain/              # ドメインモデル
│   │   ├── entities/        # Creature, Skill等
│   │   ├── value_objects/   # Stats, Type等
│   │   └── enums/           # MoveCategory等
│   ├── application/         # アプリケーション層
│   │   └── services/        # DamageCalculator等
│   ├── battle/              # バトルエンジン
│   └── infrastructure/      # インフラ層
│
├── tests/                   # テストコード
├── examples/                # サンプルスクリプト
├── data/                    # マスタデータ
├── docs/                    # ドキュメント
└── ROADMAP.md              # 開発ロードマップ
```

## 📖 ドキュメント

- [DEVELOPMENT.md](DEVELOPMENT.md) - 詳細な仕様
- [ROADMAP.md](ROADMAP.md) - 開発ロードマップ

## 🎮 使用例

```python
from creature_duel import Creature, Skill, Stats, Type, MoveCategory, BattleEngine

# クリーチャーを作成
charizard = Creature(
    name="Charizard",
    types=[Type.FIRE],
    base_stats=Stats(hp=150, attack=84.0, defence=78.0,
                     sp_attack=109.0, sp_defence=85.0, speed=100.0),
    skills=[...]
)

# バトルを実行
engine = BattleEngine()
result = engine.execute_battle(charizard, blastoise)

print(f"勝者: {result['winner']}")
print(f"総ターン数: {result['total_turns']}")
```

## 🧪 開発状況

- ✅ Phase 1: 基礎構築（完了）
- ⚪ Phase 2: ドメインモデル拡張（未着手）
- ⚪ Phase 3: 計算ロジック実装（未着手）
- ⚪ Phase 4: バトルシステム実装（未着手）
- ⚪ Phase 5: BigQuery連携（未着手）
- ⚪ Phase 6: 🎨 Streamlit UI（未着手）
- ⚪ Phase 7: テスト・最適化・Double Battle（未着手）

詳細は [ROADMAP.md](ROADMAP.md) を参照してください。

## 🎨 Streamlit UI（Phase 6で実装予定）

WebベースのインタラクティブUIを提供します。

### インストール（Phase 6）

```bash
pip install -e ".[streamlit]"
```

### 起動方法

```bash
streamlit run streamlit_app/app.py
```

### 提供機能
- 🎮 **バトル実行** - クリーチャーを選択してバトル実行
- 📊 **統計分析** - BigQueryデータの可視化
- 📚 **マスタデータブラウザ** - クリーチャー・技の詳細表示
- 📜 **バトルログビューワー** - 過去のバトルログ閲覧

詳細は [docs/streamlit_integration_plan.md](docs/streamlit_integration_plan.md) を参照してください。

## 🛠️ 技術スタック

- **Python 3.11+**
- **Pydantic** - データバリデーション
- **Google Cloud BigQuery** - ログ保存
- **pytest** - テスト
- **black** / **ruff** - コード品質

## 📝 ライセンス

MIT License

## 📦 マスタデータ

プロジェクトには10体のクリーチャー、29種類の技、10種類の特性が含まれています。

### 利用可能なクリーチャー
- **Charizard** (Fire) - 特殊アタッカー
- **Blastoise** (Water) - バランス型
- **Venusaur** (Grass) - バランス型
- **Pikachu** (Electric) - 素早さ型
- **Lapras** (Water/Ice) - 耐久型
- **Jolteon** (Electric) - 素早さ特攻型
- **Snorlax** (Normal) - 物理耐久型
- **Flareon** (Fire) - 物理アタッカー
- **Vaporeon** (Water) - 特殊耐久型
- **Leafeon** (Grass) - 物理防御型

### マスタデータの使い方

```python
from creature_duel.infrastructure.data.loader import MasterDataLoader

# ローダーを初期化
loader = MasterDataLoader()

# クリーチャーを取得
charizard = loader.get_creature("charizard")
pikachu = loader.get_creature("pikachu")

# バトル実行
from creature_duel import BattleEngine
engine = BattleEngine()
result = engine.execute_battle(charizard, pikachu)
```

詳細は [docs/master_data_summary.md](docs/master_data_summary.md) を参照してください。
