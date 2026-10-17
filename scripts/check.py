#!/usr/bin/env python3
"""Check static routes, offline assets, media limits, captions and download boundaries."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,subprocess
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
captions=json.loads((ROOT/'src/transcripts.json').read_text())['languages'] if (ROOT/'src/transcripts.json').exists() else json.loads((ROOT/'src/captions.json').read_text())['languages']
content=json.loads((ROOT/'src/content.json').read_text())['languages'];assert set(content)=={'es','en','de','fr','ru','uk','pt'}
media=json.loads((ROOT/'src/media.json').read_text())
scene_captions=json.loads((ROOT/'src/scene-captions.json').read_text())['languages']
assert all(set(v)==set(scene_captions['es']) for v in scene_captions.values())
assert len(media)==14 and 'overview' in media
policy=json.loads((ROOT/'src/video-scripts.json').read_text())
scenario_captions=json.loads((ROOT/'src/scenario-captions.json').read_text())['languages']
expected_keys={f"{c['id']}-{i:02d}" for c in policy['chapters'] for i in range(1,len(c['scenes'])+1)}
assert set(scenario_captions)==set(content)
for lang,values in scenario_captions.items():
 assert set(values)==expected_keys and all(0<len(text)<=160 for text in values.values())

class Page(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.video=0;self.tracks=0;self.forms=0;self.ids=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  for key in ('href','src','poster','data-enlarge'):
   if key in d:self.refs.append(d[key])
  if 'id' in d:self.ids.append(d['id'])
  if tag=='video':
   self.video+=1;assert 'autoplay' not in d and 'controls' in d and 'playsinline' in d
  if tag=='track':self.tracks+=1
  self.forms+=tag in ('form','input','iframe')
for lang,c in content.items():
 assert c.keys()==content['es'].keys()
 assert len(c['chapters'])==13 and [x['id'] for x in c['chapters']]==[x['id'] for x in content['es']['chapters']]
 for path in (DOCS/lang/'index.html',DOCS/lang/'privacy/index.html') + ((DOCS/'index.html',) if lang=='es' else ()):
  s=path.read_text();p=Page();p.feed(s)
  assert f'<html lang="{lang}">' in s and not p.forms
  assert len(p.ids)==len(set(p.ids))
  if path.parent.name!= 'privacy':assert p.video==14 and p.tracks==98
  for ref in p.refs:
   u=urlsplit(ref)
   if u.scheme or u.netloc:
    assert u.scheme in ('https','mailto'),f'Unexpected remote URI {path} {ref}'
    if '/releases/download/' in ref:assert '/v1.12.0-preview.1/' in ref
    continue
   if not u.path:
    if u.fragment:assert u.fragment in p.ids, (path,ref)
    continue
   target=(path.parent/unquote(u.path)).resolve()
   assert target.is_relative_to(DOCS.resolve()),(path,ref)
   assert target.is_file() or (target/'index.html').is_file(),f'Missing asset/link: {path} {ref}'
for id,info in media.items():
 assert info.get('storyboardRevision')==3
 if id!='overview':
  assert info.get('smsPreference')=='SMS'
  assert all(len(s.get('captureBuildSha256',''))==64 and (id=='first-use' or s.get('smsAssistanceEnabled') is True) for s in info['sources'])
  assert all(s.get('smsPreference')=='SMS' and (not s.get('requiresSmsAutofill') or s.get('smsAutofillEvents',0)>0) for s in info['sources'])
 path=DOCS/'media'/f'{id}.mp4';assert path.stat().st_size<100*1024*1024
 result=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
 duration=float(result['format']['duration']);assert duration>=29.9
 if id=='overview':assert 90<=duration<=120
 assert next(x for x in result['streams'] if x['codec_type']=='video')['codec_name']=='h264'
 assert not any(x['codec_type']=='audio' for x in result['streams'])
 events=json.loads((DOCS/'media/events'/f'{id}.json').read_text())['events']
 for event in events:
  assert 0<=event['timeSeconds']<=duration
  if event['type'] in ('tap','swipe'):
   assert 0<event['x']<540 and 0<event['y']<1200,(id,event)
 raw=path.read_bytes();assert raw.index(b'moov')<raw.index(b'mdat'),'MP4 missing fast-start metadata'
 for lang in content:
  vtt=(DOCS/'media/captions'/lang/f'{id}.vtt').read_text();assert vtt.startswith('WEBVTT\n') and '-->' in vtt
  times=re.findall(r'(\d{2}):(\d{2}):(\d{2})\.(\d{3}) --> (\d{2}):(\d{2}):(\d{2})\.(\d{3})',vtt)
  assert times,(lang,id,'missing caption timing')
  previous=0
  for values in times:
   numbers=list(map(int,values));begin=numbers[0]*3600+numbers[1]*60+numbers[2]+numbers[3]/1000;end=numbers[4]*3600+numbers[5]*60+numbers[6]+numbers[7]/1000
   assert previous<=begin<end<=duration+.1,(lang,id,begin,end,duration)
   previous=end
  assert all(cue in vtt for cue in captions[lang][id]),'Captions differ from source transcript'
size=sum(p.stat().st_size for p in DOCS.rglob('*') if p.is_file());assert size<250*1024*1024
for p in ROOT.rglob('*'):
 if not p.is_file() or '.git' in p.parts:continue
 assert p.suffix not in ('.apk','.aab','.jks','.p12','.keystore'),f'Excluded binary in website: {p}'
print(f'Seven languages, privacy routes, links, 14 H.264 videos, 98 caption tracks, no forms, file budgets passed ({size/1024/1024:.1f} MiB).')
