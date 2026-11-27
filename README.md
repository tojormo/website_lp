# とうじょうRMO ウェブサイト

兵庫県加東市東条地域「とうじょうRMO」の公式ウェブサイトです。
ビルド不要の素の **HTML / CSS / JavaScript** で構成しており、そのままサーバーに置くだけで公開できます。

## ファイル構成

```
website_lp/
├── index.html      … トップページ（ヒーロー＋RMOとは＋3つの活動＋お知らせ＋くわしく知る）
├── about.html      … RMOとは
├── solutions.html  … 3つの目的（農用地保全・地域資源活用・生活支援）
├── challenges.html … 地域の課題
├── contact.html    … お問合せ（Googleフォーム埋め込み＋連絡先）
├── tojo-yamadanishiki.html … 解説「山田錦の特A地区・東条とは」（検索流入の柱ページ）
├── yamadanishiki.html … 解説「山田錦とは」（品種の特徴・歴史・育て方。上のページと対になる柱ページ）
├── news.json       … お知らせデータ（ここを編集して更新）
├── info/           … お知らせからリンクするPDF（イベント案内など）
├── style.css       … 全ページ共通スタイル
├── common.js       … 共通メニューバー・フッターの生成＋共通動作（メニュー等）
├── README.md       … このファイル
├── 404.html        … ページが見つからないときの表示（GitHub Pages が自動で使用）
├── sitemap.xml     … 検索エンジン向けのページ一覧（tools/update_sitemap.py で更新日を管理）
├── robots.txt      … 検索エンジン向けの設定（sitemap.xml の場所を記載）
├── CNAME           … 独自ドメイン（tojormo.com）の設定。GitHub Pages が使用するので消さない
├── tools/
│   ├── sync_chrome.py … common.js のメニュー・フッター・ファビコン・Clarity計測タグを各HTMLに静的に書き込む
│   ├── sync_news.py   … news.json のお知らせを index.html に静的に書き込む
│   └── update_sitemap.py … sitemap.xml の更新日（lastmod）を実際の更新日に合わせる
├── article/        … コラム（検索流入の入り口）
│   ├── index.html  … コラム一覧（/article/）
│   ├── article_*.html … 各コラム記事
│   └── images/     … 記事内の写真（webp＝ページで使用、*-ogp.jpg＝SNS共有用、それ以外の jpg＝元画像として保管）
└── images/
    ├── rmo-logo.webp … メニューバーのロゴマーク（favicon.png を縮小したもの。差し替えたら同じ名前で上書き）
    ├── hero1.jpg / hero1.webp … ヒーロー画像①（jpg＝元画像、webp＝ページで使用）
    ├── hero2.jpg / hero2.webp … ヒーロー画像②（jpg＝元画像、webp＝ページで使用）
    ├── hero3.jpg / hero3.webp … ヒーロー画像③（jpg＝元画像、webp＝ページで使用）
    ├── hero4.jpg / hero4.webp … ヒーロー画像④（jpg＝元画像、webp＝ページで使用）
    ├── hero5.jpg / hero5.webp … ヒーロー画像⑤（jpg＝元画像、webp＝ページで使用）
    └── hero6.jpg / hero6.webp … ヒーロー画像⑥（jpg＝元画像、webp＝ページで使用）
```

## メニューバー・フッターの共通化について

メニューバー（ヘッダー）とフッターは共通化されています。
各ページには `<div id="site-header"></div>` と `<div id="site-footer"></div>` の
プレースホルダーだけを置き、実際の中身は `common.js` が読み込み時に自動で挿入します。

→ **メニューやフッターの修正は `common.js` の1か所を直すだけ**で、全ページに反映されます。

### 修正後は `tools/sync_chrome.py` を実行（SEO対策）

JavaScript で差し込んだリンクやファビコンは、検索エンジンやSNSのプレビューが読み取れない（または読むのが遅れる）ことがあります。
そこで、同じ中身を各HTMLのプレースホルダー内にも**静的なHTMLとして**書き込んでいます
（`<!-- static:begin -->`〜`<!-- static:end -->`、`<head>` 内の `<!-- favicons:begin -->`〜`<!-- favicons:end -->`）。
ブラウザでは従来どおり `common.js` が最新の内容で置き換えるため、見た目は変わりません。

`common.js` のメニュー・フッター・ファビコンを直したら、リポジトリ直下で次を実行してください。

