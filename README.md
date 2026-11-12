<p align="center">
  <a href="https://www.nemdull.com/"><img src="./assets/header.svg" alt="ねむい。だるい。だから自動化する。" width="100%" /></a>
</p>

nemdull（ねむだる）です。金融系の SIer で、会員向け Web システムのプロジェクトリーダーをしています。

同じ確認を手で何度も繰り返すのが苦手で、気づくとテストを書いて機械に任せています。最近は生成 AI にも手伝ってもらっていますが、テストを通すために期待値のほうを書き換えてしまうことがあるので、それをさせない決まりを作りました。

くわしいことは [nemdull.com](https://www.nemdull.com/) にまとめています。開くたびに自分で自分を点検するページで、隕石をぶつけて壊すこともできます。

ふだんは [X](https://x.com/nemdull) にいます。記事は [Qiita](https://qiita.com/nemdull) と [Zenn](https://zenn.dev/nemdull)、登壇の資料は [Speaker Deck](https://speakerdeck.com/nemdull)、参加した勉強会は [connpass](https://connpass.com/user/nemdull/)、スキルの偏り具合は [Findy](https://findy-code.io/skills-share/6l9E_223HPNgn) で見られます。

## 置いてあるもの

| リポジトリ | ひとこと |
| --- | --- |
| [sf-meter-api](https://github.com/nemdull/sf-meter-api) | SF に出てくる技術の「実現度」を返す API。Go の標準ライブラリで、層を分けて依存の向きをそろえています。保存先（メモリと PostgreSQL）のどちらにも、同じテストを当てています |
| [sf-meter-web](https://github.com/nemdull/sf-meter-web) | その画面。React と TypeScript。針の計器と検索つきで、API が落ちていてもサンプルデータで動きます |
| [sf-meter](https://github.com/nemdull/sf-meter) | 上の 2 つをまとめた入り口。`docker compose up` で DB・API・画面がまとめて立ち上がります |
| [profile_site](https://github.com/nemdull/profile_site) | [nemdull.com](https://www.nemdull.com/) のコード。ページが自分で自分を点検します。隕石で壊して、見つけて、直すところまでを Playwright で確かめています |
| [sakujiru-app](https://github.com/nemdull/sakujiru-app) | 作字クリエイターのための作品投稿サイト。Ruby on Rails 6（[動いているもの](https://sakujiru-web.onrender.com/)。起動に少し時間がかかります） |
| [zenn](https://github.com/nemdull/zenn) | 記事の原稿置き場 |
| [atcoder](https://github.com/nemdull/atcoder) | 競技プログラミングの解答。Java |

ほかに、Expo（React Native）でモバイルアプリも作っています。こちらはまだ非公開です。

## 仕事でやっていること

- 会員向け Web システムの保守とエンハンス。要件の整理から見積、お客さんとのやりとりまでを見ています
- Playwright と Jest で、回帰テストを自動にすること
- 生成 AI にテストや設計書を手伝ってもらうときの決まりづくり（期待値を勝手に変えない、根拠を必ず書く、あいまいな言い回しは自動で引っかける）
- 本番障害の原因調査と、再発防止（[そのとき学んだことを書きました](https://qiita.com/nemdull/items/460ff96a438317e69722)）

Findy の「開発組織のぷち改善ハッカソン」では、Slack で匿名の相談ができる Bot を 1 日で作りました（[記事](https://qiita.com/nemdull/items/a2d72e6a5d4e82161e00)）。AWS Solutions Architect Professional の対策書（改訂 2 版）も、チームで書いています。

## 最近書いたもの

<!-- posts:start -->
- 2025-12-17 - [障害対応で学んだこと ― 保守・運用の現場で、実務を通じて理解が進んだこと ―](https://qiita.com/nemdull/items/460ff96a438317e69722)
- 2025-12-12 - [Findy「開発組織のぷち改善ハッカソン」で Slack匿名お悩みBot を作った話 〜AI × Slack × Playwright で心理的安全性をちょっとだけ上げる〜](https://qiita.com/nemdull/items/a2d72e6a5d4e82161e00)
- 2025-12-19 - [Go言語で気づいたシンプル設計の真髄 ─ Rails・Java経験者がハマったポイントまとめ](https://qiita.com/nemdull/items/7ff73572ccc3c78d311d)
- 2025-08-25 - [『初めてのGo言語 第2版』読書＆学習ログ（第3章）](https://qiita.com/nemdull/items/c51875f636e074358d1e)
<!-- posts:end -->

## 使っている道具

| 場面 | 道具 |
| --- | --- |
| 仕事 | Oracle APEX、PL/SQL、React、TypeScript、AWS（Lambda、API Gateway、RDS、S3、CloudWatch）、Playwright、Jest、Claude Code |
| 個人開発 | Go、PostgreSQL、Docker、Ruby on Rails、Expo（React Native）、GitHub Actions |
| ほかに使ってきたもの | Node.js、Python、Storybook、RJSF |

<p align="center">
  <img src="https://raw.githubusercontent.com/nemdull/nemdull/output/github-contribution-grid-snake.svg" alt="コントリビューションの記録" />
</p>
