#!/usr/bin/env python3
"""Encode approved native captures, posters, localized captions and a 104-second overview."""
import argparse,json,math,subprocess,tempfile,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--captures',type=Path,action='append',required=True);a=p.parse_args()
ROOT=Path(__file__).resolve().parents[1];MEDIA=ROOT/'docs/media';MEDIA.mkdir(parents=True,exist_ok=True)
content=json.loads((ROOT/'src/content.json').read_text())['languages'];captions=json.loads((ROOT/'src/captions.json').read_text())['languages']
ids=[c['id'] for c in content['es']['chapters']];approved={}
for folder in a.captures:
 for metadata in sorted(folder.glob('*/complete.json')):
  info=json.loads(metadata.read_text());assert info['passed'] and info['fictional'] and info['nativeTapOverlay'] and info.get('inputMarkerVersion')==2, 'Capture requires synchronized input markers'
  approved[(info['chapter'],info['scenario'])]=(metadata.parent,info)
def run(*args):subprocess.run(list(args),check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def probe(path):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(path)]))
def align_first_ring(path,events,epoch):
 taps=[e for e in events if e['type']=='tap']
 if not taps:return 0.0,None
 first=taps[0];estimate=(first['epochMs']-epoch)/1000;begin=max(0,estimate-1)
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
 raise RuntimeError('Could not locate the first native input ring in '+str(path))

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
def vtt(id,duration):
 for lang,chapters in captions.items():
  cues=chapters[id];folder=MEDIA/'captions'/lang;folder.mkdir(parents=True,exist_ok=True)
  step=8 if id=='overview' else duration/len(cues)
  lines=['WEBVTT','']
  for i,cue in enumerate(cues):lines.extend([str(i+1),f'{stamp(i*step)} --> {stamp(min(duration,(i+1)*step-.1))}',cue,''])
  (folder/f'{id}.vtt').write_text('\n'.join(lines))
