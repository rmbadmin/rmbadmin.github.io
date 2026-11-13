#!/usr/bin/env python3
"""Rebuild the static blog, preserving the imported routes and article HTML."""
import json,re,html
from pathlib import Path
from collections import Counter
from urllib.parse import unquote
R=Path(__file__).resolve().parents[1]
data=json.loads((R/'content/site.json').read_text()); posts=data['posts']; byurl={p['url']:p for p in posts}
esc=lambda s:html.escape(str(s),quote=True)
cats={c['url']:unquote(c['url']).removeprefix('/categories/').strip('/').replace('/', ' / ') for p in posts for c in p['categories']}
counts=Counter(c['url'] for p in posts for c in p['categories'])
icons={'sun':'☼','search':'⌕','arrow':'↗'}
def chips(p):return ''.join(f'<a class="chip" href="{esc(c["url"])}">{esc(c["name"])}</a>' for c in p['categories'][:2])
def card(p,n):
 excerpt=p['text'][:110]+'…' if len(p['text'])>110 else p['text']
 return f'''<article class="post-card"><div class="card-top"><span class="date">{p['date'].replace('-',' / ')}</span><span class="post-number">{n:02d}</span></div><h2><a href="{esc(p['url'])}">{esc(p['title'])}</a></h2><p class="excerpt">{esc(excerpt)}</p><div class="card-bottom"><div class="chips">{chips(p)}</div><a class="read-link" href="{esc(p['url'])}" aria-label="阅读 {esc(p['title'])}">阅读全文 <span>↗</span></a></div></article>'''
