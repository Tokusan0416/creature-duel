# Creature Duel - Development Roadmap

最終更新: 2026-03-31 (Phase 5完了)

## 📋 プロジェクト概要

ポケモンに似た対戦バトルシミュレーションシステムの開発。
バトルログをJSON形式で出力し、BigQueryに格納して分析・機械学習に活用。

## 🎯 開発方針

- **タイプシステム**: 簡易版の6タイプから始める（ノーマル、ほのお、みず、でんき、くさ、こおり）
- **Ability**: 5-10種類の基本的なもの（もうか、げきりゅう、いかく、ふみん等）
- **BigQuery**: 接続テストは実環境で実施
- **優先順位**: Single Battleを完全実装後、Double Battleに着手
- **データ管理**: 最初はJSONファイルでマスタ管理、後からBigQuery移行

## 📦 採用技術・ライブラリ

### コア機能
- **Python 3.12+**: ベース言語
- **Pydantic 2.x**: データバリデーションとスキーマ定義
- **標準ライブラリ**: dataclasses, enum, random

### BigQuery連携
- **google-cloud-bigquery**: BigQueryへのデータ送信
- **google-auth**: 認証管理

### 開発・テスト
- **pytest**: テストフレームワーク
- **pytest-cov**: カバレッジ計測
- **black**: コードフォーマッター
- **ruff**: 高速リンター
- **mypy**: 型チェッカー

## 📁 ディレクトリ構造

```
creature-duel/
├── src/
│   └── creature_duel/
│       ├── domain/              # ドメインモデル
│       │   ├── entities/        # Creature, Skill, Ability, Player
│       │   ├── value_objects/   # Stats, Type, StatusAilment等
│       │   └── enums/           # MoveCategory, BattleMode等
│       │
│       ├── application/          # アプリケーション層
│       │   ├── services/        # DamageCalculator, TypeEffectiveness等
│       │   └── use_cases/       # ExecuteBattle, ExportBattleLog
│       │
│       ├── battle/              # バトルエンジン
│       │   └── BattleEngine, TurnProcessor, SkillExecutor等
│       │
│       ├── infrastructure/      # インフラ層
│       │   ├── bigquery/        # BigQueryクライアント
│       │   └── data/            # マスタデータ（JSON）
│       │
│       ├── presentation/        # プレゼンテーション層
│       └── utils/               # ユーティリティ
│
├── tests/                       # テスト
├── data/                        # 開発用データ
├── docs/                        # ドキュメント
└── scripts/                     # 運用スクリプト
```

---

## 🚀 開発フェーズ

### Phase 1: 基礎構築 ✅ [完了]

**期間**: Week 1 (2026-03-23)

#### 完了項目
- [x] ROADMAP.md作成
- [x] pyproject.toml更新（依存関係追加）
- [x] 新しいディレクトリ構造作成
- [x] 既存コードの移行とリファクタリング
- [x] 開発環境セットアップ（black, ruff, pytest）
- [x] ユニットテスト作成（Creature, Stats）
- [x] デモスクリプト作成（simple_battle.py）
- [x] **マスタデータ作成（10体、29技、10特性）**
- [x] **MasterDataLoader実装**
- [x] **ローダーのテスト作成（12テスト）**
- [x] **マスタデータ対応デモスクリプト**

#### 実装内容
- プロジェクト構造の再編成
- `src/creature_duel/` 配下の構築
- 既存コード（entities, value_objects, services, battle）の移行
- 開発ツールの導入と設定
- 基本的なバトルシステムの動作確認

#### 実装されたファイル
- `src/creature_duel/domain/entities/creature.py` - Creatureエンティティ
- `src/creature_duel/domain/entities/skill.py` - Skillエンティティ
- `src/creature_duel/domain/value_objects/stats.py` - Stats, BattleStats（能力ランク対応）
- `src/creature_duel/domain/value_objects/type.py` - タイプシステム（6タイプ）
- `src/creature_duel/domain/enums/move_category.py` - 技のカテゴリ
- `src/creature_duel/application/services/damage_calculator.py` - ダメージ計算
- `src/creature_duel/application/services/accuracy_calculator.py` - 命中判定
- `src/creature_duel/battle/battle_state.py` - バトル状態管理
- `src/creature_duel/battle/turn_processor.py` - ターン処理
- `src/creature_duel/battle/battle_engine.py` - バトルエンジン
- `tests/unit/domain/test_creature.py` - Creatureのテスト（6テスト）
- `tests/unit/domain/test_stats.py` - Statsのテスト（4テスト）
- `examples/simple_battle.py` - デモスクリプト

