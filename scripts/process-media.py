#!/usr/bin/env python3
"""Encode approved native captures, posters, localized captions and a 104-second overview."""
import argparse,json,math,subprocess,tempfile,shutil,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--captures',type=Path,action='append',required=True);p.add_argument('--chapter',action='append');p.add_argument('--captions-only',action='store_true');a=p.parse_args()
ROOT=Path(__file__).resolve().parents[1];MEDIA=ROOT/'docs/media';MEDIA.mkdir(parents=True,exist_ok=True)
scene_captions=json.loads((ROOT/'src/scene-captions.json').read_text())['languages']
scenario_captions=json.loads((ROOT/'src/scenario-captions.json').read_text())['languages'] if (ROOT/'src/scenario-captions.json').exists() else {}
transcripts=json.loads((ROOT/'src/transcripts.json').read_text())['languages'] if a.chapter and (ROOT/'src/transcripts.json').exists() else {lang:{} for lang in scene_captions}
content=json.loads((ROOT/'src/content.json').read_text())['languages'];captions=json.loads((ROOT/'src/captions.json').read_text())['languages']
ids=[c['id'] for c in content['es']['chapters']];requested=a.chapter or ids
assert len(requested)==len(set(requested)) and set(requested)<=set(ids),'Unknown/repeated chapter'
policy=json.loads((ROOT/'src/video-scripts.json').read_text());script_hash=hashlib.sha256((ROOT/'src/video-scripts.json').read_bytes()).hexdigest()
expected={c['id']:len(c['scenes']) for c in policy['chapters']};approved={}
for folder in a.captures:
 for metadata in sorted(folder.glob('*/complete.json')):
  info=json.loads(metadata.read_text());assert info['passed'] and info['fictional'] and info['nativeTapOverlay'] and info.get('inputMarkerVersion')==2 and info.get('storyboardRevision')==3 and info.get('smsPreference')=='SMS' and info.get('manualBankSmsTyping') is False and (info['chapter']=='first-use' or info.get('smsAssistanceEnabled') is True), 'Capture requires synchronized input markers'
  approved[(info['chapter'],info['scenario'])]=(metadata.parent,info)
