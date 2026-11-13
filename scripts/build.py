#!/usr/bin/env python3
"""Build with Hugo, then synchronize only managed generated files to Pages root."""
import json, os, shutil, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
manifest=ROOT/'.generated-files.json'
old=set(json.loads(manifest.read_text())) if manifest.exists() else set()
subprocess.run([os.environ.get('HUGO','hugo'),'--cleanDestinationDir','--destination',str(ROOT/'public')],cwd=ROOT,check=True)
new={p.relative_to(ROOT/'public').as_posix() for p in (ROOT/'public').rglob('*') if p.is_file()}
def safe(name):
 p=Path(name)
 if p.is_absolute() or '..' in p.parts or p.parts[0] in {'.git','content','layouts','static','scripts','tests','data','archetypes','hugo-assets'}:raise ValueError('Unsafe generated path: '+name)
 return ROOT/p
for name in old-new:
 target=safe(name)
 if target.is_file():target.unlink()
for name in sorted(new):
 target=safe(name);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'public'/name,target)
manifest.write_text(json.dumps(sorted(new),ensure_ascii=False,indent=2)+'\n')
print(f'Synchronized {len(new)} generated files.')
