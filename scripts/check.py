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
ux=json.loads((ROOT/'src/ux-copy.json').read_text())['languages']
assert set(ux)==set(content)
assert policy['revision']==4 and len(policy['overview']['excerpts'])==13
for lang,copy in ux.items():
 assert copy.keys()==ux['es'].keys() and len(copy['benefits'])==6
 assert set(copy['chapters'])=={c['id'] for c in policy['chapters']}
 assert [c['id'] for c in copy['overviewCues']]==policy['overview']['chapterOrder']
 assert all(0<len(c['text'])<=160 for c in copy['overviewCues'])
 assert all(b['chapter'] in copy['chapters'] for b in copy['benefits'])

for lang,values in scenario_captions.items():
 assert set(values)==expected_keys and all(0<len(text)<=160 for text in values.values())

class Page(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.video=0;self.tracks=0;self.forms=0;self.ids=[];self.templates=0;self.inert=0;self.previews=0
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='template':self.inert+=1;self.templates+=1
  for key in ('href','src','poster','data-enlarge'):
   if key in d:self.refs.append(d[key])
  if 'id' in d:self.ids.append(d['id'])
  if tag=='video':
   self.video+=1;assert self.inert and 'autoplay' not in d and 'controls' in d and 'playsinline' in d and d.get('preload')=='none'
  if tag=='source':assert self.inert,'Video source must stay in an inert template until Play'
  if tag=='track':self.tracks+=1;assert self.inert
  if 'data-play-video' in d:self.previews+=1;assert tag=='a' and '.mp4?' in d.get('href','')
  self.forms+=tag in ('form','input','iframe')
 def handle_endtag(self,tag):
  if tag=='template':self.inert-=1
for lang,c in content.items():
 assert c.keys()==content['es'].keys()
 assert len(c['chapters'])==13 and [x['id'] for x in c['chapters']]==[x['id'] for x in content['es']['chapters']]
 for path in (DOCS/lang/'index.html',DOCS/lang/'privacy/index.html') + ((DOCS/'index.html',) if lang=='es' else ()):
  s=path.read_text();p=Page();p.feed(s)
  assert f'<html lang="{lang}">' in s and not p.forms
  assert len(p.ids)==len(set(p.ids))
  if path.parent.name!= 'privacy':assert p.video==p.templates==p.previews==14 and p.tracks==98
  for ref in p.refs:
   u=urlsplit(ref)
   if u.scheme or u.netloc:
    assert u.scheme in ('https','mailto'),f'Unexpected remote URI {path} {ref}'
    if '/releases/download/' in ref:assert '/v1.12.1-preview.1/' in ref
    continue
   if not u.path:
    if u.fragment:assert u.fragment in p.ids, (path,ref)
    continue
   target=(path.parent/unquote(u.path)).resolve()
   assert target.is_relative_to(DOCS.resolve()),(path,ref)
   assert target.is_file() or (target/'index.html').is_file(),f'Missing asset/link: {path} {ref}'
for id,info in media.items():
 assert info.get('storyboardRevision')==policy['revision']
 if id!='overview':
  assert info.get('smsPreference')=='SMS'
  assert all(len(s.get('captureBuildSha256',''))==64 and (id=='first-use' or s.get('smsAssistanceEnabled') is True) for s in info['sources'])
  assert all(s.get('recordingMode')=='recording' and (id in ('first-use','login','verification') or s.get('loginInputEvents')==0) for s in info['sources'])
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
overview_events=json.loads((DOCS/'media/events/overview.json').read_text())['events']
for chapter in ('login','transfers'):
 assert any(e['type']=='sms-autofill' and e.get('sourceChapter')==chapter for e in overview_events),('Overview omits actual SMS autofill',chapter)
assert media['overview']['chapters']==policy['overview']['chapterOrder']
assert media['overview']['chapters'][:2]==['login','transfers']
for cut in media['overview']['excerpts']:
 assert cut['start']>=cut['sourceSceneStart'] and cut['start']+cut['duration']<=cut['sourceSceneEnd']+.05,'Overview may not spill into the next scenario'
for chapter,result_cue in [('login','read'),('transfers','receipt')]:
 sms_time=next(e['timeSeconds'] for e in overview_events if e['type']=='sms-autofill' and e.get('sourceChapter')==chapter)
 assert any(e['type']=='hold' and e.get('sourceChapter')==chapter and e.get('cue')==result_cue and e['timeSeconds']>sms_time for e in overview_events),('SMS excerpt must include its actual result',chapter)
for id in ('transfers','payments'):
 assert all(source['requiresSmsAutofill'] for source in media[id]['sources'] if 'ShowcaseMoneyUxTest' in source['test'])
 assert not any('BankingFlowTest' in source['test'] for source in media[id]['sources'])
assert {'sms-wait','sms-filled'}<=set(media['transfers']['featuredFrames'])
for chapter,start,end in [('login',0,14.2),('transfers',13,32.2)]:
 assert any(e['type']=='sms-autofill' and e.get('sourceChapter')==chapter and start<=e['timeSeconds']<=end for e in overview_events)
size=sum(p.stat().st_size for p in DOCS.rglob('*') if p.is_file());assert size<250*1024*1024
for p in ROOT.rglob('*'):
 if not p.is_file() or '.git' in p.parts:continue
 assert p.suffix not in ('.apk','.aab','.jks','.p12','.keystore'),f'Excluded binary in website: {p}'
print(f'Seven languages, privacy routes, links, 14 H.264 videos, 98 caption tracks, no forms, file budgets passed ({size/1024/1024:.1f} MiB).')
