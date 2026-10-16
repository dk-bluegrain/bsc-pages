#!/usr/bin/env python3
"""Publish verified APK assets, then deploy main:/docs through GitHub Pages.

The website main branch must already exist (initial source push may precede
Pages setup). Later updates publish assets before pushing new versioned links.
Uses the existing gh login; no credentials are written into this repository.
"""
import argparse,hashlib,json,subprocess,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];REPO='dk-bluegrain/bsc-pages';TAG='v1.11.0-preview.1';SITE='https://dk-bluegrain.github.io/bsc-pages/'
p=argparse.ArgumentParser();p.add_argument('--apk-directory',type=Path,required=True);a=p.parse_args()
def gh(*args):return subprocess.check_output(['gh',*args],cwd=ROOT,text=True)
def api(path,*args):return gh('api',path,*args)
subprocess.run(['python3','scripts/check.py'],cwd=ROOT,check=True)
assert json.loads(gh('repo','view',REPO,'--json','visibility'))['visibility']=='PUBLIC'
status=subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True)
if status:raise SystemExit('Commit verified website sources and docs before publishing')
downloads=json.loads((ROOT/'src/downloads.json').read_text());assets=[]
for data in downloads.values():
 path=a.apk_directory/data['filename'];assert hashlib.sha256(path.read_bytes()).hexdigest()==data['sha256'];assets.append(str(path.resolve()))
checksums=a.apk_directory/'SHA256SUMS';assert checksums.is_file();assets.append(str(checksums.resolve()))
release=subprocess.run(['gh','release','view',TAG,'--repo',REPO,'--json','assets,url'],capture_output=True,text=True)
if release.returncode:
 subprocess.run(['gh','release','create',TAG,*assets,'--repo',REPO,'--target','main','--prerelease','--title','Santa Cruz Modern 1.11.0 — independent preview','--notes-file',str(ROOT/'RELEASE-NOTES.md')],check=True)
else:
 data=json.loads(release.stdout);existing={x['name'] for x in data['assets']}
 missing=[p for p in assets if Path(p).name not in existing]
 if missing:subprocess.run(['gh','release','upload',TAG,*missing,'--repo',REPO],check=True)
subprocess.run(['git','push','origin','main'],cwd=ROOT,check=True)
page=subprocess.run(['gh','api',f'repos/{REPO}/pages'],capture_output=True,text=True)
if page.returncode:
 payload=json.dumps({'build_type':'legacy','source':{'branch':'main','path':'/docs'}})
 result=subprocess.run(['gh','api','--method','POST',f'repos/{REPO}/pages','--input','-'],input=payload,text=True,capture_output=True)
 if result.returncode:raise SystemExit(result.stderr)
else:
 data=json.loads(page.stdout)
 assert data['source']=={'branch':'main','path':'/docs'},'Existing Pages source differs; inspect before changing'
 if data.get('build_type')!='legacy':raise SystemExit('Existing Pages deployment type differs')
build_request=subprocess.run(['gh','api',f'repos/{REPO}/pages/builds','--method','POST'],capture_output=True,text=True)
if build_request.returncode and '409' not in build_request.stderr:raise SystemExit(build_request.stderr)
expected_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
for attempt in range(60):
 result=json.loads(api(f'repos/{REPO}/pages/builds/latest'))
 if result['status']=='built' and result.get('commit')==expected_commit:break
 if result['status']=='errored':raise SystemExit(json.dumps(result.get('error')))
 time.sleep(5)
else:raise SystemExit('Pages build still pending; resume verification without rebuilding')
# Anonymous HTTP verification deliberately supplies no GitHub auth headers.
for path in ('','es/','en/','de/','fr/','ru/','uk/','pt/','es/privacy/','media/overview.mp4','media/provenance.json'):
 with urllib.request.urlopen(SITE+path,timeout=45) as response:assert response.status==200
base=f'https://github.com/{REPO}/releases/download/{TAG}/'
with urllib.request.urlopen(base+'SHA256SUMS',timeout=45) as response:published=response.read().decode()
assert published==checksums.read_text(),'Published checksums differ'
for data in downloads.values():
 digest=hashlib.sha256()
 with urllib.request.urlopen(base+data['filename'],timeout=90) as response:
  while block:=response.read(1024*1024):digest.update(block)
 assert digest.hexdigest()==data['sha256'],'Anonymous APK download checksum differs'
print(SITE)
print(f'https://github.com/{REPO}/releases/tag/{TAG}')
print('Anonymous pages, media, privacy, release assets and APK checksums verified.')
