import unittest,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class SiteTests(unittest.TestCase):
 def test_manifest(self):
  self.assertTrue((R/'content/site.json').exists(),'preserved content manifest required')
 def test_new_shell(self):
  self.assertIn('data-theme-toggle',(R/'index.html').read_text())
 def test_comments_opt_in(self):
  self.assertTrue((R/'assets/comments.json').exists(),'comment configuration required')
 def test_old_routes(self):
  import subprocess
  paths=subprocess.check_output(['git','ls-tree','-r','--name-only','HEAD'],cwd=R,text=True).splitlines()
  for p in paths:
   if p.endswith('index.html'): self.assertTrue((R/p).exists(),p)
 def test_domain_unchanged(self):
  self.assertEqual((R/'CNAME').read_text(),'blog.rmbgame.net')
 def test_year_archive_has_all_posts(self):
  d=json.loads((R/'content/site.json').read_text());page=(R/'archives/2016/index.html').read_text()
  for p in d['posts']:
   if p['date'].startswith('2016'): self.assertIn('href="'+p['url']+'"',page)
 def test_all_distinct_categories_accessible(self):
  self.assertTrue((R/'categories/index.html').is_file());d=json.loads((R/'content/site.json').read_text());page=__import__('urllib.parse',fromlist=['unquote']).unquote((R/'categories/index.html').read_text())
  for p in d['posts']:
   for c in p['categories']:self.assertIn('href="'+c['url']+'"',page)
 def test_article_html_preserved(self):
  d=json.loads((R/'content/site.json').read_text());self.assertEqual(len(d['posts']),19)
  for p in d['posts']:
   self.assertIn(p['html'],(R/p['url'].lstrip('/')/'index.html').read_text())
 def test_local_links_resolve(self):
  from html.parser import HTMLParser
  from urllib.parse import unquote,urlsplit
  class Links(HTMLParser):
   def __init__(self):super().__init__();self.links=[]
   def handle_starttag(self,tag,attrs):
    for name,value in attrs:
     if tag=='a' and name=='href' and value:self.links.append(value)
  for p in R.rglob('index.html'):
   if 'node_modules' in p.parts:continue
   parser=Links();parser.feed(p.read_text())
   for link in parser.links:
    if link.startswith('/') and not link.startswith('//'):
     target=R/unquote(urlsplit(link).path).lstrip('/')
     if target.is_dir():target=target/'index.html'
     self.assertTrue(target.is_file(),f'{p}: {link}')
 def test_comments_disabled_without_ids(self):
  config=json.loads((R/'assets/comments.json').read_text());self.assertFalse(config['enabled']);self.assertEqual(config['repo'],'rmbadmin/rmbadmin.github.io')