```
python tools/sync_chrome.py
```

- 静的部分のリンクはルート基準（`/about.html` など）です。
- 自動生成部分は直接編集しないでください（次回実行時に上書きされます）。
- 新しいページを追加したときも、`<div id="site-header"></div>` と `<div id="site-footer"></div>` を置いてから実行すれば中身が入ります。

## アクセス解析（Google アナリティクス / Microsoft Clarity）

- **Google アナリティクス（GA4）**：測定ID `G-NV6GTSJNPZ`。各ページの `<head>` に直接書いています。
- **Microsoft Clarity**（ヒートマップ・操作の録画）：プロジェクトID `zjlnmoalsy`。
  `common.js` の `CLARITY_ID` で管理し、`python tools/sync_chrome.py` で全ページの `<head>`
  （`<!-- clarity:begin -->`〜`<!-- clarity:end -->`）に書き込んでいます。
  - IDを変えるときは `CLARITY_ID` を書き換えて再実行、計測を止めるときは `''`（空）にして再実行します。
  - 新しいページを追加したときも、`python tools/sync_chrome.py` を実行すれば計測タグが入ります。
  - 管理画面：https://clarity.microsoft.com

## 「くわしく知る」セクションの背景画像

トップページ下部の「くわしく知る（Contents）」セクションは、コンテンツナビの各タイルに、
リンク先ページと同じヒーロー画像を敷いています（`style.css` の `.menu-card`）。

- 画像の上に暗いグラデーションを重ねて、白い見出しが読みやすいようにしています。
- 暗さを調整したいときは、`.menu-card::after` の `linear-gradient(...)` の
  数値（0〜1）を変更してください（大きいほど暗く＝画像が控えめになります）。

## お知らせの更新方法

お知らせは `news.json` を編集するだけで更新できます。HTMLを触る必要はありません。

| 項目 | 説明 |
| --- | --- |
| date | 日付（YYYY-MM-DD 形式）。新しいものを上に並べます。 |
| category | 分類ラベル（例：お知らせ / イベント / 活動報告）。 |
| title | 表示する見出し。 |
| url | リンク先。空 "" なら文字だけ、URLを入れるとリンクになります。 |

イベント案内などのPDFは `info/` に置き、`url` には **拡張子 `.pdf` まで含めた** URL を書きます
（例：`https://tojormo.com/info/Info_GrassCutter20261123.pdf`）。拡張子がないとリンク切れになります。
お知らせから外したPDFは、`info/` からも削除してください。

### 編集後は `tools/sync_news.py` を実行（SEO対策）

お知らせは JavaScript で読み込んでいるため、そのままでは検索エンジンに中身が伝わりにくくなります。
`news.json` を直したら、リポジトリ直下で次を実行してください。同じ内容が `index.html` の
`<!-- news:begin -->`〜`<!-- news:end -->` の間に静的なHTMLとして書き込まれます（この部分は直接編集しないでください）。

```
python tools/sync_news.py
```

## sitemap.xml の更新日（lastmod）

ページを直したら、コミットの前に次を実行してください。`sitemap.xml` の各ページの更新日が、
実際の更新日（未コミットのページは今日、それ以外は最後にコミットした日）に書き換わります。

```
python tools/update_sitemap.py
```

新しいページを追加したときは、先に `sitemap.xml` へ `<url>` を1つ追記してから実行します。
ページを削除したときは、`sitemap.xml` から該当する `<url>` も消してください。
`404.html`（noindex）と `info/` のPDFは sitemap に載せません。

## 解説ページ「山田錦の特A地区・東条とは」（tojo-yamadanishiki.html）

「山田錦 特A地区」「東条 山田錦」などの検索から訪れる人の入り口になるページです。見た目はコラム記事と同じ
`style.css` の「コラム記事」ブロックを使っています。

- 数字や制度の説明は、ページ末尾の「参考資料」（農林水産省・兵庫県・加東市・特許庁など）にもとづいています。直すときは出典も確認してください。
- 「よくある質問」を直したら、`<head>` 内の構造化データ（`FAQPage`）も同じ文面に直してください（`about.html` も同様）。
- 要点ボックス・表・よくある質問の見た目は、`style.css` 末尾の「解説ブロック」（`.key-points` / `.fact-table` / `.faq`）です。

## 解説ページ「山田錦とは」（yamadanishiki.html）

