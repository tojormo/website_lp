#!/usr/bin/env python3
"""
common.js のヘッダー・フッター・ファビコンを、各HTMLに「静的なHTML」として書き込むスクリプト。

なぜ必要？
  common.js は JavaScript でメニュー等を差し込むため、HTMLのソースにはリンクが残りません。
  検索エンジンやSNSのプレビューが確実にリンク・アイコンを読めるよう、同じ中身をHTMLにも書いておきます。
  （ブラウザでは従来どおり common.js が最新の内容で置き換えるので、表示は変わりません）

使い方（common.js のメニュー・フッター・ファビコンを直したら実行）:
  python tools/sync_chrome.py
"""
import re, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = '/'  # サイトのルート（tojormo.com 直下）

js = open(os.path.join(ROOT, 'common.js'), encoding='utf-8').read()

def template(name):
    m = re.search(r'const ' + name + r' = `(.*?)`;', js, re.S)
    if not m:
        raise SystemExit(f'common.js に {name} が見つかりません')
    return m.group(1).strip().replace('${SITE_BASE}', BASE)

header = template('HEADER_HTML')
footer = template('FOOTER_HTML')
ver = re.search(r"const FAVICON_VER = '([^']*)'", js).group(1)
favs = []
for m in re.finditer(r"\{\s*(rel:.*?)\}", js[js.index('const FAVICONS'):js.index('];', js.index('const FAVICONS'))]):
    attrs = dict(re.findall(r"(\w+)\s*:\s*'([^']*)'", m.group(1)))
    attrs['href'] = f"{BASE}{attrs['href']}?v={ver}"
    favs.append('<link ' + ' '.join(f'{k}="{v}"' for k, v in attrs.items()) + '>')
fav_block = '<!-- favicons:begin（tools/sync_chrome.py が common.js から自動生成） -->\n' + '\n'.join(favs) + '\n<!-- favicons:end -->'

NOTE = '（tools/sync_chrome.py が common.js から自動生成。ここは直接編集せず common.js を直して再実行）'
def slot(id_, body):
    return f'<div id="{id_}"><!-- static:begin{NOTE} -->\n{body}\n<!-- static:end --></div>'

files = sorted(glob.glob(os.path.join(ROOT, '*.html')) + glob.glob(os.path.join(ROOT, 'article', '*.html')))
for f in files:
    src = open(f, encoding='utf-8', newline='').read()
    out = src
    for id_, body in (('site-header', header), ('site-footer', footer)):
        pat = re.compile(r'<div id="' + id_ + r'">(?:<!-- static:begin.*?<!-- static:end -->)?</div>', re.S)
        out = pat.sub(lambda _: slot(id_, body), out, count=1)
    if '<!-- favicons:begin' in out:
        out = re.sub(r'<!-- favicons:begin.*?<!-- favicons:end -->', lambda _: fav_block, out, flags=re.S)
    else:
        out = out.replace('</head>', fav_block + '\n</head>', 1)
    if '\r\n' in src:  # 元の改行コードを維持
        out = out.replace('\r\n', '\n').replace('\n', '\r\n')
    if out != src:
        open(f, 'w', encoding='utf-8', newline='').write(out)
        print('updated:', os.path.relpath(f, ROOT))
    else:
        print('no change:', os.path.relpath(f, ROOT))
