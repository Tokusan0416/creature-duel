# Creature Duel - Development Roadmap

最終更新: 2026-03-23 (Phase 1完了)

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

### Phase 2: ドメインモデル拡張

**期間**: Week 2-3

#### タスク
- [ ] Statsクラスの拡張
  - [ ] Evasion, Accuracy, Critical Hit Rate追加
  - [ ] 能力ランク（-6 ~ +6段階）の追加
- [ ] StatModifiers実装
  - [ ] ランク→倍率変換
  - [ ] HP依存のAttack/Sp.Attack補正
- [ ] StatusAilment実装
  - [ ] 6種類の状態異常（毒、火傷、氷、眠り、まひ、混乱）
  - [ ] ターン開始時/終了時の処理
- [ ] Ability実装
  - [ ] Abilityエンティティ作成
  - [ ] 発動トリガーシステム
  - [ ] 基本的なAbility 5-10種類
    - もうか、げきりゅう、しんりょく
    - いかく、ふみん、めんえき
    - せいでんき、ほのおのからだ等
- [ ] Playerエンティティ実装
  - [ ] 6体のCreature管理
  - [ ] 現在のCreature切り替え
- [ ] タイプ相性表の完全実装（6タイプ）
- [ ] ユニットテスト作成

#### 実装ファイル
- `domain/entities/ability.py`
- `domain/entities/player.py`
- `domain/value_objects/stat_modifiers.py`
- `domain/value_objects/status_ailment.py`
- `domain/enums/move_category.py`
- `domain/enums/battle_mode.py`
- `domain/enums/ailment_type.py`

---

### Phase 3: 計算ロジック実装

**期間**: Week 3-4

#### タスク
- [ ] ダメージ計算の改善
  - [ ] HP依存の補正（50%以下、25%以下）
  - [ ] 能力ランクの適用
  - [ ] STABボーナス（1タイプ/2タイプ対応）
  - [ ] Abilityによる補正
- [ ] 命中判定の実装
  - [ ] Accuracy × Evasionの計算
  - [ ] スキル命中判定
- [ ] クリティカルヒットの実装
  - [ ] 変動するCritical Rate対応
- [ ] タイプ相性サービス
  - [ ] 6タイプの完全な相性表
  - [ ] 2倍、0.5倍、0.25倍、0倍の判定
- [ ] StatModifierサービス
  - [ ] 能力変化の適用
  - [ ] 上限・下限チェック
- [ ] ユニットテスト作成

#### 実装ファイル
- `application/services/damage_calculator.py` (改善)
- `application/services/accuracy_calculator.py`
- `application/services/type_effectiveness.py`
- `application/services/stat_modifier_service.py`

---

### Phase 4: バトルシステム実装

**期間**: Week 5-7

#### タスク
- [ ] Skill実行エンジン
  - [ ] PP消費管理
  - [ ] 命中判定
  - [ ] ダメージ適用
  - [ ] Effect適用（状態異常、能力変化）
- [ ] ターン処理
  - [ ] Speed順の決定
  - [ ] ターン開始時処理
  - [ ] スキルのランダム選択（PP考慮）
  - [ ] スキル実行
  - [ ] ターン終了時処理
  - [ ] 戦闘不能チェック
- [ ] バトルエンジン
  - [ ] バトル初期化
  - [ ] ターンループ制御
  - [ ] 勝敗判定
  - [ ] 次Creature投入
- [ ] バトルログシステム
  - [ ] ログイベント定義
  - [ ] ターン毎のログ記録
  - [ ] JSON形式の出力
- [ ] Single Battle完全実装
- [ ] 統合テスト作成

#### 実装ファイル
- `battle/skill_executor.py`
- `battle/turn_processor.py` (改善)
- `battle/battle_engine.py` (改善)
- `battle/battle_logger.py`
- `battle/battle_state.py` (改善)

#### ログイベント種類
- turn_start
- skill_used
- damage_dealt
- ailment_applied
- stat_changed
- creature_fainted
- creature_switched
- battle_end

---

### Phase 5: BigQuery連携

**期間**: Week 7-8

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
  - [ ] JSON出力機能
- [ ] 統合テスト作成

#### 実装ファイル
- `infrastructure/bigquery/client.py`
- `infrastructure/bigquery/schema.py`
- `infrastructure/bigquery/repository.py`
- `application/use_cases/export_battle_log.py`

#### BigQueryテーブル構造
```sql
-- battles: バトル基本情報
-- battle_logs: ターン毎のイベントログ
-- battle_creatures: 参加Creatureの統計情報
```

---

### Phase 6: テスト・データ整備・最適化

**期間**: Week 8-10

#### タスク
- [ ] マスタデータ作成
  - [ ] Creatureデータ（JSON）
  - [ ] Skillデータ（JSON）
  - [ ] Abilityデータ（JSON）
  - [ ] タイプ相性表（JSON）
- [ ] エンドツーエンドテスト
  - [ ] JSON読み込み→バトル実行→BigQuery送信
  - [ ] 複数バトルシナリオ
- [ ] パフォーマンス最適化
  - [ ] プロファイリング
  - [ ] ボトルネック改善
- [ ] ドキュメント整備
  - [ ] アーキテクチャドキュメント
  - [ ] API仕様書
  - [ ] 運用マニュアル
- [ ] コードレビュー＆リファクタリング

#### 実装ファイル
- `infrastructure/data/creatures.json`
- `infrastructure/data/skills.json`
- `infrastructure/data/abilities.json`
- `infrastructure/data/type_chart.json`
- `docs/architecture.md`
- `docs/battle_flow.md`
- `docs/bigquery_schema.md`

---

## 🔮 将来の拡張（Phase 7以降）

### Double Battle実装
- [ ] 2対2のバトルステート管理
- [ ] 複数ターゲット処理
- [ ] Speed順の複雑な制御

### マスタデータのBigQuery管理
- [ ] BigQueryからのマスタ読み込み
- [ ] キャッシュ機構

### REST API化
- [ ] FastAPIの導入
- [ ] バトル実行API
- [ ] ログ取得API

### 機械学習連携
- [ ] バトルデータの分析
- [ ] 勝率予測モデル
- [ ] 最適なパーティ編成の提案

---

## 📊 進捗トラッキング

### 全体進捗
- Phase 1: ✅ 完了 (100%)
- Phase 2: ⚪ 未着手 (0%)
- Phase 3: ⚪ 未着手 (0%)
- Phase 4: ⚪ 未着手 (0%)
- Phase 5: ⚪ 未着手 (0%)
- Phase 6: ⚪ 未着手 (0%)

### 直近の更新
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
