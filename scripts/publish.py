#!/usr/bin/env python3
"""Publish verified APK assets, then deploy main:/docs through GitHub Pages.

The website main branch must already exist (initial source push may precede
Pages setup). Later updates publish assets before pushing new versioned links.
Uses the existing gh login; no credentials are written into this repository.
"""
import argparse,hashlib,json,subprocess,time,urllib.request,urllib.parse,concurrent.futures
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];REPO='dk-bluegrain/bsc-pages';RELEASE_INFO=json.loads((ROOT/'src/release.json').read_text());TAG=RELEASE_INFO['tag'];SITE='https://dk-bluegrain.github.io/bsc-pages/'
p=argparse.ArgumentParser();p.add_argument('--apk-directory',type=Path,required=True);p.add_argument('--website-only',action='store_true');a=p.parse_args()
def gh(*args):return subprocess.check_output(['gh',*args],cwd=ROOT,text=True)
def api(path,*args):return gh('api',path,*args)
subprocess.run(['python3','scripts/check.py'],cwd=ROOT,check=True)
assert json.loads(gh('repo','view',REPO,'--json','visibility'))['visibility']=='PUBLIC'
status=subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True)
if status:raise SystemExit('Commit verified website sources and docs before publishing')
expected_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
downloads=json.loads((ROOT/'src/downloads.json').read_text());assets=[]
for data in downloads.values():
 path=a.apk_directory/data['filename'];assert hashlib.sha256(path.read_bytes()).hexdigest()==data['sha256'];assets.append(str(path.resolve()))
checksums=a.apk_directory/'SHA256SUMS';assert checksums.is_file();assets.append(str(checksums.resolve()));assets.append(str(ROOT/'RELEASE-NOTES.md'))
# Push only the verified source tag; Pages remains on the old main until assets are public.
if not a.website_only:subprocess.run(['git','push','origin',f'{expected_commit}:refs/tags/{TAG}'],cwd=ROOT,check=True)
release=subprocess.run(['gh','release','view',TAG,'--repo',REPO,'--json','assets,url,isDraft'],capture_output=True,text=True)
if a.website_only:
 assert release.returncode==0,'Existing public release required for a website-only update'
 data=json.loads(release.stdout);assert not data['isDraft'],'Publish the APK release first'
 by_name={item['name']:item for item in data['assets']}
 for asset in assets:
  path=Path(asset);item=by_name[path.name]
  assert item.get('state')=='uploaded' and item.get('digest')=='sha256:'+hashlib.sha256(path.read_bytes()).hexdigest(),'Existing release asset differs: '+path.name
elif release.returncode:
 subprocess.run(['gh','release','create',TAG,*assets,'--repo',REPO,'--target','main','--prerelease','--title',f"Santa Cruz Modern {RELEASE_INFO['version']} — independent preview",'--notes-file',str(ROOT/'RELEASE-NOTES.md')],check=True)
else:
 data=json.loads(release.stdout);existing={x['name'] for x in data['assets']}
 missing=[p for p in assets if Path(p).name not in existing]
 if missing:subprocess.run(['gh','release','upload',TAG,*missing,'--repo',REPO],check=True)
 # Staged previews must become public before the website links are pushed.
 if data.get('isDraft'):
  # GitHub's upload digest must match every local asset before the preview is published.
  uploaded=json.loads(gh('release','view',TAG,'--repo',REPO,'--json','assets'))['assets']
  by_name={item['name']:item for item in uploaded}
  for asset in assets:
   path=Path(asset);item=by_name[path.name]
   assert item.get('state')=='uploaded' and item.get('digest')=='sha256:'+hashlib.sha256(path.read_bytes()).hexdigest(), 'Incomplete or mismatched release asset: '+path.name
  subprocess.run(['gh','release','edit',TAG,'--repo',REPO,'--target',expected_commit,'--draft=false','--prerelease'],check=True)


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
def verify_document(path):
 relative=path.relative_to(ROOT/'docs').as_posix()
 digest=hashlib.sha256()
 url=SITE+urllib.parse.quote(relative)+'?v='+expected_commit[:12]
 with urllib.request.urlopen(url,timeout=45) as response:
  assert response.status==200
  while block:=response.read(1024*1024):digest.update(block)
 assert digest.hexdigest()==hashlib.sha256(path.read_bytes()).hexdigest(), 'Anonymous deployed file differs: '+relative
 return relative
files=[p for p in (ROOT/'docs').rglob('*') if p.is_file() and not p.name.startswith('.')]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 verified=list(pool.map(verify_document,files))
print('Anonymous deployed files matched:',len(verified))
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