def run(*args):subprocess.run(list(args),check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def probe(path):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(path)]))
def align_first_ring(path,events,epoch):
 taps=[e for e in events if e['type']=='tap']
 if not taps:return 0.0,None
 # Some first taps close their native window before its overlay reaches a frame.
 # Calibrate against an actually visible recorded marker, retaining every input event.
 for first in taps[:8]:
  estimate=(first['epochMs']-epoch)/1000;begin=max(0,estimate-1)
  x=max(0,min(440,round(first['x']/2)-50));y=max(0,min(1100,round(first['y']/2)-50))
  data=subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error','-i',str(path),'-vf',f'scale=540:1200,crop=100:100:{x}:{y},fps=30:start_time=0,trim=start={begin}:duration=2,setpts=PTS-STARTPTS','-frames:v','60','-f','rawvideo','-pix_fmt','rgb24','pipe:1'])
  size=100*100*3
  counts=[]
  for i in range(len(data)//size):
   frame=memoryview(data)[i*size:(i+1)*size];count=0
   for j in range(0,size,3):
    if 175<=frame[j]<=235 and frame[j+1]>=243 and 75<=frame[j+2]<=180:count+=1
   counts.append(count)
  baseline=max(counts[:18],default=0)
  for i,count in enumerate(counts[18:],18):
   if count>=baseline+5:
    observed=begin+i/30;difference=observed-estimate
    if abs(difference)<=.35:return difference,round(observed,3)
 raise RuntimeError('Could not locate any early native input marker in '+str(path))

def write_touch_overlay(path,events):
 # Native frame markers calibrate actual event time. This persistent final layer
 # keeps each ring visible for one second even when a dialog/window closes.
 header="""[Script Info]
ScriptType: v4.00+
PlayResX: 540
PlayResY: 1200
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Tap,DejaVu Sans,20,&H0080FFCC,&H0080FFCC,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0.7,0,5,0,0,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
 def ass_time(t):
  centi=round(t*100);return f'{centi//360000}:{centi//6000%60:02d}:{centi//100%60:02d}.{centi%100:02d}'
 # Opposite winding leaves a transparent center, producing a vector ring.
 shape='m 0 14 b 0 6.268 6.268 0 14 0 b 21.732 0 28 6.268 28 14 b 28 21.732 21.732 28 14 28 b 6.268 28 0 21.732 0 14 m 3 14 b 3 20.075 7.925 25 14 25 b 20.075 25 25 20.075 25 14 b 25 7.925 20.075 3 14 3 b 7.925 3 3 7.925 3 14'
 lines=[header]
 for e in events:
  if e['type']!='tap':continue
  t=e['timeSeconds'];x=e['x'];y=e['y']
  tags=rf'{{\an5\pos({x},{y})\fscx50\fscy50\t(0,1000,\fscx264\fscy264\alpha&HFF&)\p1}}'
  lines.append(f'Dialogue: 10,{ass_time(t)},{ass_time(t+1)},Tap,,0,0,0,,{tags}{shape}\n')
 path.write_text(''.join(lines))

def stamp(value):
 ms=round(value*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d}.{ms%1000:03d}'
def vtt(id,duration,events):
 for lang,chapters in captions.items():
  base=chapters[id];folder=MEDIA/'captions'/lang;folder.mkdir(parents=True,exist_ok=True)
  cues=[]
  if id=='overview':
   position=0.0
   segments=manifest.get('overview',{}).get('excerpts',[])
   for i,text in enumerate(base):
    seconds=segments[i]['duration'] if segments else 8
    cues.append((position,min(duration,position+seconds),text));position+=seconds
  else:
   special=[e for e in events if e['type']=='hold' and e.get('cue') not in ('read','navigation','opening') and e.get('durationMs',0)>=3000]
   points={0.0,duration,max(0,duration-6)}
   starts=sorted((e for e in events if e['type']=='scene-start'),key=lambda e:e['timeSeconds'])
   if scenario_captions:
    for e in starts:points.add(max(0,min(duration,e['timeSeconds'])))
   else:
    for i in range(1,len(base)):points.add(duration*i/len(base))
   for e in special:
    points.add(max(0,min(duration,e['timeSeconds'])));points.add(max(0,min(duration,e['timeSeconds']+e['durationMs']/1000)))
   bounds=sorted(points)
   for begin,end in zip(bounds,bounds[1:]):
    if end-begin<.05:continue
    middle=(begin+end)/2;index=min(len(base)-1,int(middle/duration*len(base)))
    text=base[index]
    if scenario_captions:
     scene=next((e for e in reversed(starts) if e['timeSeconds']<=middle),starts[0])
     text=scenario_captions[lang][f"{id}-{scene['scenario']:02d}"]
    active=[e for e in special if e['timeSeconds']<=middle<e['timeSeconds']+e['durationMs']/1000]
    if active and middle<duration-6:text=scene_captions[lang][active[-1]['cue']]
    if cues and cues[-1][2]==text:cues[-1]=(cues[-1][0],end,text)
    else:cues.append((begin,end,text))
   # Avoid a brief summary flash between two important scripted reading holds.
   for i in range(len(cues)-1,-1,-1):
    begin,end,text=cues[i]
    if end-begin<2.4 and i>0:
     previous=cues[i-1];cues[i-1]=(previous[0],end,previous[2]);cues.pop(i)
  lines=['WEBVTT','']
  for i,(begin,end,text) in enumerate(cues):lines.extend([str(i+1),f'{stamp(begin)} --> {stamp(max(begin+.05,end-.05))}',text,''])
  (folder/f'{id}.vtt').write_text('\n'.join(lines))
  transcripts[lang][id]=list(dict.fromkeys(text for _,_,text in cues))

manifest=json.loads((ROOT/'src/media.json').read_text()) if a.chapter and (ROOT/'src/media.json').exists() else {}
if a.captions_only:
 manifest=json.loads((ROOT/'src/media.json').read_text())
 for id in requested + ([] if a.chapter else ['overview']):
  events=json.loads((MEDIA/'events'/f'{id}.json').read_text())['events']
  vtt(id,manifest[id]['duration'],events)
 (ROOT/'src/transcripts.json').write_text(json.dumps({'languages':transcripts},ensure_ascii=False,indent=2)+'\n')
 print('Scene-timed captions and matching transcripts refreshed.')
 raise SystemExit(0)

with tempfile.TemporaryDirectory(prefix='bsc-media-') as temp:
 temp=Path(temp)
 for id in requested:
  selections=[(key,pair) for key,pair in sorted(approved.items()) if key[0]==id]
  assert [key[1] for key,pair in selections]==list(range(1,expected[id]+1)), 'Missing scripted scene for '+id
  assert all(pair[1]['scriptSha256']==script_hash for key,pair in selections),'Capture script mismatch for '+id
  for old in MEDIA.glob(f'{id}-*.jpg'):old.unlink()
  clips=[];events=[];shots=[];sources=[];offset=0
  for (_,index),(folder,info) in selections:
   raw=folder/'raw.mp4';source_events=[json.loads(s) for s in (folder/'captures/events.jsonl').read_text().splitlines()] if (folder/'captures/events.jsonl').exists() else []
   raw_duration=probe(raw)
   alignment,first_ring=align_first_ring(raw,source_events,info['recordingStartEpochMs'])
   opening=next(e for e in source_events if e['type']=='scene-start')
   ending=next(e for e in reversed(source_events) if e['type']=='scene-end')
   start=max(0,(opening['epochMs']-info['recordingStartEpochMs'])/1000+alignment-.15)
   end=min(raw_duration,(ending['epochMs']-info['recordingStartEpochMs'])/1000+alignment+.1);duration=end-start
   # Ring overlays are rendered in Android at the actual touch, retained in the footage.
   clip=temp/f'{id}-{index}.mp4'
   run('ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(raw),'-t',str(duration),'-vf',f'scale=540:1200,fps=15:start_time=0,trim=start={start}:end={end},setpts=PTS-STARTPTS','-an','-c:v','libx264','-preset','veryfast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(clip));clips.append(clip)
   actual_duration=probe(clip)
   for e in source_events:
    t=(e['epochMs']-info['recordingStartEpochMs'])/1000+alignment-start+offset
    if 0<=t<=offset+actual_duration:
     item={'type':e['type'],'timeSeconds':round(t,3),'epochMs':e['epochMs'],'scenario':index}
     for key in ('x','y','endX','endY'):
      if key in e:item[key]=round(e[key]/2,2)
     if 'characters' in e:item['characters']=e['characters']
     for key in ('cue','durationMs','method','manualTyping','preferredMedium','action'):
      if key in e:item[key]=e[key]
     events.append(item)
   images=sorted((folder/'captures').glob('screen-*.png'))
   if images:
    # Select a few actual captured screens per segment; no generated banking UI.
    picks=sorted(set([min(1,len(images)-1),len(images)//2,max(0,len(images)-1)]))
    for pos in picks:
     name=f'{id}-{len(shots)+1:02d}.jpg'
     run('ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(images[pos]),'-vf','scale=540:-2','-frames:v','1','-q:v','3',str(MEDIA/name));shots.append(name)
   sources.append({'test':info['test'],'emulator':info['emulator'],'passed':True,'scenario':index,'scriptSha256':info['scriptSha256'],'smsPreference':info['smsPreference'],'smsAssistanceEnabled':info.get('smsAssistanceEnabled',False),'captureBuildSha256':info.get('captureBuildSha256'),'smsAutofillEvents':info['smsAutofillEvents'],'requiresSmsAutofill':info['requiresSmsAutofill'],'firstNativeRingVideoTime':first_ring,'eventAlignmentOffset':round(alignment,3),'trimStart':round(start,3),'duration':round(actual_duration,3)})
   offset+=actual_duration
  concat=temp/f'{id}.txt';concat.write_text(''.join("file '"+str(c)+"'\n" for c in clips))
  target=MEDIA/f'{id}.mp4'
  touch_overlay=temp/f'{id}-touches.ass';write_touch_overlay(touch_overlay,events)
  # A short chapter holds its real final frame to remain readable for at least30s.
  run('ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-vf',f'tpad=stop_mode=clone:stop_duration=30,ass={touch_overlay}','-t',str(max(30,offset)),'-an','-c:v','libx264','-preset','veryfast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(target))
  duration=probe(target);poster=MEDIA/f'{id}.jpg';shutil.copy2(MEDIA/shots[min(1,len(shots)-1)],poster)
  (MEDIA/'events').mkdir(exist_ok=True);(MEDIA/'events'/f'{id}.json').write_text(json.dumps({'coordinateSpace':{'width':540,'height':1200},'timing':'Epoch events retained; MP4 offsets aligned to the first observed native ring at30fps. Android records each actual input and native marker. A persistent one-second overlay follows those same events across native window handoffs.','events':events},indent=2)+'\n')
  manifest[id]={'duration':round(duration,3),'durationLabel':f'{int(duration)//60}:{int(duration)%60:02d}','screenshots':shots,'sources':sources,'fictional':True,'nativeTapOverlay':True,'persistentFinalMarkers':True,'storyboardRevision':3,'smsPreference':'SMS','assetRevision':selections[0][1][1]['scriptSha256'][:12]}
  vtt(id,duration,events);print(id,manifest[id]['durationLabel'],flush=True)
 ready=all(manifest.get(id,{}).get('storyboardRevision')==policy['revision'] and manifest[id].get('assetRevision')==script_hash[:12] and len(manifest[id].get('sources',[]))==expected[id] for id in ids)
 if ready:
  # Overview: thirteen8-second segments in the documented chapter order, no speedup.
  overview=[];overview_events=[];excerpts=[]
  for id in ids:
   source=MEDIA/f'{id}.mp4';duration=manifest[id]['duration'];clip=temp/f'overview-{id}.mp4'
   starts=json.loads((ROOT/'src/overview-starts.json').read_text()) if (ROOT/'src/overview-starts.json').exists() else {}
   chapter_events=json.loads((MEDIA/'events'/f'{id}.json').read_text())['events']
   preferred_hold=next((e for e in chapter_events if e['type']=='hold' and e.get('cue')=='sms-filled'),None)
   if preferred_hold is None:preferred_hold=next((e for e in chapter_events if e['type']=='hold' and e.get('cue') in ('review','consent','receipt','configuration') and e.get('durationMs',0)>=8000),None)
   preferred=min(max(0,preferred_hold['timeSeconds'] if preferred_hold else starts.get(id,duration*.3)),duration-8)
   start=preferred
   for step in range(81):
    delta=(step+1)//2*.1*(1 if step%2 else -1)
    candidate=min(max(0,preferred+delta),duration-8)
    inputs=[e['timeSeconds'] for e in chapter_events if e['type'] in ('tap','swipe')]
    if not any(0<candidate-t<1.05 or 7.0<t-candidate<8.05 for t in inputs):
     start=candidate;break
   run('ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(start),'-i',str(source),'-t','8','-an','-c:v','libx264','-preset','veryfast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(clip))
   actual=probe(clip);position=sum(e['duration'] for e in excerpts)
   excerpts.append({'chapter':id,'start':round(start,3),'duration':round(actual,3),'overviewStart':round(position,3)})
   for event in chapter_events:
    if start<=event['timeSeconds']<start+actual:
     overview_events.append(dict(event,timeSeconds=round(event['timeSeconds']-start+position,3),sourceChapter=id))
   overview.append(clip)
  concat=temp/'overview.txt';concat.write_text(''.join("file '"+str(c)+"'\n" for c in overview))
  run('ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(MEDIA/'overview.mp4'))
  (MEDIA/'events/overview.json').write_text(json.dumps({'coordinateSpace':{'width':540,'height':1200},'events':overview_events},indent=2)+'\n')
  duration=probe(MEDIA/'overview.mp4');shutil.copy2(MEDIA/'accounts.jpg',MEDIA/'overview.jpg');manifest['overview']={'duration':round(duration,3),'durationLabel':'1:44','chapters':ids,'excerpts':excerpts,'fictional':True,'storyboardRevision':3,'assetRevision':manifest['accounts']['assetRevision']};vtt('overview',duration,overview_events)
  shutil.copy2(MEDIA/'accounts-01.jpg',MEDIA/'hero.jpg')
(ROOT/'src/transcripts.json').write_text(json.dumps({'languages':transcripts},ensure_ascii=False,indent=2)+'\n')
(ROOT/'src/media.json').write_text(json.dumps(manifest,indent=2)+'\n')
(MEDIA/'provenance.json').write_text(json.dumps({'appVersion':'1.12.0 (27)','sourceCommit':'6ee13357218005e84c3719d5ac5ff7714af83390','sourceRepository':'https://github.com/dk-bluegrain/bsc','capture':'Scripted native Android instrumentation; fictional identities, synthetic PDFs and fake bank transports only. Capture-only QA builds are identified by each source APK digest; distribution hashes are listed separately in downloads.json.','storyboardRevision':3,'smsPolicy':'SMS assistance enabled outside initial pre-choice onboarding and the settings off/on demonstration; SMS delivery restored after configuration. Fake keyboard autofill retains Verify; a separate synthetic one-message consent result completes only SMS-only login automatically. Offline demo and generated token codes are distinct.','audio':'Silent: no music or narration.','security':'Only a disposable QA checkout permits screenshots. Distribution live screens retain FLAG_SECURE.','notEvidenceOf':'Bank authorization, owner-account validation, current live compatibility, or inclusion of all advanced flows in the basic demo.','chapters':manifest},indent=2)+'\n')
print('Scripted chapters exported; overview ready:',ready)