manifest={}
with tempfile.TemporaryDirectory(prefix='bsc-media-') as temp:
 temp=Path(temp)
 for id in ids:
  selections=[(key,pair) for key,pair in sorted(approved.items()) if key[0]==id]
  if not selections:raise SystemExit('No approved capture for '+id)
  clips=[];events=[];shots=[];sources=[];offset=0
  for (_,index),(folder,info) in selections:
   raw=folder/'raw.mp4';source_events=[json.loads(s) for s in (folder/'captures/events.jsonl').read_text().splitlines()] if (folder/'captures/events.jsonl').exists() else []
   raw_duration=probe(raw)
   alignment,first_ring=align_first_ring(raw,source_events,info['recordingStartEpochMs'])
   earliest=min(((e['epochMs']-info['recordingStartEpochMs'])/1000+alignment for e in source_events),default=1.4)
   start=max(0,earliest-1.4);end=max(start+1,raw_duration-1.0);duration=end-start
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
     events.append(item)
   images=sorted((folder/'captures').glob('screen-*.png'))
   if images:
    # Select a few actual captured screens per segment; no generated banking UI.
    picks=sorted(set([min(1,len(images)-1),len(images)//2,max(0,len(images)-1)]))
    for pos in picks:
     name=f'{id}-{len(shots)+1:02d}.jpg'
     run('ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(images[pos]),'-vf','scale=540:-2','-frames:v','1','-q:v','3',str(MEDIA/name));shots.append(name)
   sources.append({'test':info['test'],'emulator':info['emulator'],'passed':True,'scenario':index,'firstNativeRingVideoTime':first_ring,'eventAlignmentOffset':round(alignment,3),'trimStart':round(start,3),'duration':round(actual_duration,3)})
   offset+=actual_duration
  concat=temp/f'{id}.txt';concat.write_text(''.join("file '"+str(c)+"'\n" for c in clips))
  target=MEDIA/f'{id}.mp4'
  touch_overlay=temp/f'{id}-touches.ass';write_touch_overlay(touch_overlay,events)
  # A short chapter holds its real final frame to remain readable for at least30s.
  run('ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-vf',f'tpad=stop_mode=clone:stop_duration=30,ass={touch_overlay}','-t',str(max(30,offset)),'-an','-c:v','libx264','-preset','veryfast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(target))
  duration=probe(target);poster=MEDIA/f'{id}.jpg';shutil.copy2(MEDIA/shots[min(1,len(shots)-1)],poster)
  (MEDIA/'events').mkdir(exist_ok=True);(MEDIA/'events'/f'{id}.json').write_text(json.dumps({'coordinateSpace':{'width':540,'height':1200},'timing':'Epoch events retained; MP4 offsets aligned to the first observed native ring at30fps. Rings are synchronized in the input action inside Android, not reconstructed in post-production.','events':events},indent=2)+'\n')
  manifest[id]={'duration':round(duration,3),'durationLabel':f'{int(duration)//60}:{int(duration)%60:02d}','screenshots':shots,'sources':sources,'fictional':True,'nativeTapOverlay':True,'persistentFinalMarkers':True}
  vtt(id,duration);print(id,manifest[id]['durationLabel'],flush=True)
 # Overview: thirteen8-second segments in the documented chapter order, no speedup.
 overview=[];overview_events=[];excerpts=[]
 for id in ids:
  source=MEDIA/f'{id}.mp4';duration=manifest[id]['duration'];clip=temp/f'overview-{id}.mp4'
  starts=json.loads((ROOT/'src/overview-starts.json').read_text()) if (ROOT/'src/overview-starts.json').exists() else {}
  preferred=min(max(0,starts.get(id,duration*.3)),duration-8)
  chapter_events=json.loads((MEDIA/'events'/f'{id}.json').read_text())['events']
  start=preferred
  for step in range(81):
   delta=(step+1)//2*.1*(1 if step%2 else -1)
   candidate=min(max(0,preferred+delta),duration-8)
   inputs=[e['timeSeconds'] for e in chapter_events if e['type'] in ('tap','swipe')]
   if not any(0<candidate-t<1.05 or 7.0<t-candidate<8.05 for t in inputs):
    start=candidate;break
  excerpts.append({'chapter':id,'start':round(start,3),'duration':8})
  for event in chapter_events:
   if start<=event['timeSeconds']<start+8:
    overview_events.append(dict(event,timeSeconds=round(event['timeSeconds']-start+len(overview)*8,3),sourceChapter=id))
  run('ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(start),'-i',str(source),'-t','8','-an','-c:v','libx264','-preset','veryfast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(clip));overview.append(clip)
 concat=temp/'overview.txt';concat.write_text(''.join("file '"+str(c)+"'\n" for c in overview))
 run('ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(MEDIA/'overview.mp4'))
 (MEDIA/'events/overview.json').write_text(json.dumps({'coordinateSpace':{'width':540,'height':1200},'events':overview_events},indent=2)+'\n')
 duration=probe(MEDIA/'overview.mp4');shutil.copy2(MEDIA/'accounts.jpg',MEDIA/'overview.jpg');manifest['overview']={'duration':round(duration,3),'durationLabel':'1:44','chapters':ids,'excerpts':excerpts,'fictional':True};vtt('overview',duration)
 if not (MEDIA/'hero.jpg').exists():shutil.copy2(MEDIA/'accounts-01.jpg',MEDIA/'hero.jpg')
(ROOT/'src/media.json').write_text(json.dumps(manifest,indent=2)+'\n')
(MEDIA/'provenance.json').write_text(json.dumps({'appVersion':'1.11.0 (26)','sourceCommit':'9cd2063dc24db26e2159d3094e959dc77c64306a','sourceRepository':'https://github.com/dk-bluegrain/bsc','capture':'Native Android instrumentation; fictional identities, synthetic PDFs and fake bank transports only.','audio':'Silent: no music or narration.','security':'Only a disposable QA checkout permits screenshots. Distribution live screens retain FLAG_SECURE.','notEvidenceOf':'Bank authorization, owner-account validation, current live compatibility, or inclusion of all advanced flows in the basic demo.','chapters':manifest},indent=2)+'\n')
print('Approved native media,104-second overview,posters and98 caption tracks exported.')