「山田錦とは」「山田錦 特徴」「山田錦 歴史」などの検索から訪れる人の入り口になるページです。
`tojo-yamadanishiki.html`（産地・特A地区の解説）と役割を分け、こちらは**品種そのもの**を扱います。
同じ内容を両方に書かず、相互にリンクで行き来できるようにしてください。

- 数字や歴史は「参考資料」（加東市「広報かとう」令和6年11月号、農林水産省掲載の日本農業遺産申請書など）にもとづいています。
- 「現場の記録」の囲み（`<aside class="field-note">`）と7章は、note の記事をもとに再構成しています。見た目は `style.css` の「解説ブロック」内 `.field-note` です。
- 「よくある質問」を直したら、`<head>` 内の構造化データ（`FAQPage`）も同じ文面に直してください。
- 写真：`images/yamadanishiki-inaho`（アイキャッチ・本文）、`yamadanishiki-app`（記録アプリ）、`yamadanishiki-kansatsu`（圃場観察）、
  `yamadanishiki-ogp.jpg`（SNS共有用 1200×630）。jpg / png が元画像、webp がページで使用。
- `tojo-yamadanishiki.html` の「産地の知恵」（鉄粉の話）の写真は `images/tojo-hari`（釣り針・イメージ）です。
  土壌調査と遊離酸化鉄の説明は、兵庫県 加西農業改良普及センターへの依頼・聞き取りにもとづきます。

## お問合せフォーム（Googleフォーム）の差し替え

`contact.html` のお問合せフォームは、Googleフォームを iframe で埋め込んでいます。
別のフォームに差し替えるときは、次の手順で行います。

1. Googleフォームを開き、右上「送信」→「< >（埋め込み HTML）」を選択
2. 表示された `<iframe ...>` をコピー
3. `contact.html` 内の `<iframe ...>` を丸ごと差し替える（`src` の URL を置き換えるだけでも可）
   ※ 末尾が「/viewform?embedded=true」などになっている共有用URLです
4. フォームが表示されないとき用に、下部の注記リンク（別ウィンドウで開く）の URL も同じものに合わせてください

フォームの高さが合わないときは、`contact.html` の `<style>` 内 `.gform-embed iframe` の
`min-height`（初期値 1100px）を項目数に応じて調整してください。

連絡先（団体名・所在地・E-mail・SNS）は `contact.html` の「連絡先」ブロックを直接編集します。

## ヒーロー画像の差し替え

ページでは軽量な `images/hero1.webp` 〜 `hero6.webp` を表示しています（`hero*.jpg` は元画像として保管）。
差し替えるときは、新しい画像を `hero1.jpg` 〜 `hero6.jpg` として保存し、WebP に変換して
`hero1.webp` 〜 `hero6.webp` を**同じファイル名**で
上書きすれば差し替わります。

- 推奨サイズ：横 1600〜1920px 程度の横長画像
- トップのヒーローは6枚が5秒ごとに自動で切り替わります
- 初期表示を軽くするため、最初に読み込むのは1枚目（hero1）だけです。2枚目以降は `data-src` に書いておき、
  「次に表示する1枚」だけを順番に先読みします（読み込みが終わっていない画像には切り替えず、次の周期まで待ちます）
- 下層ページの上部画像は、`about.html`＝hero1、`solutions.html`＝hero2、
  `challenges.html`＝hero3、`contact.html`＝hero4 を使用しています

## コラム記事（article/）の構成と追加方法

コラムは検索から直接訪れる人の「入り口」として、次の順で組んでいます。
見た目はすべて `style.css` 末尾の「コラム記事」ブロックで共通化しています（各記事に `<style>` は置きません）。

1. パンくず（HOME ／ コラム ／ 記事名）
2. カテゴリ・タイトル（h1）・公開日／更新日・読了時間
3. アイキャッチ画像（16:9 で表示）
4. サイト紹介バー（とうじょうRMOとは？＋トップへのリンク）
5. この記事の要点（`<div class="key-points">`。検索結果に引用されやすい3〜4行の要約）
6. 目次（h2 に `id="sec1"`〜 を付けてリンク）
7. 本文（末尾に「よくある質問」`<div class="faq">` と「参考資料」。よくある質問を直したら `<head>` の構造化データ `FAQPage` も同じ文面に）
8. 団体紹介ボックス（トップ・RMOとは・3つの目的・地域の課題へのリンク）
9. 公式LINE CTA
10. あわせて読みたい（他の記事カード）＋コラム一覧へ
11. トップページへの写真バンド
12. スマホのみ：画面下の固定メニュー（トップ／コラム一覧／上へ／公式LINE）