#### 動作確認
- 全テスト合格（10/10）
- リザードン vs カメックスのバトル実行成功
- バトルログのJSON出力確認

---

### Phase 2: ドメインモデル拡張 ✅ [完了]

**期間**: Week 2 (2026-03-26)

#### 完了項目
- [x] **タイプ相性表のJSON統一**
  - [x] type.pyから重複コードを削除
  - [x] TypeEffectivenessService実装（JSON読み込み方式）
  - [x] damage_calculator.pyを新サービス対応に修正
- [x] **StatusAilment実装**
  - [x] 6種類の状態異常（毒、火傷、氷、眠り、まひ、混乱）
  - [x] ターン開始時/終了時の処理
  - [x] Creatureへの状態異常統合
- [x] **Abilityシステム実装**
  - [x] Abilityエンティティ作成
  - [x] 発動トリガーシステム（on_attack, on_hit, on_switch_in, passive）
  - [x] MasterDataLoaderのAbility対応
  - [x] 10種類の特性サポート
- [x] **Playerエンティティ実装**
  - [x] 6体のCreature管理
  - [x] 現在のCreature切り替え
  - [x] 全滅判定
- [x] **StatModifierサービス実装**
  - [x] 能力ランク変更
  - [x] HP依存の補正計算
  - [x] 状態異常による補正
  - [x] 実効素早さ計算
- [x] **ユニットテスト作成（全82テスト）**

#### 実装内容
- タイプ相性表をtype_chart.jsonに統一（データ駆動設計）
- 6種類の状態異常とその効果を完全実装
- 10種類のAbilityをサポート（JSON駆動）
- Playerエンティティで最大6体のCreature管理
- 能力値補正の一元管理（StatModifierService）

#### 実装されたファイル
- `src/creature_duel/application/services/type_effectiveness.py` - タイプ相性計算
- `src/creature_duel/application/services/stat_modifier_service.py` - 能力値補正
- `src/creature_duel/domain/entities/ability.py` - Abilityエンティティ
- `src/creature_duel/domain/entities/player.py` - Playerエンティティ
- `src/creature_duel/domain/value_objects/status_ailment.py` - StatusAilment
- `src/creature_duel/domain/enums/ailment_type.py` - 状態異常タイプ
- `tests/unit/application/test_type_effectiveness.py` - タイプ相性テスト（4テスト）
- `tests/unit/application/test_stat_modifier_service.py` - 能力補正テスト（11テスト）
- `tests/unit/domain/test_ability.py` - Abilityテスト（9テスト）
- `tests/unit/domain/test_player.py` - Playerテスト（13テスト）
- `tests/unit/domain/test_status_ailment.py` - StatusAilmentテスト（17テスト）
- `tests/unit/domain/test_creature.py` - Creatureテスト更新（+6テスト）

#### 動作確認
- 全テスト合格（82/82）
- StatusAilmentの動作確認（毒、火傷のダメージ処理）
- Abilityの読み込み確認
- Player管理機能の確認

---

### Phase 3: 計算ロジック実装 ✅ [完了]

**期間**: Week 3 (2026-03-27)

#### 完了項目
- [x] **ダメージ計算の改善**
  - [x] HP依存の補正（50%以下、25%以下）- Phase 1で実装済み
  - [x] 能力ランクの適用 - Phase 1で実装済み
  - [x] STABボーナス（1タイプ/2タイプ対応）- Phase 1で実装済み
  - [x] **Abilityによる補正（もうか、げきりゅう、しんりょく等）**
  - [x] **状態異常による攻撃力補正（火傷で物理攻撃半減）**
- [x] **命中判定の実装** - Phase 1で実装済み
  - [x] Accuracy × Evasionの計算
  - [x] スキル命中判定
- [x] **クリティカルヒットの実装** - Phase 1で実装済み
  - [x] 変動するCritical Rate対応
- [x] **タイプ相性サービス** - Phase 2で実装済み
  - [x] 6タイプの完全な相性表
  - [x] 2倍、0.5倍、0.25倍、4倍の判定
- [x] **StatModifierサービス** - Phase 2で実装済み
  - [x] 能力変化の適用
  - [x] 上限・下限チェック
