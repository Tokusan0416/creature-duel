# Creature Duel - ドキュメント

このディレクトリには、Creature Duelプロジェクトの各種ドキュメントが格納されています。

---

## 📚 ドキュメント一覧

### 🎯 プロジェクト全体

#### [project_status.md](project_status.md)
**現在のプロジェクトステータス**

- 全体進捗（Phase別）
- 実装済み機能一覧
- 未実装機能リスト
- テスト状況
- コード品質メトリクス
- 既知の問題・制限

**👉 最初に読むべきドキュメント** - プロジェクトの現状を把握できます。

---

#### [architecture.md](architecture.md)
**アーキテクチャドキュメント**

- 設計思想とコア原則
- レイヤード構造の説明
- 各層の責務とコンポーネント
- データフロー
- 設計パターン
- 依存関係の原則

**👉 設計を理解するための必読ドキュメント** - システム全体の構造を把握できます。

---

### 📖 Phase別サマリー

#### [phase1_summary.md](phase1_summary.md)
**Phase 1完了サマリー（2026-03-23）**

- プロジェクト構造の構築
- 開発環境のセットアップ
- ドメインモデルの実装
- バトルシステムの基本実装
- テストの実装（10テスト）

**内容**:
- Creature, Skill, Stats, Type実装
- DamageCalculator, AccuracyCalculator実装
- BattleEngine, TurnProcessor実装
- デモスクリプト作成

---

#### [phase2_summary.md](phase2_summary.md)
**Phase 2完了サマリー（2026-03-26）**

- タイプ相性表のJSON統一
- StatusAilment（状態異常）の実装
- Abilityシステムの実装
- Playerエンティティの実装
- StatModifierServiceの実装
- テスト追加（+56テスト、計82テスト）

**内容**:
- 6種類の状態異常（毒、火傷、氷、眠り、麻痺、混乱）
- 10種類のAbility
- Player管理機能（最大6体のCreature）
- TypeEffectivenessService実装

---

#### [phase3_summary.md](phase3_summary.md)
**Phase 3完了サマリー（2026-03-27）**

- Abilityによる補正の実装
- 状態異常による攻撃力補正の実装
- ダメージ計算式の完成
- 包括的なテストの作成
- テスト追加（+7テスト、計89テスト）

**内容**:
- もうか、げきりゅう、しんりょく特性の実装
- 火傷状態での物理攻撃半減
- 最終的なダメージ計算式の完成

---

#### [phase4_summary.md](phase4_summary.md)
**Phase 4完了サマリー（2026-03-30）**

- SkillExecutorの実装
- Effect適用システムの実装
- ターン終了時の状態異常処理
- 統合テストの作成
- テスト追加（+14テスト、計103テスト）

**内容**:
- SkillExecutorパターンによる技実行ロジックの一元化
- ailment/stat_change Effect適用システム
- 状態異常ダメージのターン終了時処理
- 包括的な統合テスト（8テスト）
- Single Battle完全実装

---

### 📊 マスタデータ

#### [master_data_summary.md](master_data_summary.md)
**マスタデータ概要**

- skills.json（29種類の技）
- creatures.json（10体のクリーチャー）
- abilities.json（10種類の特性）
- type_chart.json（6×6タイプ相性表）

**内容**:
- 各マスタデータの詳細
- タイプ別・カテゴリ別の分布
- バトルスタイル別の分類
- タイプ相性表の説明

---

### 🎨 Streamlit UI（Phase 5）

#### [streamlit_integration_plan.md](streamlit_integration_plan.md)
**Streamlit統合計画**

- Streamlitアプリの設計
- ページ構成（Home, Battle, Analytics, Master Data, Logs）
- UI機能の詳細
- 実装コード例
- セットアップ方法

**Phase 5で実装予定** - WebベースのダッシュボードUI（ローカルデータ）

---

#### [streamlit_quick_start.md](streamlit_quick_start.md)
**Streamlitクイックスタート**

- インストール方法
- 使い方
- カスタマイズ方法

**Phase 5で実装予定** - Streamlitアプリの簡易ガイド

---

## 🗺️ ドキュメントの読み方

### 初めての方
1. **[project_status.md](project_status.md)** - プロジェクトの現状を把握
2. **[architecture.md](architecture.md)** - システムの設計を理解
3. **Phase別サマリー** - 各フェーズの実装内容を確認

### 開発者向け
1. **[architecture.md](architecture.md)** - アーキテクチャを理解
2. **[phase4_summary.md](phase4_summary.md)** - 最新の実装状況を確認
3. **[master_data_summary.md](master_data_summary.md)** - マスタデータ構造を把握

### 今後の開発に参加する方
1. **[project_status.md](project_status.md)** - 未実装機能を確認
2. **[../ROADMAP.md](../ROADMAP.md)** - 今後の開発計画を確認
3. **Phase別サマリー** - 既存実装を理解

---

## 📁 ディレクトリ構造

```
docs/
├── README.md                        # このファイル
├── project_status.md                # プロジェクトステータス ⭐
├── architecture.md                  # アーキテクチャドキュメント ⭐
│
├── phase1_summary.md                # Phase 1サマリー
├── phase2_summary.md                # Phase 2サマリー
├── phase3_summary.md                # Phase 3サマリー
├── phase4_summary.md                # Phase 4サマリー（最新）⭐
│
├── master_data_summary.md           # マスタデータ概要
│
├── streamlit_integration_plan.md    # Streamlit統合計画（Phase 6）
└── streamlit_quick_start.md         # Streamlitクイックスタート（Phase 6）
```

**⭐ = 特に重要なドキュメント**

---

## 🔄 ドキュメントの更新

### 更新ルール
- **Phase完了時**: 対応するphase_summary.mdを作成
- **機能追加時**: architecture.mdとproject_status.mdを更新
- **マイルストーン達成時**: project_status.mdを更新

### 更新履歴
- 2026-03-27: Phase 3完了に伴い、各ドキュメントを更新
- 2026-03-26: Phase 2完了に伴い、phase2_summary.md作成
- 2026-03-23: Phase 1完了に伴い、phase1_summary.md、master_data_summary.md作成

---

## 📞 お問い合わせ

ドキュメントに不明点や誤りがある場合は、Issueトラッカーで報告してください。

---

**このドキュメントは、Creature Duelプロジェクトの理解を助けるために作成されました。** 📚
