#!/usr/bin/env python3
"""
news.json のお知らせを、index.html に「静的なHTML」として書き込むスクリプト。

なぜ必要？
  お知らせは JavaScript（fetch）で news.json を読み込んで表示しているため、
  HTMLのソースには中身が残りません。検索エンジンが確実に読めるよう、
  同じ中身を index.html の <!-- news:begin --> 〜 <!-- news:end --> の間にも書いておきます。
  （ブラウザでは従来どおり JavaScript が最新の news.json で置き換えるので、表示は変わりません）

使い方（news.json を直したら実行）:
  python tools/sync_news.py
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTE = '（tools/sync_news.py が news.json から自動生成。ここは直接編集せず news.json を直して再実行）'

items = json.load(open(os.path.join(ROOT, 'news.json'), encoding='utf-8'))
rows = []
for n in items:
    y, m, d = n['date'].split('-')
    title = html.escape(n['title'], quote=False)
    if n.get('url'):
        title = f'<a class="title" href="{html.escape(n["url"], quote=True)}">{title}</a>'
    else:
        title = f'<span class="title">{title}</span>'
    rows.append(f'<div class="news-item"><span class="date">{y}.{m}.{d}</span>'
                f'<span class="cat">{html.escape(n["category"])}</span>{title}</div>')
block = f'<!-- news:begin{NOTE} -->\n' + '\n'.join(rows) + '\n<!-- news:end -->'

path = os.path.join(ROOT, 'index.html')
src = open(path, encoding='utf-8', newline='').read()
if '<!-- news:begin' not in src:
    raise SystemExit('index.html に <!-- news:begin --> 〜 <!-- news:end --> が見つかりません')
out = re.sub(r'<!-- news:begin.*?<!-- news:end -->', lambda _: block, src, count=1, flags=re.S)
if '\r\n' in src:  # 元の改行コードを維持
    out = out.replace('\r\n', '\n').replace('\n', '\r\n')
if out != src:
    open(path, 'w', encoding='utf-8', newline='').write(out)
    print(f'updated: index.html（お知らせ {len(rows)} 件）')
else:
    print('no change: index.html')
