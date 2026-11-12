# nemdull（ねむだる）

**面倒なことは、仕組みに任せる。**

金融系 SIer で、会員向け Web システムのプロジェクトリーダーをしているアプリケーションエンジニアです。人が何度も確かめなくて済むように、テストを自動化し、生成 AI には「誤らせない」ための決まりを組み込んでいます。

_Application engineer and project lead at a financial systems integrator in Japan. I automate regression tests and build guardrails that keep generative AI from quietly rewriting the expected results._

[ポートフォリオ](https://www.nemdull.com/) ｜ [X](https://x.com/nemdull) ｜ [Zenn](https://zenn.dev/nemdull) ｜ [Qiita](https://qiita.com/nemdull) ｜ [Speaker Deck](https://speakerdeck.com/nemdull) ｜ [connpass](https://connpass.com/user/nemdull/) ｜ [Findy Skills](https://findy-code.io/skills-share/6l9E_223HPNgn)

## できること（根拠つき）

| できること | 根拠 |
| --- | --- |
| PL として、要件整理から見積・顧客折衝まで案件を回す | 会員向け Web システムの保守・エンハンス（業務、2026 年度から） |
| 回帰テストを自動化して、手で確かめる回数を減らす | 管理画面の開発に Playwright と Jest を導入（業務） |
| 生成 AI に、期待値を書き換えさせない | 改変の禁止・根拠の必須化・曖昧な表現の自動検査を設計し、社内勉強会で 2 回登壇（業務） |
| 本番障害を、原因までさかのぼって直す | 本番障害 2 件の原因特定と恒久対策（業務）／記事「[障害対応で学んだこと](https://qiita.com/nemdull/items/460ff96a438317e69722)」 |
| Go で、依存の向きを守った API を書く | [sf-meter-api](https://github.com/nemdull/sf-meter-api)／記事「[Go言語で気づいたシンプル設計の真髄](https://qiita.com/nemdull/items/7ff73572ccc3c78d311d)」 |

## リポジトリ

| リポジトリ | 何をしているか | 技術 |
| --- | --- | --- |
| [sf-meter-api](https://github.com/nemdull/sf-meter-api) | SF 作品に出てくるテクノロジーを数値にする API。標準ライブラリの `net/http` を中心に層を分け、依存の向きを内側にそろえた。保存先は、PostgreSQL とメモリ上の実装を切り替えられる | Go、PostgreSQL、Docker |
| [sf-meter-web](https://github.com/nemdull/sf-meter-web) | sf-meter の画面 | React、TypeScript、Vite |
| [profile_site](https://github.com/nemdull/profile_site) | [nemdull.com](https://www.nemdull.com/) のコード。載せる内容に、根拠の無い主張やリンクの不備が無いかを、ビルドの前に検査している | React、TypeScript、Tailwind CSS |
| [sakujiru-app](https://github.com/nemdull/sakujiru-app) | 作字クリエイターのための、作品投稿プラットフォーム | Ruby on Rails、Docker |
| [zenn](https://github.com/nemdull/zenn) | 技術記事の原稿 | Markdown |
| [atcoder](https://github.com/nemdull/atcoder) | 競技プログラミングの解答 | Java |

ほかに、Expo（React Native）で個人向けのモバイルアプリを開発しています（コードは非公開）。

## 最近書いたもの

<!-- posts:start -->
- 2025-12-17 - [障害対応で学んだこと ― 保守・運用の現場で、実務を通じて理解が進んだこと ―](https://qiita.com/nemdull/items/460ff96a438317e69722)
- 2025-12-12 - [Findy「開発組織のぷち改善ハッカソン」で Slack匿名お悩みBot を作った話 〜AI × Slack × Playwright で心理的安全性をちょっとだけ上げる〜](https://qiita.com/nemdull/items/a2d72e6a5d4e82161e00)
- 2025-12-19 - [Go言語で気づいたシンプル設計の真髄 ─ Rails・Java経験者がハマったポイントまとめ](https://qiita.com/nemdull/items/7ff73572ccc3c78d311d)
- 2025-08-25 - [『初めてのGo言語 第2版』読書＆学習ログ（第3章）](https://qiita.com/nemdull/items/c51875f636e074358d1e)
<!-- posts:end -->

Findy「開発組織のぷち改善ハッカソン」では、LLM と Slack、Playwright を組み合わせた「Slack 匿名お悩み Bot」を 1 日で作りました（[記事](https://qiita.com/nemdull/items/a2d72e6a5d4e82161e00)）。AWS Solutions Architect Professional 対策書（改訂 2 版）の共著にも参加しています。

## 使っている技術

| 場面 | 技術 |
| --- | --- |
| 仕事 | Oracle APEX、PL/SQL、React、TypeScript、AWS（Lambda、API Gateway、RDS、S3、CloudWatch）、Playwright、Jest、Claude Code |
| 個人開発 | Go、PostgreSQL、Docker、Ruby on Rails、Expo（React Native）、GitHub Actions |
| ほかに使ってきたもの | Node.js、Python、Storybook、RJSF |

## 経歴

- 2026 年 4 月から：プロジェクトリーダー、PM 補佐（金融系 SIer）。会員向け Web システムの保守・エンハンスと、生成 AI を使ったテスト自動化・設計書整備
- 2024 年 4 月から 2026 年 3 月：ソフトウェアエンジニア（金融系 SIer）。不動産 EC 向け管理画面の開発・保守、E2E テストの導入、障害対応

くわしくは[ポートフォリオ](https://www.nemdull.com/)にまとめています。

<p align="center">
  <img src="https://raw.githubusercontent.com/nemdull/nemdull/output/github-contribution-grid-snake.svg" alt="コントリビューションの記録" />
</p>
