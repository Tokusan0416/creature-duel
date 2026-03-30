# Creature Duel - アーキテクチャドキュメント

**最終更新**: 2026-03-27

## 📐 設計思想

Creature Duelは、ポケモンに似た対戦バトルシミュレーションシステムです。以下の設計思想に基づいて開発されています：

### コア原則
1. **クリーンアーキテクチャ**: ビジネスロジックとインフラの分離
2. **ドメイン駆動設計（DDD）**: ドメインモデルを中心とした設計
3. **テスタビリティ**: 高いテストカバレッジを維持
4. **データ駆動**: マスタデータをJSON/BigQueryで管理
5. **拡張性**: 新機能追加が容易な設計

---

## 🏗️ アーキテクチャ概要

### レイヤード構造

```
┌─────────────────────────────────────────────────────────┐
│                  Presentation Layer                      │
│              (streamlit_app/ - Phase 6)                  │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│                 Application Layer                        │
│  ┌──────────────┐     ┌──────────────┐                 │
│  │  Services    │     │  Use Cases   │                 │
│  │  (計算ロジック)│     │  (ビジネス  │                 │
│  │              │     │   フロー)     │                 │
│  └──────────────┘     └──────────────┘                 │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│                   Domain Layer                           │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐            │
│  │Entities  │  │Value      │  │ Enums     │            │
│  │(Creature,│  │Objects    │  │(Type,     │            │
│  │ Player)  │  │(Stats)    │  │ Category) │            │
│  └──────────┘  └──────────┘  └───────────┘            │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│                Infrastructure Layer                      │
│  ┌──────────────┐     ┌──────────────┐                 │
│  │  Data        │     │  BigQuery    │                 │
│  │  (JSON)      │     │  (Phase 5)   │                 │
│  └──────────────┘     └──────────────┘                 │
└─────────────────────────────────────────────────────────┘
```

---

## 📂 ディレクトリ構造

```
creature-duel/
├── src/
│   └── creature_duel/
│       ├── domain/                 # ドメイン層
│       │   ├── entities/          # エンティティ
│       │   │   ├── creature.py
│       │   │   ├── skill.py
│       │   │   ├── ability.py
│       │   │   └── player.py
│       │   ├── value_objects/     # 値オブジェクト
│       │   │   ├── stats.py
│       │   │   ├── type.py
│       │   │   └── status_ailment.py
│       │   └── enums/             # 列挙型
│       │       ├── move_category.py
│       │       └── ailment_type.py
│       │
│       ├── application/            # アプリケーション層
│       │   ├── services/          # ドメインサービス
│       │   │   ├── damage_calculator.py
│       │   │   ├── accuracy_calculator.py
│       │   │   ├── type_effectiveness.py
│       │   │   └── stat_modifier_service.py
│       │   └── use_cases/         # ユースケース（Phase 4以降）
│       │
│       ├── battle/                # バトルエンジン
│       │   ├── battle_engine.py
│       │   ├── turn_processor.py
│       │   └── battle_state.py
│       │
│       └── infrastructure/        # インフラ層
│           ├── data/              # マスタデータ
│           │   ├── loader.py
│           │   ├── skills.json
│           │   ├── creatures.json
│           │   ├── abilities.json
│           │   └── type_chart.json
│           └── bigquery/          # BigQuery連携（Phase 5）
│
├── tests/                         # テスト
│   └── unit/
│       ├── domain/
│       ├── application/
│       └── infrastructure/
│
├── examples/                      # サンプルスクリプト
├── docs/                          # ドキュメント
└── streamlit_app/                 # Streamlit UI（Phase 6）
```

---

## 🔷 ドメイン層

### 責務
- ビジネスロジックの中核
- ドメインモデルの定義
- ビジネスルールの実装

### 主要コンポーネント

#### Entities（エンティティ）
**Creature** - クリーチャー
- 識別子: name
- 属性: types, base_stats, skills, ability
- 状態: battle_stats, status_ailment
- メソッド: take_damage(), heal(), apply_status_ailment()

**Skill** - 技
- 識別子: name
- 属性: type, category, power, accuracy, max_pp
- 状態: current_pp
- メソッド: use(), reset_pp(), can_use()

**Ability** - 特性
- 識別子: id
- 属性: name, description, trigger, effect_config
- メソッド: is_type_boost(), is_stat_change()