def comments():return '''<section class="comments panel" id="comments"><div class="section-heading"><span class="eyebrow">LET’S TALK</span><h2>留下你的想法</h2></div><p>使用 GitHub 账号参与讨论，与我交换想法。</p><div id="github-comments"><p class="comment-status">GitHub 留言尚未启用。</p></div></section>'''
def shell(title,body,active='home',outline=False,description='软件、游戏与编程。软妹币玩家的技术笔记与折腾记录。',url='/'):
 nav=''.join(f'<a {"aria-current=\"page\"" if active==k else ""} href="{u}">{t}</a>' for k,u,t in [('home','/','首页'),('archives','/archives/','归档'),('about','/about/','关于')])
 sidebar=f'''<aside class="sidebar"><section class="profile panel"><div class="profile-art"><span class="orb one"></span><span class="orb two"></span><span class="art-code">&lt; / &gt;</span></div><div class="avatar">软</div><h2>软妹币玩家<span class="online" title="持续探索"></span></h2><p class="profile-handle">@rmbadmin</p><p class="bio">写代码，也记录生活。<br>在软件、游戏与二次元之间，<br>保持好奇，慢慢生长。</p><a class="github-link" href="https://github.com/rmbadmin" target="_blank" rel="noopener noreferrer">GitHub <span>↗</span></a><div class="stats"><a href="/archives/"><strong>{len(posts)}</strong>文章</a><a href="/categories/"><strong>{len(cats)}</strong>分类</a><a href="/tags/"><strong>{len(set(t['name'] for p in posts for t in p['tags']))}</strong>标签</a></div></section><section class="topics panel"><h3><span class="tiny-dot"></span>探索分类</h3>{''.join(f'<a href="{esc(n)}"><span>{esc(cats[n])}</span><span>{counts[n]:02d}</span></a>' for n,_ in counts.most_common(6))}<a class="all-topics" href="/categories/">查看全部分类 ↗</a></section>{'<nav class="outline panel" aria-label="文章目录"><h3>本页目录</h3><ol id="outline"></ol></nav>' if outline else '<div class="sidebar-note"><span>✦</span> 把想法写下来，让灵感有迹可循。</div>'}</aside>'''
 return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><meta name="description" content="{esc(description[:160])}"><meta property="og:title" content="{esc(title)} | 软软’s Blog"><meta property="og:description" content="{esc(description[:160])}"><link rel="canonical" href="https://blog.rmbgame.net{esc(url)}"><title>{esc(title)} · 软软’s Blog</title><link rel="icon" href="/favicon.ico"><script src="/assets/theme.js"></script><link rel="stylesheet" href="/assets/style.css"><script src="/assets/app.js" defer></script></head><body><a class="skip-link" href="#main">跳到内容</a><header class="site-header"><div class="header-inner"><a class="brand" href="/"><span class="brand-mark">R<span>·</span></span><span>软软<span class="brand-light">’s Blog</span></span></a><nav class="navigation" aria-label="主导航">{nav}<a href="https://github.com/rmbadmin" target="_blank" rel="noopener noreferrer">GitHub ↗</a></nav><div class="header-actions"><button class="icon-button search-trigger" data-search-open aria-label="搜索文章"><span>⌕</span><span class="search-word">搜索</span><kbd>/</kbd></button><button class="icon-button theme-toggle" data-theme-toggle aria-label="切换深浅主题">◐</button><button class="icon-button menu-toggle" aria-label="展开导航" aria-expanded="false">☰</button></div></div></header><div class="layout">{sidebar}<main id="main" tabindex="-1">{body}</main></div><footer class="site-footer"><span>© 2015–2026 软妹币玩家</span><span>记录 · 分享 · 成长 <span class="footer-dot">✦</span> 保持热爱</span><a href="#top" data-top>回到顶部 ↑</a></footer><dialog id="search-dialog" aria-labelledby="search-title"><div class="search-heading"><h2 id="search-title">搜索文章</h2><button class="icon-button" data-search-close aria-label="关闭搜索">×</button></div><label class="search-label" for="search-input">标题、分类或文章内容</label><input id="search-input" type="search" autocomplete="off" placeholder="试试 C#、Windows、游戏…"><p id="search-status" role="status">输入关键词，找到一段过去的记录。</p><ul id="search-results"></ul></dialog></body></html>'''
for route in data['routes']:
 url=route['url']; kind=route['kind'];title=route.get('title','首页');outline=False;description='软件、游戏与编程。软妹币玩家的技术笔记与折腾记录。'
 if kind=='post':
  p=byurl[url];title=p['title'];description=p['text'];outline=True
  idx=posts.index(p);older=posts[idx+1] if idx+1<len(posts) else None
  body=f'''<article class="article panel"><a class="breadcrumb" href="/archives/">← 返回文章归档</a><div class="article-meta">{p['date']}<span>·</span>{max(1,round(len(p['text'])/450))} 分钟阅读</div><h1>{esc(title)}</h1><div class="chips">{chips(p)}</div><div class="historical-note">这是一篇历史文章，文中的软件版本与链接可能已发生变化。</div><div class="prose" id="article-body">{p['html']}</div><div class="article-end">— 感谢阅读 —</div>{f'<a class="next-post" href="{esc(older["url"])}">继续阅读 <span>{esc(older["title"])}</span> ↗</a>' if older else ''}</article>{comments()}'''
 elif kind=='about':
  title='关于';outline=True
  body=f'''<section class="about-intro panel"><span class="eyebrow">HELLO, WORLD</span><h1>你好，我是<span>软软。</span></h1><p>一名喜欢折腾的 .NET 程序员。<br>这里收藏技术笔记，也留下生活中的小小回声。</p><a class="primary-link" href="https://github.com/rmbadmin">在 GitHub 找到我 ↗</a></section><article class="article panel"><div class="section-heading"><span class="eyebrow">MY STORY</span><h2>一路走来的记录</h2></div><p class="historical-note">以下保留原博客的自我介绍与时间线，其中“目前”等表述属于当年的记录。</p><div class="prose" id="article-body">{route['html']}</div></article>{comments()}'''
 elif kind=='home':
  page=route['page'];selected=posts[(page-1)*10:page*10];title='首页' if page==1 else f'文章 · 第 {page} 页'
  hero='''<section class="hero panel"><div class="hero-text"><div class="eyebrow"><span class="tiny-dot"></span> A LITTLE CORNER OF THE INTERNET</div><h1>记录所思，<br><span>分享所爱。</span></h1><p>关于代码、游戏，以及那些值得记下的瞬间。<br>欢迎来到我的数字小天地。</p><a href="/about/" class="hero-link">认识一下我 <span>↗</span></a></div><div class="hero-art" aria-hidden="true"><div class="orbit orbit-a"></div><div class="orbit orbit-b"></div><div class="code-cube">&lt;/&gt;</div><span class="spark s1">✦</span><span class="spark s2">+</span><span class="art-label">CREATE. PLAY. REPEAT.</span></div></section>''' if page==1 else ''
  body=hero+f'<div class="feed-heading"><h2>最新文章 <span>NOTES & STORIES</span></h2><a href="/archives/">全部归档 ↗</a></div><div class="post-grid">'+''.join(card(p,i+1+(page-1)*10) for i,p in enumerate(selected))+'</div><nav class="pagination" aria-label="分页">'+''.join(f'<a {"aria-current=\"page\"" if page==n else ""} href="{"/" if n==1 else f"/page/{n}/"}">{n:02d}</a>' for n in range(1,(len(posts)+9)//10+1))+'</nav>'
 else:
  selected=[byurl[u] for u in route['posts'] if u in byurl]
  if url=='/archives/':selected=posts
  elif re.fullmatch(r'/archives/\d{4}/',url):selected=[p for p in posts if p['date'].startswith(url.split('/')[2])]
  elif re.fullmatch(r'/archives/\d{4}/\d{2}/',url):selected=[p for p in posts if p['date'].startswith('-'.join(url.split('/')[2:4]))]
  if url in ['/categories/','/tags/']:
   title='分类' if url=='/categories/' else '标签'; vals={x['url']:unquote(x['url']).removeprefix('/categories/').removeprefix('/tags/').strip('/').replace('/', ' / ') for p in posts for x in p['categories' if title=='分类' else 'tags']}
   body=f'<section class="panel listing"><span class="eyebrow">EXPLORE</span><h1>按{title}探索</h1><p class="muted">寻找你感兴趣的那一部分。</p><div class="taxonomy">'+''.join(f'<a href="{esc(k)}">{esc(v)} <span>↗</span></a>' for k,v in vals.items())+'</div></section>'
  else:
   body=f'<section class="panel listing"><span class="eyebrow">THE ARCHIVE</span><h1>{esc(title)}</h1><p class="muted">共 {len(selected)} 篇记录，每一次折腾都有迹可循。</p><div class="archive-list">'+''.join(f'<a href="{esc(p["url"])}"><time>{p["date"]}</time><span>{esc(p["title"])}</span><b>↗</b></a>' for p in selected)+'</div></section>'
 active='about' if kind=='about' else 'home' if kind=='home' else 'archives'
 target=R/url.lstrip('/')/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(shell(title,body,active,outline,description,url))
(R/'assets/search.json').write_text(json.dumps([dict(title=p['title'],url=p['url'],date=p['date'],text=p['text'],categories=[c['name'] for c in p['categories']]) for p in posts],ensure_ascii=False))
print(f'Built {len(data["routes"])} pages, preserved {len(posts)} articles.')
