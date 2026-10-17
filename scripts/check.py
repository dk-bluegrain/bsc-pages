#!/usr/bin/env python3
"""Check static routes, offline assets, media limits, captions and download boundaries."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
captions=json.loads((ROOT/'src/transcripts.json').read_text())['languages'] if (ROOT/'src/transcripts.json').exists() else json.loads((ROOT/'src/captions.json').read_text())['languages']
content=json.loads((ROOT/'src/content.json').read_text())['languages'];assert set(content)=={'es','en','de','fr','ru','uk','pt'}
download_copy=json.loads((ROOT/'src/download-copy.json').read_text())
downloads=json.loads((ROOT/'src/downloads.json').read_text())
assert set(download_copy['languages'])==set(content)
for lang,copy in download_copy['languages'].items():
 assert set(copy)==set(download_copy['context'])==set(download_copy['languages']['es'])
 assert all(isinstance(v,str) and v.strip() for key,v in copy.items() if key!='steps')
 assert len(copy['steps'])==6 and all(set(step)=={'title','body'} and all(step.values()) for step in copy['steps'])
 if lang!='en':
  assert all(copy[key]!=download_copy['languages']['en'][key] for key in copy if key!='steps'),(lang,'English fallback')
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
spoken=json.loads((ROOT/'src/narration-copy.json').read_text())
assert set(spoken['languages'])==set(content)
assert all(set(copy)==set(spoken['context']) for copy in spoken['languages'].values())
audio_languages=dict(es='spa',en='eng',de='deu',fr='fra',ru='rus',uk='ukr',pt='por')
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
 def __init__(self):super().__init__();self.refs=[];self.video=0;self.tracks=0;self.forms=0;self.ids=[];self.templates=0;self.inert=0;self.previews=0;self.sources=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='template':self.inert+=1;self.templates+=1
  for key in ('href','src','poster','data-enlarge'):
   if key in d:self.refs.append(d[key])
  if 'id' in d:self.ids.append(d['id'])
  if tag=='video':
   self.video+=1;assert self.inert and 'autoplay' not in d and 'controls' in d and 'playsinline' in d and d.get('preload')=='none'
  if tag=='source':
   assert self.inert,'Video source must stay in an inert template until Play'
   self.sources.append(d['src'])
  if tag=='track':self.tracks+=1;assert self.inert
  if 'data-play-video' in d:self.previews+=1;assert tag=='a' and '.mp4?' in d.get('href','')
  self.forms+=tag in ('form','input','iframe')
 def handle_endtag(self,tag):
  if tag=='template':self.inert-=1
for lang,c in content.items():
 assert c.keys()==content['es'].keys()
 assert len(c['chapters'])==13 and [x['id'] for x in c['chapters']]==[x['id'] for x in content['es']['chapters']]
 for path in (DOCS/lang/'index.html',DOCS/lang/'privacy/index.html',DOCS/lang/'download/index.html') + ((DOCS/'index.html',) if lang=='es' else ()):
  s=path.read_text();p=Page();p.feed(s)
  assert f'<html lang="{lang}">' in s and not p.forms
  assert len(p.ids)==len(set(p.ids))
  if path.parent.name not in ('privacy','download'):
   assert p.video==p.templates==p.previews==14 and p.tracks==98
   assert all(f'/narrated/{lang}/' in src for src in p.sources),'Page must use its own narrated language'
   assert not any(urlsplit(ref).path.endswith('.apk') for ref in p.refs),'Landing pages must show the edition choice before APK downloads'
   assert f'href="{"./" if path==DOCS/"index.html" else "../"}{lang}/download/"' in s
  if path.parent.name=='download':
   assert p.video==p.templates==p.previews==0
   assert {'demo','live-guide','installation','live-download'}<=set(p.ids)
   assert sum(ref.endswith('-demo.apk') for ref in p.refs)==1
   assert sum(ref.endswith('-live.apk') for ref in p.refs)==1
   assert s.index('id="live-guide"')<s.index('class="download-section risk-notice"')<s.index('id="installation"')<s.index('id="live-download"')
   assert all(data['sha256'] in s and data['filename'] in s for data in downloads.values())
   assert not any('/media/install/' in ref for ref in p.refs)
   assert s.count('class="app-shot"')==4
   for file in ('first-use-01.jpg','accounts-01.jpg','history-03.jpg','first-use-09.jpg'):
    assert sum(urlsplit(ref).path.endswith('/'+file) for ref in p.refs)==2
    assert any(file in chapter['screenshots'] for chapter in media.values())
   assert f'href="../../{lang}/download/"' in s
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
 if id=='overview':assert 60<=duration<=120
 assert next(x for x in result['streams'] if x['codec_type']=='video')['codec_name']=='h264'
 assert not any(x['codec_type']=='audio' for x in result['streams'])
 pacing=info['pacing'];assert pacing['actionsAtOriginalSpeed'] and duration<pacing['sourceDuration']
 cuts=pacing['cuts'];assert all(0<=cut['start']<cut['end']<=pacing['sourceDuration'] for cut in cuts)
 assert all(a['end']<=b['start'] for a,b in zip(cuts,cuts[1:]))
 assert abs(pacing['sourceDuration']-duration-sum(c['end']-c['start'] for c in cuts))<.08
 assert abs(info['duration']-duration)<.01
 assert set(info['narration']['languages'])==set(content)
 events=json.loads((DOCS/'media/events'/f'{id}.json').read_text())['events']
 for event in events:
  assert 0<=event['timeSeconds']<=duration
  source_time=event['sourceTimeSeconds']
  expected_time=source_time-sum(max(0,min(source_time,c['end'])-c['start']) for c in cuts)
  assert abs(event['timeSeconds']-expected_time)<.002,(id,event,'bad edited event time')
  if event['type'] not in ('hold','screenshot'):
   assert not any(c['start']<=source_time<c['end'] for c in cuts),'A recorded action was removed'
  if event['type'] in ('tap','swipe'):
   assert 0<event['x']<540 and 0<event['y']<1200,(id,event)
 raw=path.read_bytes();assert raw.index(b'moov')<raw.index(b'mdat'),'MP4 missing fast-start metadata'
 for lang in content:
  speech=info['narration']['languages'][lang]
  voiced=DOCS/'media'/speech['file']
  assert speech['file']==f'narrated/{lang}/{id}.mp4'
  assert voiced.stat().st_size==speech['bytes']<100*1024*1024
  assert hashlib.sha256(voiced.read_bytes()).hexdigest()==speech['sha256']
  voiced_info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(voiced)]))
  assert abs(float(voiced_info['format']['duration'])-duration)<.1
  assert next(s for s in voiced_info['streams'] if s['codec_type']=='video')['codec_name']=='h264'
  audio=next(s for s in voiced_info['streams'] if s['codec_type']=='audio')
  assert audio['codec_name']=='aac' and audio['channels']==1 and audio['sample_rate']=='24000'
  assert audio['tags']['language']==audio_languages[lang],(id,lang,audio.get('tags'))
  previous=0
  for cue in speech['cues']:
   assert previous<=cue['start']<cue['end']<=duration+.01,(id,lang,cue)
   previous=cue['end']
  scenes=range(1,len(info['excerpts' if id=='overview' else 'sources'])+1)
  assert {c['scene'] for c in speech['cues'] if c['summary']}==set(scenes),'Every scene needs a localized spoken summary'
  voiced_raw=voiced.read_bytes();assert voiced_raw.index(b'moov')<voiced_raw.index(b'mdat')
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
for chapter in ('login','transfers'):
 excerpt=next(e for e in media['overview']['excerpts'] if e['chapter']==chapter)
 start=excerpt['playbackStart'];end=start+excerpt['playbackDuration']
 assert any(e['type']=='sms-autofill' and e.get('sourceChapter')==chapter and start<=e['timeSeconds']<=end for e in overview_events)
size=sum(p.stat().st_size for p in DOCS.rglob('*') if p.is_file());assert size<250*1024*1024
for p in ROOT.rglob('*'):
 if not p.is_file() or '.git' in p.parts:continue
 assert p.suffix not in ('.apk','.aab','.jks','.p12','.keystore'),f'Excluded binary in website: {p}'
print(f'Seven languages, privacy routes, links, 14 paced videos, 98 narrated H.264/AAC videos, 98 caption tracks, action timing, no forms and file budgets passed ({size/1024/1024:.1f} MiB).')
