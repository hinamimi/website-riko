# 理工の補講 — Webサイト

静的HTMLとCSSのGitHub Pagesサイト。Node.jsやビルド処理は不要です。
動画制作プロジェクトでは `website/` サブモジュールとして利用します。

## 編集とプレビュー

- `public/index.html`：トップページ
- `public/assets/style.css`：共通スタイル
- `public/`：公開するHTML・画像・CSSなど
- `.github/workflows/pages.yml`：GitHub Pages公開設定

このリポジトリのルートで実行します。

```bash
python3 -m http.server 8000 --bind 127.0.0.1 --directory public
```

http://127.0.0.1:8000/ を開きます。終了は Ctrl+C。
HTMLは直接編集し、ページを増やすときは `public/` に追加します。
リンクと画像のパスは相対パスにして、リポジトリ名を含むPagesのURLでも動くようにします。

## チャンネルとデザイン

チャンネル：[理工の補講 / @hinamimi09](https://www.youtube.com/@hinamimi09)。
全ページのヘッダーとフッター、トップの紹介から移動できます。
ニコニコ動画：[シリーズ](https://www.nicovideo.jp/user/51952754/series/580080)。全ページのヘッダーとフッターに配置。

- `public/assets/branding/icon.png`：既存のアイコンv1。ヘッダー・紹介欄で使用。
- `public/assets/branding/banner.png`：既存のバナーv2。トップ上部で使用。
- 原本は制作プロジェクトの `media/branding/rikou-no-hokou/`。画像自体は変更せず複製。
- バナーの表示範囲とサイズ、配色、カードの列数は `public/assets/style.css` で調整。

YouTubeへのリンクには公式faviconを16pxのアクセントとして表示します。
`public/assets/youtube-favicon.ico` は https://www.youtube.com/favicon.ico から2026-09-27に取得。
CSSでリンク先を判定するため、動画URL更新後も自動で表示されます。
サイト自体のfaviconは、チャンネルアイコンから小サイズ用に生成した専用画像です。
`public/favicon.ico` に16・32・48px、`public/assets/favicon/` に各PNGと180pxのタッチアイコンを配置。
元のヘッダー用アイコンとYouTubeリンク用アイコンは変更していません。

スマホでもバナーの文字が残るよう中央を表示しています。
画像を差し替える場合はPCとスマホで文字や図が欠けないことを確認してください。

## 動画ごとのページ

| 動画 | HTML | 要約 |
| --- | --- | --- |
| 複素インピーダンス | `public/videos/complex-impedance/index.html` | 5場面 |
| 集中定数回路 | `public/videos/lumped-circuit/index.html` | 6場面 |
| GND・帰線・アース | `public/videos/gnd-return-earth/index.html` | 6場面・YouTube埋め込み |

トップの動画一覧から各ページへ移動できます。各ページの `images/` に図解画像を置き、
HTMLに短い説明・代替テキスト・目次を直接記述しています。画像を選ぶと拡大表示します。
ページ・要約の表示にはJavaScriptを使いません。

### YouTubeの登録

2026-09-26、複素インピーダンスにユーザー提供の
[YouTube動画](https://www.youtube.com/shorts/DsIEvbgxioI)を埋め込み済みです。
2026-09-27、集中定数回路にもユーザー提供の
[YouTube動画](https://www.youtube.com/shorts/9BAfsqTt8M8)を埋め込みました。
2026-09-30、GND・帰線・アースにユーザー指定の予定URL
https://youtube.com/shorts/RtR0ZcnU_Rw を設定しました。公開・再生可否は未確認です。
動画URLを変更するときは、このリポジトリのルートから次を実行します。
`YOUTUBE_URL` は対象動画の実際のURLへ置き換えてください。

```bash
python3 scripts/set_youtube.py complex-impedance 'YOUTUBE_URL'
python3 scripts/set_youtube.py lumped-circuit 'YOUTUBE_URL'
python3 scripts/set_youtube.py gnd-return-earth 'YOUTUBE_URL'
```

`watch?v=...`、`shorts/...`、`youtu.be/...` を受け付けます。
HTMLへiframeとYouTubeへの直接リンクを書き込みます。ランタイムのPythonやAPIキーは不要です。
プレーヤーは縦動画に合わせた9:16で、自動再生はしません。
ローカル確認は `file://` ではなくHTTPサーバーを使ってください。
複素インピーダンスはローカルChromeでプレーヤーのタイトル・チャンネル名の読込と、
320・390・1280px幅での9:16表示を確認済みです。動画の再生完了は未確認です。

動画を増やす場合は、`public/videos/` に既存ページを複製して、見出し・画像・説明・関連リンクを変更し、
トップの動画一覧にもリンクを追加します。更新コマンドを使う場合は
`scripts/set_youtube.py` の `choices` に新しいディレクトリ名も追加してください。

画像の出典は制作プロジェクトの現行納品動画です。
複素インピーダンスはshort-v2、集中定数回路は改訂29から抽出しています。
切り出し時刻・元動画のハッシュは、制作プロジェクトの `docs/github-pages.md` に記録しています。

埋め込み仕様： [YouTube公式プレーヤー仕様](https://developers.google.com/youtube/player_parameters)、
[Refererの要件](https://developers.google.com/youtube/terms/required-minimum-functionality#embedded-player-api-client-identity)
（2026-09-26確認）。

## GitHub Pagesの初回設定

1. このリポジトリをGitHubへpushします。公開ブランチは `main` です。
2. GitHubの **Settings → Pages → Build and deployment → Source** を **GitHub Actions** にします。
3. **Actions → Deploy static site to GitHub Pages → Run workflow** で `main` を選んで実行します。
4. 成功した実行の `github-pages` 環境に表示される公開URLを確認します。

以降は `main` の `public/` または公開ワークフローを変更してpushすると自動公開します。
公開対象は `public/` だけです。READMEや制作プロジェクトのファイルは配信しません。
公開設定を変えただけではワークフローは実行されないため、初回は手動実行してください。
利用プランによってはPages用リポジトリをpublicにする必要があります。

## 制作プロジェクトからの更新

制作プロジェクトのルートで、サイトの変更を先にcommit・pushします。

```bash
git -C website switch main
git -C website add public
git -C website commit -m "Update website"
git -C website push origin main
git add website
git commit -m "Update website submodule"
```

ワークフローを変更した場合は、サイト側で `.github/workflows/pages.yml` もaddします。
親リポジトリのcommitだけでは、サイトの変更はpush・公開されません。
親が記録するサイトのcommitは、先にサイト用リモートへpushしてください。

仕様確認：2026-09-26、[GitHub公式のPagesワークフロー手順](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。