- [x] **包括的なユニットテスト作成（全89テスト）**

#### 実装内容
- damage_calculatorにAbility補正を統合（もうか、げきりゅう、しんりょく）
- 状態異常による攻撃力補正を適用（火傷で物理攻撃半減）
- StatModifierServiceを活用した補正計算
- 包括的なテストカバレッジの実現

#### 実装されたファイル
- `src/creature_duel/application/services/damage_calculator.py` - Ability補正・状態異常補正追加
- `tests/unit/application/test_damage_calculator.py` - ダメージ計算テスト（7テスト）

#### 動作確認
- 全テスト合格（89/89）
- Ability補正の動作確認（もうか特性でダメージ1.5倍）
- 状態異常補正の動作確認（火傷で物理攻撃半減）
- デモスクリプトで統合動作確認

#### 備考
Phase 3の多くの機能はPhase 1とPhase 2で既に実装済みでした：
- HP依存の補正、能力ランク、STAB、クリティカルヒット（Phase 1）
- タイプ相性サービス、StatModifierサービス（Phase 2）

Phase 3では残りの部分（Ability補正、状態異常補正）を実装し、
包括的なテストで全機能を検証しました。

---

### Phase 4: バトルシステム実装 ✅ [完了]

**期間**: Week 5-7 (2026-03-30)

#### 完了項目
- [x] **Skill実行エンジン**
  - [x] PP消費管理
  - [x] 命中判定
  - [x] ダメージ適用
  - [x] Effect適用（状態異常、能力変化）
- [x] **ターン処理**
  - [x] Speed順の決定（状態異常による素早さ補正含む）
  - [x] ターン開始時処理
  - [x] スキルのランダム選択（PP考慮）
  - [x] スキル実行（SkillExecutor統合）
  - [x] ターン終了時処理（状態異常ダメージ処理）
  - [x] 戦闘不能チェック
- [x] **バトルエンジン**
  - [x] バトル初期化
  - [x] ターンループ制御
  - [x] 勝敗判定
- [x] **バトルログシステム**
  - [x] ログイベント定義
  - [x] ターン毎のログ記録
  - [x] JSON形式の出力
- [x] **Single Battle完全実装**
- [x] **統合テスト作成（8テスト）**
- [x] **ユニットテスト作成（全103テスト）**

#### 実装内容
- SkillExecutorパターンで技実行ロジックを一元化
- Effect適用システムを実装（状態異常、能力変化）
- TurnProcessorに状態異常処理を統合
- 包括的な統合テストでバトルシステム全体を検証

#### 実装されたファイル
- `src/creature_duel/battle/skill_executor.py` - スキル実行エンジン
- `src/creature_duel/battle/turn_processor.py` - ターン処理（状態異常処理追加）
- `src/creature_duel/battle/battle_engine.py` - バトルエンジン（既存）
- `src/creature_duel/battle/battle_state.py` - バトル状態管理（既存）
- `src/creature_duel/domain/entities/skill.py` - effectsフィールド追加
- `src/creature_duel/infrastructure/data/loader.py` - effects読み込み対応
- `tests/unit/battle/test_skill_executor.py` - SkillExecutorテスト（6テスト）
- `tests/integration/test_battle_integration.py` - 統合テスト（8テスト）

#### 実装されたログイベント種類
- battle_start - バトル開始
- turn_start - ターン開始
- skill_used - 技使用
- skill_missed - 技外れ
- damage_dealt - ダメージ発生
- effect_applied - Effect適用（状態異常、能力変化）
- ailment_damage - 状態異常ダメージ
- cannot_move - 行動不能（氷、眠り）
- no_pp - PP切れ
- creature_fainted - 戦闘不能
- battle_end - バトル終了

#### 動作確認
- 全テスト合格（103/103）
  - ユニットテスト: 95テスト
  - 統合テスト: 8テスト
- 状態異常付与とターン終了時ダメージの動作確認
- 能力変化Effectの動作確認
- タイプ相性、特性、状態異常を含む包括的なバトルテスト成功
- 最大ターン到達時の勝敗判定確認

#### 備考
Phase 4ではバトルシステムの完全実装を達成しました：
- SkillExecutorにより技実行ロジックを集約し、保守性向上
- Effect適用システムにより拡張性の高い技システムを実現
- 状態異常のターン終了時処理を完全実装
- 包括的な統合テストでシステム全体の動作を保証

