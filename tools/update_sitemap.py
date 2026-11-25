#!/usr/bin/env python3
"""
sitemap.xml の <lastmod>（最終更新日）を、各ページの実際の更新日に合わせるスクリプト。

  ・コミット済みで変更のないページ … 最後にコミットした日（git の記録）
  ・編集中（未コミット）のページ   … 今日の日付
  ・git が使えない環境             … ファイルの更新日

sitemap.xml に載っていないページは追加しません（新しいページは <url> を1つ手で追記してください）。

使い方（ページを直したら、コミットの前に実行）:
  python tools/update_sitemap.py
"""
import datetime, os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://tojormo.com/'

def git(*args):
    try:
        r = subprocess.run(['git', '-C', ROOT, *args], capture_output=True, text=True, encoding='utf-8')
        return r.stdout.strip() if r.returncode == 0 else None
    except OSError:
        return None

def lastmod(rel):
    full = os.path.join(ROOT, rel)
    if not os.path.exists(full):
        return None
    status = git('status', '--porcelain', '--', rel)
    if status is None:                      # git が使えない
        return datetime.date.fromtimestamp(os.path.getmtime(full)).isoformat()
    if status:                              # 未コミットの変更あり
        return datetime.date.today().isoformat()
    return git('log', '-1', '--format=%cs', '--', rel) or datetime.date.today().isoformat()

path = os.path.join(ROOT, 'sitemap.xml')
src = open(path, encoding='utf-8', newline='').read()

def fix(m):
    loc = m.group(2)
    rel = loc[len(SITE):] if loc.startswith(SITE) else None
    if rel is None:
        return m.group(0)
    if rel == '' or rel.endswith('/'):
        rel += 'index.html'
    d = lastmod(rel)
    if d is None:
        print('見つかりません（sitemap.xml を確認）:', loc)
        return m.group(0)
    if d != m.group(4):
        print(f'{m.group(4)} → {d}  {loc}')
    return m.group(1) + loc + m.group(3) + d + m.group(5)

out = re.sub(r'(<loc>)(.*?)(</loc>\s*<lastmod>)(.*?)(</lastmod>)', fix, src, flags=re.S)
if out != src:
    open(path, 'w', encoding='utf-8', newline='').write(out)
    print('updated: sitemap.xml')
else:
    print('no change: sitemap.xml')
