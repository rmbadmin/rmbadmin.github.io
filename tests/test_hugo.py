import unittest,json,re,subprocess,os,hashlib,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class HugoTests(unittest.TestCase):
 def test_hugo_source(self):
  self.assertTrue((R/'hugo.toml').exists())
  self.assertEqual(len(list((R/'content/posts').glob('*.html'))),19)
 def test_title_and_clean_copy(self):
  s=(R/'index.html').read_text()
  self.assertIn('软妹币游戏',s)
  for text in ['软软','数字小天地','保持热爱','慢慢生长','hero-text']:self.assertNotIn(text,s)
 def test_readme_removed(self): self.assertFalse((R/'README.md').exists())
 def test_avatar(self):
  s=(R/'index.html').read_text();match=re.search(r'src="(/avatar-source_[^"]+)"',s)
  self.assertIsNotNone(match);self.assertTrue((R/match[1].lstrip('/')).exists())
 def test_search(self):self.assertEqual(len(json.loads((R/'search.json').read_text())),19)
 def test_frontmatter_metadata(self):
  expected=json.loads((R/'content/site.json').read_text())['posts']
  actual=[]
  for p in sorted((R/'content/posts').glob('*.html')):
   meta,_=json.JSONDecoder().raw_decode(p.read_text());actual.append(meta)
  for e,a in zip(expected,actual):
   for k in ['title','date','url']:self.assertEqual(e[k],a[k])
   self.assertEqual(e['categories'],a['categorylinks']);self.assertEqual(e['tags'],a['taglinks'])
 def test_managed_cleanup_and_reproducibility(self):
  env=dict(os.environ);env['HUGO']=env.get('HUGO','hugo')
  manifest=R/'.generated-files.json';old=manifest.read_bytes();stale=R/'assets/stale-test.txt';unmanaged=R/'assets/preserve-test.txt'
  stale.write_text('old');unmanaged.write_text('keep');files=json.loads(old);files.append('assets/stale-test.txt');manifest.write_text(json.dumps(files))
  try:
   subprocess.run(['python3','scripts/build.py'],cwd=R,env=env,check=True,stdout=subprocess.DEVNULL)
   self.assertFalse(stale.exists());self.assertTrue(unmanaged.exists())
   snap={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in json.loads(manifest.read_text())}
   subprocess.run(['python3','scripts/build.py'],cwd=R,env=env,check=True,stdout=subprocess.DEVNULL)
   self.assertEqual(snap,{p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in snap})
  finally:
   stale.unlink(missing_ok=True);unmanaged.unlink(missing_ok=True)