制約により「次Creature投入」機能は実装していません（Creatureの交代は仕様上不可）。

---

### Phase 5: Streamlit UI 🎨 ✅ [完了]

**期間**: Week 7-8 (2026-03-31)

#### 完了項目
- [x] **Streamlitのセットアップ**
  - [x] pyproject.toml更新（streamlit, plotly追加）
  - [x] streamlit_app/ディレクトリ作成
  - [x] 基本レイアウト構築
- [x] **バトル実行ページ**
  - [x] クリーチャー選択UI（2体）
  - [x] バトル実行ボタン
  - [x] リアルタイムバトルログ表示
  - [x] ターン毎のHP推移グラフ
  - [x] 最終結果表示
- [x] **マスタデータブラウザ**
  - [x] クリーチャー一覧表示
  - [x] スキル詳細表示
  - [x] タイプ相性表の可視化
  - [x] 特性一覧表示
- [x] **バトルログビューワー**
  - [x] ローカルバトルログ表示
  - [x] ログの再生機能
  - [x] JSON出力
- [x] **統計・分析ページ（ローカルデータ）**
  - [x] ローカルバトルログの集計
  - [x] 勝率分析（クリーチャー別、タイプ別）
  - [x] ダメージ統計の可視化
  - [x] 平均ターン数の分析

#### 実装内容
- Streamlitによるインタラクティブなウェブインターフェース
- 4つのメインページ（ホーム、バトル、マスタデータ、ログ、分析）
- Plotlyによる豊富なデータ可視化
- ローカルデータの完全なCRUD操作

#### 実装ファイル
- `streamlit_app/app.py` - メインアプリ
- `streamlit_app/pages/1_🎮_battle.py` - バトル実行
- `streamlit_app/pages/2_📚_master_data.py` - マスタデータ
- `streamlit_app/pages/3_📜_battle_logs.py` - ログビューワー
- `streamlit_app/pages/4_📊_analytics.py` - 統計分析（ローカル）
- `streamlit_app/utils/visualization.py` - 可視化ヘルパー
- `streamlit_app/utils/formatters.py` - フォーマット関数
- `streamlit_app/utils/battle_runner.py` - バトル実行ヘルパー

#### UI機能
- サイドバーでページ切り替え
- カラフルな統計グラフ（Plotly使用）
- インタラクティブなテーブル
- バトルログのアニメーション表示
- リアルタイムデータ更新

#### セットアップコマンド
```bash
# Streamlitアプリ起動
streamlit run streamlit_app/app.py

# ブラウザで http://localhost:8501 が開く
```

#### 備考
Phase 5ではローカルデータのみを扱います。BigQuery連携はPhase 6で実装し、Phase 5のUIに統合します。

---

### Phase 6: BigQuery連携

**期間**: Week 9-10

#### タスク
- [ ] BigQueryスキーマ設計
  - [ ] battlesテーブル
  - [ ] battle_logsテーブル
  - [ ] battle_creaturesテーブル
- [ ] BigQueryクライアント実装
  - [ ] 認証設定
  - [ ] 接続テスト
- [ ] バトルログのエクスポート
  - [ ] JSON→BigQueryマッピング
  - [ ] バッチ挿入機能
  - [ ] エラーハンドリング
- [ ] リポジトリ実装
  - [ ] BattleLogRepository
  - [ ] BigQuery読み込み機能
- [ ] Streamlit UIとの統合
  - [ ] BigQueryからのデータ取得
  - [ ] 統計・分析ページの拡張
  - [ ] データソース切り替え（ローカル/BigQuery）
- [ ] 統合テスト作成

#### 実装ファイル
- `infrastructure/bigquery/client.py`
- `infrastructure/bigquery/schema.py`
- `infrastructure/bigquery/repository.py`
- `application/use_cases/export_battle_log.py`
- `streamlit_app/pages/5_☁️_cloud_analytics.py` - BigQuery統計分析

#### BigQueryテーブル構造
```sql
-- battles: バトル基本情報
-- battle_logs: ターン毎のイベントログ
-- battle_creatures: 参加Creatureの統計情報
```

#### 備考
Phase 6ではBigQuery連携を実装し、Phase 5で作成したStreamlit UIに統合します。これにより、ローカルデータとクラウドデータの両方を扱えるようになります。

---

### Phase 7: テスト・最適化・Double Battle

**期間**: Week 11-13