`article_rmo.html` の画像は `images/hero6・hero3・hero2` をトリミングしたものです
（`article/images/rmo-eyecatch`＝アイキャッチ、`rmo-machine`・`rmo-rice`＝本文、`rmo-ogp.jpg`＝SNS共有用 1200×630）。

各記事の画像は article_rmo と同じルールでそろえています。

- アイキャッチ・本文写真は **16:9** に切り出した専用画像を使い、本文写真は `<figure class="column-figure">` ＋ キャプション
- SNS共有用は **1200×630 の jpg**（`*-ogp.jpg`）
- 一覧・関連記事・トップのカードは、各記事のアイキャッチと同じ画像

| 記事 | アイキャッチ | 本文 | OGP |
| --- | --- | --- | --- |
| article_rmo | rmo-eyecatch（hero6） | rmo-machine（hero3）、rmo-rice（hero2） | rmo-ogp.jpg |
| article_rtkvrs | rtk-eyecatch（rtk-tractor） | rtk-auto（auto）、rtk-vrs（vrs-station） | rtk-ogp.jpg |
| article_wataras | wtr-eyecatch（wataras） | wtr-field（hero1） | wtr-ogp.jpg |
| article_yamadanishiki | ymd_grain | ymd_sakagura_16x9（sakagura）、ymd_sake（締めの引用パネル） | ymd-ogp.jpg |

（　）内は切り出し元の写真です。切り出し元は jpg のみ `article/images/` に保管しています（ページでは使っていません）。
コラム一覧（`article/index.html`）の上部画像は `photo-02.webp` です。

写真を背景にした引用パネルは `<figure class="photo-quote">` で、ほかの記事でも使えます。

記事の大見出し（h1）と title は、検索される言葉（例：「RTK・VRSとは？」「水田の水位管理を自動化する理由」）を先頭に置いています。

**記事を追加するとき**は、既存の記事をコピーして中身を差し替え、次の箇所も更新してください。

- `<head>`：title / description / canonical / og:* / twitter:* / 構造化データ（JSON-LD）の見出し・日付・URL
- `article/index.html`：一覧にカードを追加
- 他の記事の「あわせて読みたい」：カードを追加（3件程度に絞る）
- `common.js` のフッター「Column」（→ `python tools/sync_chrome.py` を実行）、`sitemap.xml`
- トップ `index.html` の「くわしく知る」（必要に応じて）

## コンテンツページの追加方法

1. 既存のページ（例：`about.html`）をコピーして `xxx.html` を作成し、中身を編集
2. メニューバーやフッターにリンクを追加したいときは、**`common.js` を1か所だけ**編集

   ```js
   // common.js の HEADER_HTML / FOOTER_HTML 内に1行追加
   <a href="xxx.html">新しいページ名</a>
   ```

   編集後は `python tools/sync_chrome.py` を実行してください（各HTMLの静的メニューにも反映されます）。

3. トップページ `index.html` の「くわしく知る」カードにも、必要に応じて追加

## ローカルでの確認方法

お知らせ（news.json）は `fetch()` で読み込むため、**ファイルをダブルクリック（file://）した
状態では表示されません。** 簡易サーバーを立てて確認してください。

```
cd website_lp
python -m http.server 8000
# → http://localhost:8000
```

## 公開方法

GitHub Pages で公開しています（リポジトリ `tojormo/website_lp` の `main` ブランチ → https://tojormo.com/ ）。
`main` に push すると数分で反映されます。ほかのサーバーに置く場合も、フォルダの中身を**そのままアップロード**するだけです。

公開前のチェック（ページや画像を直したとき）:

1. `python tools/sync_chrome.py`（`common.js` を直したとき）
2. `python tools/sync_news.py`（`news.json` を直したとき）
3. `python tools/update_sitemap.py`（コミットの前に毎回）
4. 使わなくなった画像・PDF は削除する（元画像の jpg は上記ルールのとおり保管）

## 補足

- 文字コードはすべて **UTF-8** です。編集時は UTF-8 のまま保存してください。
- 対応ブラウザ：モダンブラウザ（Chrome / Edge / Safari / Firefox の最新版）

© 2026 とうじょうRMO ｜ 兵庫県加東市東条地域