**Player** - プレイヤー
- 識別子: name
- 属性: creatures (1-6体)
- 状態: current_creature_index
- メソッド: switch_creature(), is_defeated()

#### Value Objects（値オブジェクト）
**Stats** - 基本ステータス
- HP, Attack, Defence, Sp.Attack, Sp.Defence, Speed
- イミュータブル

**BattleStats** - バトル中のステータス
- current_hp, 各種ステータス
- 能力ランク（-6 ~ +6）
- 回避率、命中率、急所率
- ミュータブル

**StatusAilment** - 状態異常
- ailment_type, turns_remaining, is_active
- メソッド: tick(), get_damage_ratio()

#### Enums（列挙型）
- **Type**: ノーマル、ほのお、みず、でんき、くさ、こおり
- **MoveCategory**: PHYSICAL, SPECIAL, STATUS
- **AilmentType**: POISON, BURN, FREEZE, SLEEP, PARALYSIS, CONFUSION
- **AbilityTrigger**: ON_ATTACK, ON_HIT, ON_SWITCH_IN, PASSIVE

---

## 🔶 アプリケーション層

### 責務
- ユースケースの実装
- ドメインサービスの提供
- ビジネスフローの制御

### Services（ドメインサービス）

#### DamageCalculator
**責務**: ダメージ計算
- 基本ダメージ = (攻撃力 × 技威力 / 防御力)
- タイプ相性補正
- STAB補正
- HP依存補正
- Ability補正
- クリティカルヒット

**依存関係**:
- TypeEffectivenessService
- StatModifierService
- MasterDataLoader

#### TypeEffectivenessService
**責務**: タイプ相性計算
- type_chart.jsonから相性表を読み込み
- 攻撃タイプ × 防御タイプの倍率計算
- 複合タイプ対応（倍率の掛け算）

#### StatModifierService
**責務**: 能力値補正計算
- 能力ランクの変更
- HP依存の補正倍率計算
- 状態異常による補正
- 実効素早さの計算

#### AccuracyCalculator
**責務**: 命中判定
- 技の命中率 × 攻撃側補正 × 防御側補正
- ランダム判定

---

## 🔵 バトル層

### 責務
- バトル全体のフロー制御
- ターン処理
- バトル状態管理

### 主要コンポーネント

#### BattleEngine
**責務**: バトル全体の制御
- バトルの初期化
- ターンループの実行
- 勝敗判定
- バトルログの生成

#### TurnProcessor
**責務**: 1ターンの処理
- Speed順の決定
- スキルの選択（ランダム、PP考慮）
- スキル実行
- ダメージ適用
- 戦闘不能チェック

#### BattleState
**責務**: バトル状態の管理
- プレイヤー情報
- ターン数
- ログイベントの記録
- JSON出力

---

## 🔳 インフラ層

### 責務
- 外部システムとの連携
- データの永続化
- 技術的な実装詳細

### Data（マスタデータ管理）

#### MasterDataLoader
**責務**: JSONファイルからマスタデータを読み込み
- load_skills() → Dict[str, Skill]
- load_creatures() → Dict[str, Creature]
- load_abilities() → Dict[str, Ability]
- load_type_chart() → Dict[str, Dict[str, float]]
- キャッシュ機構

#### マスタデータファイル
- **skills.json**: 29種類の技
- **creatures.json**: 10体のクリーチャー
- **abilities.json**: 10種類の特性
- **type_chart.json**: 6×6のタイプ相性表

### BigQuery（Phase 5で実装予定）
- バトルログの保存
- 統計データの蓄積
- 機械学習データの提供

---

## 🔄 データフロー

### バトル実行のフロー

```
1. BattleEngine.execute_battle()
   ↓
2. TurnProcessor.process_turn()
   ↓
3. スキル選択（ランダム、PP考慮）
   ↓
4. AccuracyCalculator.check_hit()
   ↓
5. DamageCalculator.calculate_damage()
   ├→ TypeEffectivenessService.get_type_multiplier()
   ├→ StatModifierService (HP補正、状態異常補正)
   └→ MasterDataLoader.get_ability() (Ability補正)
   ↓
6. Creature.take_damage()
   ↓
7. 戦闘不能チェック
   ↓
8. 状態異常処理（ターン終了時）
   ↓
9. BattleState.add_log()
   ↓
10. 勝敗判定
```