#### タスク
- [ ] エンドツーエンドテスト
  - [ ] JSON読み込み→バトル実行→BigQuery送信
  - [ ] ローカル→クラウドの完全フロー
  - [ ] 複数バトルシナリオ
  - [ ] Streamlit UIのテスト
- [ ] パフォーマンス最適化
  - [ ] プロファイリング
  - [ ] ボトルネック改善
  - [ ] BigQueryクエリ最適化
  - [ ] バトル実行速度の改善
- [ ] Double Battle実装
  - [ ] 2対2のバトルステート管理
  - [ ] 複数ターゲット処理
  - [ ] Speed順の複雑な制御
  - [ ] StreamlitでのDouble Battle UI
- [ ] ドキュメント整備
  - [ ] Streamlit使い方ガイド
  - [ ] BigQueryスキーマドキュメント
  - [ ] デプロイガイド
- [ ] コードレビュー＆リファクタリング

#### 実装ファイル
- `docs/streamlit_guide.md`
- `docs/bigquery_schema.md`
- `docs/deployment_guide.md`
- `battle/double_battle_engine.py`
- `streamlit_app/pages/6_⚔️_double_battle.py`

---

## 🔮 将来の拡張（Phase 8以降）

### マスタデータのBigQuery管理
- [ ] BigQueryからのマスタ読み込み
- [ ] キャッシュ機構
- [ ] バージョニングシステム

### REST API化
- [ ] FastAPIの導入
- [ ] バトル実行API
- [ ] ログ取得API
- [ ] Streamlitとの連携

### 機械学習連携
- [ ] バトルデータの分析（Streamlit上で実行）
- [ ] 勝率予測モデル
- [ ] 最適なパーティ編成の提案
- [ ] 予測結果のStreamlit表示

### 高度なUI機能
- [ ] バトルアニメーション
- [ ] リアルタイム対戦（WebSocket）
- [ ] ユーザー認証
- [ ] バトル履歴の保存

---

## 📊 進捗トラッキング

### 全体進捗
- Phase 1: ✅ 完了 (100%) - 基礎構築+マスタデータ
- Phase 2: ✅ 完了 (100%) - ドメインモデル拡張
- Phase 3: ✅ 完了 (100%) - 計算ロジック実装
- Phase 4: ✅ 完了 (100%) - バトルシステム実装
- Phase 5: ✅ 完了 (100%) - 🎨 Streamlit UI
- Phase 6: ⚪ 未着手 (0%) - BigQuery連携
- Phase 7: ⚪ 未着手 (0%) - テスト・最適化・Double Battle

### 直近の更新
- 2026-03-31: Phase 5完了 - Streamlit UI実装（9ファイル作成、4ページ完成）
- 2026-03-30: Phase 4完了 - SkillExecutor実装、Effect適用システム実装、統合テスト作成（テスト103個合格）
- 2026-03-27: Phase 3完了 - Ability補正・状態異常補正を実装、包括的なテスト作成（テスト89個合格）
- 2026-03-26: Phase 2完了 - StatusAilment、Ability、Player、StatModifierサービス実装（テスト82個合格）
- 2026-03-23 18:30: マスタデータ作成完了 - 10体のクリーチャー、29種類の技、10種類の特性、タイプ相性表、ローダークラス実装（テスト22個合格）
- 2026-03-23 17:00: Phase 1完了 - 基本バトルシステム動作確認、全テスト合格
- 2026-03-23 10:00: プロジェクト開始、ROADMAP.md作成

---

## 🎓 参考情報

### ポケモン仕様（ダイヤモンド・パール期）
- タイプ相性システム
- 状態異常の仕様
- 能力ランクシステム
- ダメージ計算式

### アーキテクチャパターン
- ドメイン駆動設計（DDD）
- クリーンアーキテクチャ
- レイヤードアーキテクチャ

---

## 📝 メモ・決定事項

### 技術的決定
1. Pythonの型ヒントを積極的に使用
2. Pydanticでバリデーション強化
3. dataclassesでイミュータブルなモデル
4. 関数型プログラミングの要素を取り入れる

### 制約・制限
1. Creatureの交代は不可（仕様）
2. 道具の概念は不要（仕様）
3. 登場順は事前決定（仕様）
4. Skill選択はランダム（仕様）

### 今後検討事項
- [ ] CI/CDパイプラインの構築
- [ ] Dockerコンテナ化
- [ ] ログレベルの設定
- [ ] エラー通知の仕組み
