# Creature Duel Application

## 概要
これはポケモンに似た対戦バトルを実施するアプリケーションです。
対戦のログはJSONで吐き出され、BigQueryに格納し分析や機械学習等に生かすことができます。
将来的にはCreatureやSkillに関してもBigQueryでマスタ管理する予定です。

## ルール・システム
- Creatureを1対1で対戦させるSingle Battle、2対2で対戦させるDouble Battleがあります
- Playerは1回のバトルで6体のCreatureを保持します
- Creatureは1ターンにつき1回のSkillを繰り出し、勝負がつくまでターンを繰り返します
- Creatureが倒れた際は次のCreatureを出し、全てのCreatureが倒されると敗戦となります

## Type（タイプ）
- Creatureは1~2つのTypeを保持します
- 後述のSkillもTypeを1つ保持しており、CreatureのTypeとの組み合わせによってダメージが0倍、0.25倍、0.5倍、1倍、2倍、4倍と変化します
- タイプの種類・相性はダイヤモンド・パール期のものを想定しています

## Skill（技）
- Creatureは1体につき4つのSkillを保持しています
- Skillには以下の要素があり、保持しているCreatureに関わらず一律のものです
    - Move Category（カテゴリ）
        - Physical Move（物理）：自CreatureのAttack、相手CreatureのDefenceの値に応じてダメージを与えます
        - Special Move（特殊）：自CreatureのSpecial Attack、相手CreatureのSpecial Defenceの値に応じてダメージを与えます
        - Status Move（変化）：ダメージは与えず、Abilityを変化させる等の効果を出します
    - Type（タイプ）
        - 前述のとおり、Skillも1つのTypeを保持しています
    - Power（威力）
        - PowerとAbility、Typeの掛け合わせによってダメージが決定します
    - Accuracy（命中）
        - 相手のEvasionの掛け合わせによって的中するかしないかが決定します
    - Effect（効果）
        - Abilityを変化させる等の効果を指します
        - Status Moveは必ず保持しており、Physical Move・Special Moveは保持するものとそうでないものがあります
    - PP（上限回数）
        - 1回のバトルでPPを超える回数使うことはできません

## Stats（能力）
- Creatureは下記のStatsを保持します
- SkillやAbilityによってバトル中に値が変化します（バトル終了後は元に戻ります）
    - HP（体力）
        - 0になると戦闘不能となります
        - 50%以下でAttackとSpecial Attackが25%、25%以下でAttackとSpecial Attackが50%上昇します
        - SkillやAbilityによって回復もできます
    - Attack（攻撃）
        - Physical Moveのダメージに影響します
        - SkillやAbilityの効果で-100%~+100%まで変化します（それ以上は変化しません）
    - Defence（防御）
        - Physical Moveの被ダメージに影響します
        - SkillやAbilityの効果で-100%~+100%まで変化します（それ以上は変化しません）
    - Special Attack（特殊攻撃）
        - Special Moveのダメージに影響します
        - SkillやAbilityの効果で-100%~+100%まで変化します（それ以上は変化しません）
    - Special Defence（特殊防御）
        - Special Moveの被ダメージに影響します
        - SkillやAbilityの効果で-100%~+100%まで変化します（それ以上は変化しません）
    - Speed（素早さ）
        - ターン内でSpeedの値が高いCreatureが先に行動できます
        - SkillやAbilityの効果で-100%~+100%まで変化します（それ以上は変化しません）
    - Evasion（回避率）
        - 相手のSkillを回避できる確率で、バトル開始時は一律0%です
        - 相手のSkill・AbilityのAccuracyとの掛け合わせで命中するかが決定します
        - SkillやAbilityの効果で-50%~+50%まで変化します（それ以上は変化しません）
    - Accuracy（命中）
        - Skillが命中する確率で、バトル開始時は一律0%です
        - SkillのAccuracy、相手のEvasionとの掛け合わせで命中するかが決定します
        - SkillやAbilityの効果で-50%~+50%まで変化します（それ以上は変化しません）
    - Critical Hit Rate（急所率）
        - 2倍のダメージを与える確率で、バトル開始時は一律10%です
        - SkillやAbilityの効果で-10%~+10%まで変化します（それ以上は変化しません）

## Ability（特性）
- Creatureは1体につき1つのAbilityを保持しています
- AbilityにはStatsを変化させるものをはじめ、発動条件や効果等様々な種類があります

## Status Ailment（状態異常）
- CreatureはSkillやAbilityの効果により、以下のStatus Ailmentになることがあります
- Status Ailmentは重複せず、同時には1つしかかかりません
    - Poisoned（毒）
        - 毎ターン終了後に最大HPの1/10のダメージを受けます
    - Burned（火傷）
        - 毎ターン終了後に最大HPの1/16のダメージを受けます
        - Attackが25%減少します
    - Frozen（氷）
        - 1~3ターンの間、Skillを出すことができなくなります
        - ターン数はランダムで決定し、終了後は状態異常がなくなります
    - Asleep（眠り）
        - 1~3ターンの間、Skillを出すことができなくなります
        - ターン数はランダムで決定し、終了後は状態異常がなくなります
    - Paralyzed（まひ）
        - 20%の確率でSkillを出すことができなくなります
        - Speedが50%減少します
    - Confused（混乱）
        - 1~4ターンの間、30%の確率でSkillを出すことができず、最大HPの1/10のダメージを受けます
        - ターン数はランダムで決定し、終了後は状態異常がなくなります

## ダメージの計算方法
- Physical Move
    - 自分のAttack * SkillのPower / 相手のDefence * SkillのTypeと相手のTypeの組み合わせ倍率
    - 自分のTypeとSkillのTypeが同じとき、以下が加算
        - 自分のTypeが1つ：1.5倍
        - 自分のTypeが2つ：1.25倍
    - Critical Rateの確率で2倍
- Special Move
    - 自分のSpecial Attack * SkillのPower / 相手のSpecial Defence * SkillのTypeと相手のTypeの組み合わせ倍率
    - 自分のTypeとSkillのTypeが同じとき、以下が加算
        - 自分のTypeが1つ：1.5倍
        - 自分のTypeが2つ：1.25倍
    - Critical Rateの確率で2倍

## その他・リアルゲームとの違い
- Creatureの交代はできない
- 道具の概念はいったん不要
- Creatureの登場順はバトル前に決定あする
- ターン毎に実行するSkillはランダムで決定される（PPが0の場合はそのSkillは選ばれない）