### ダメージ計算の依存関係

```
DamageCalculator
 ├→ TypeEffectivenessService
 │   └→ MasterDataLoader (type_chart.json)
 ├→ StatModifierService
 │   └→ Creature.battle_stats
 └→ MasterDataLoader
     └→ abilities.json
```

---

## 🧪 テスト戦略

### テストピラミッド

```
        ┌──────────────┐
        │   E2E Tests  │  統合テスト（Phase 4以降）
        │   (少数)     │
        └──────────────┘
       ┌──────────────────┐
       │ Integration Tests│  サービス間のテスト
       │   (中程度)       │
       └──────────────────┘
    ┌──────────────────────────┐
    │      Unit Tests          │  ユニットテスト（現在89個）
    │      (多数)              │
    └──────────────────────────┘
```

### テストの分類

#### Unit Tests（ユニットテスト）
- **domain層**: Creature, Stats, StatusAilment, Ability, Player
- **application層**: DamageCalculator, TypeEffectivenessService, StatModifierService
- **infrastructure層**: MasterDataLoader

#### Integration Tests（統合テスト）
- バトル実行の完全フロー
- マスタデータ読み込み → バトル → ログ出力

#### E2E Tests（エンドツーエンドテスト）
- JSON読み込み → バトル実行 → BigQuery送信 → Streamlit表示

---

## 🎯 設計パターン

### 使用しているパターン

#### 1. Repository Pattern
- **MasterDataLoader**: データアクセスを抽象化
- JSONとBigQueryの切り替えが容易

#### 2. Service Layer Pattern
- **DamageCalculator, TypeEffectivenessService**: ビジネスロジックをサービスに集約
- ドメインモデルをシンプルに保つ

#### 3. Strategy Pattern
- **Ability**: 特性による異なる振る舞い
- effect_configで動的に動作を変更

#### 4. Value Object Pattern
- **Stats, StatusAilment**: イミュータブルな値オブジェクト
- 等価性の比較が明確

#### 5. Factory Pattern
- **Ability.from_dict()**: JSONから複雑なオブジェクトを生成
- **MasterDataLoader**: エンティティの生成を一元管理

---

## 📊 依存関係の原則

### 依存性逆転の原則（DIP）

```
Domain Layer (ビジネスロジック)
     ↑
     │ 依存
     │
Application Layer (アプリケーションサービス)
     ↑
     │ 依存
     │
Infrastructure Layer (技術詳細)
```

### ポイント
- **ドメイン層は他の層に依存しない**
- アプリケーション層はドメイン層に依存
- インフラ層はアプリケーション層に依存
- **依存の方向は常に内側（ドメイン）に向かう**

---

## 🚀 拡張性

### 新機能の追加方法

#### 新しいタイプの追加
1. `Type` enumに追加
2. `type_chart.json`に相性を追加
3. テストを追加

#### 新しいAbilityの追加
1. `abilities.json`に定義を追加
2. 必要に応じて新しいeffect_typeを実装
3. テストを追加

#### 新しいCreatureの追加
1. `creatures.json`に定義を追加
2. 技とAbilityを関連付け
3. バランステスト

---

## 🔐 設計上の制約

### ビジネスルール
1. **Creatureの交代は不可**（仕様）
2. **道具の概念は不要**（仕様）
3. **登場順は事前決定**（仕様）
4. **Skill選択はランダム**（現在の実装）

### 技術的制約
1. **Python 3.11+**
2. **型ヒントの使用必須**
3. **テストカバレッジ維持**
4. **JSON形式のマスタデータ**

---

## 📈 今後の拡張予定

### Phase 4: バトルシステム実装
- Skill実行エンジンの完全実装
- Effect適用システム
- バトルログの充実

### Phase 5: BigQuery連携
- バトルログの保存
- 統計データの蓄積

### Phase 6: Streamlit UI
- Webベースのダッシュボード
- バトル実行UI
- 統計・分析UI

### Phase 7: 最適化
- Double Battle対応
- パフォーマンスチューニング
- エンドツーエンドテスト

---

**このアーキテクチャは、拡張性と保守性を重視して設計されています。** 🏗️
