#!/usr/bin/env python3
"""Run against a local static server, or the published Pages URL with --url."""
import argparse,json
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8765/');p.add_argument('--browser');p.add_argument('--output',type=Path,default=Path('/tmp/bsc-browser-check'));a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
transcripts=json.loads((Path(__file__).resolve().parents[1]/'src/transcripts.json').read_text())['languages']
release=json.loads((Path(__file__).resolve().parents[1]/'src/release.json').read_text())
results=[];errors=[];caption_results=[]
def check_captions(page,id,lang):
 video=page.locator('#video-'+id)
 page.wait_for_function('(id)=>{const v=document.getElementById("video-"+id);return v.readyState>=2 && [...v.textTracks].some(t=>t.mode==="showing" && t.cues?.length)}',arg=id)
 tracks=video.evaluate('(v)=>[...v.textTracks].filter(t=>t.mode==="showing").map(t=>({language:t.language,text:[...t.cues].map(c=>c.text)}))')
 assert tracks==[{'language':lang,'text':transcripts[lang][id]}],(lang,id,'browser captions do not match transcript',tracks)
 # Play from the start so this also works with the documented non-range local server.
 assert f'/narrated/{lang}/{id}.mp4' in video.evaluate('(v)=>v.currentSrc')
 assert not video.evaluate('(v)=>v.muted')
 video.evaluate('(v)=>{v.pause();v.currentTime=0;return v.play()}')
 page.wait_for_function('(id)=>{const v=document.getElementById("video-"+id);return v.currentTime>0 && v.webkitAudioDecodedByteCount>0 && v.webkitDecodedFrameCount>0 && [...v.textTracks].some(t=>t.mode==="showing" && t.activeCues?.length)}',arg=id)
 assert video.evaluate('(v)=>[...v.textTracks].find(t=>t.mode==="showing").activeCues[0].text')==transcripts[lang][id][0]
 video.evaluate('(v)=>v.pause()')
 caption_results.append({'language':lang,'chapter':id,'cues':len(transcripts[lang][id]),'passed':True})
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=a.browser,args=['--no-sandbox'])
 for width,height in ((390,844),(820,1180),(1440,1000)):
  for lang in ('es','en','de','fr','ru','uk','pt'):
   page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
   page.on('pageerror',lambda e:errors.append(str(e)))
   media_requests=[]
   page.on('request',lambda request:media_requests.append(urlsplit(request.url).path) if urlsplit(request.url).path.endswith(('.mp4','.vtt')) else None)
   response=page.goto(a.url+lang+'/');assert response.ok
   assert page.locator('html').get_attribute('lang')==lang
   assert release['version'] in page.locator('header .brand small').inner_text()
   assert page.locator('.hero a[href$="/download/"]').count()==1
   assert page.locator('a[href$=".apk"]').count()==0
   assert not page.evaluate('document.documentElement.scrollWidth > innerWidth'),(lang,width,'overflow')
   assert page.locator('video[autoplay]').count()==0
   assert page.locator('video').count()==0
   assert page.locator('[data-play-video]').count()==14
   assert page.locator('[data-play-video]').first.get_attribute('data-play-video')=='video-overview'
   page.locator('[data-play-video="video-overview"] img').wait_for(state='visible')
   page.wait_for_function('()=>{const i=document.querySelector("[data-play-video=video-overview] img");return i?.complete && i.naturalWidth>0}')
   assert page.locator('[data-play-video="video-overview"] img').evaluate('(i)=>i.complete && i.naturalWidth>0')
   assert page.locator('[data-play-video="video-overview"] img').get_attribute('src')==page.locator('#template-video-overview').evaluate('(t)=>t.content.querySelector("video").getAttribute("poster")')
   assert not media_requests,('Media loaded before Play',lang,width,media_requests)
   assert page.locator('.media-context details p').all_text_contents()==transcripts[lang]['overview'],(lang,width,'overview transcript')
   assert page.locator('.benefit').count()==6
   assert page.locator('.sms-frames [data-enlarge]').count()==2
   assert page.locator('.chapter-list a').first.get_attribute('href')=='#login'
   assert page.locator('main').inner_text().find(page.locator('h1').inner_text())>=0
   if width==1440:
    bounds=page.locator('[data-play-video="video-overview"]').bounding_box();assert bounds['y']<height and bounds['x']>width/2

   page.locator('.phone').focus();page.keyboard.press('Enter');assert page.locator('dialog').evaluate('(d)=>d.open')
   page.keyboard.press('Escape');assert not page.locator('dialog').evaluate('(d)=>d.open')
   assert page.locator('.phone').evaluate('(e)=>e===document.activeElement')
   page.locator('.chapter-list a[href="#history"]').click();page.locator('#history').wait_for(state='visible');assert not page.locator('#first-use').is_visible()
   page.locator('#speed-history').select_option('0.75');assert page.locator('#video-history').count()==0
   page.locator('#history details summary').click();assert page.locator('#history details').get_attribute('open') is not None
   shot=page.locator('#history .shot-button').first;shot.click();assert page.locator('dialog').evaluate('(d)=>d.open');page.keyboard.press('Escape')
   # Each chapter is directly addressable and its footage/captions are real files.
   for link in page.locator('.chapter-list a').all():
    id=link.get_attribute('href')[1:];page.evaluate('(id)=>location.hash=id',id);page.locator('#'+id).wait_for(state='visible')
    page.locator('#'+id+' details').evaluate('(d)=>d.open=true')
    image=page.locator('[data-play-video="video-'+id+'"] img');image.scroll_into_view_if_needed()
    page.wait_for_function('(id)=>{const i=document.querySelector(`[data-play-video="video-${id}"] img`);return i?.complete && i.naturalWidth>0}',arg=id)
    image.evaluate('(i)=>i.decode()')
    assert image.get_attribute('src')==page.locator('#template-video-'+id).evaluate('(t)=>t.content.querySelector("video").getAttribute("poster")')
    assert page.locator('#'+id+' details p').all_text_contents()==transcripts[lang][id],(lang,width,id,'rendered transcript')
    assert page.locator('#template-video-'+id).evaluate('(t)=>t.content.querySelector("source").getAttribute("src")').split('?')[0].endswith(f'/narrated/{lang}/{id}.mp4')
   assert not media_requests,('Browsing chapters loaded media',lang,width,media_requests)
   if width==390 and lang=='es':page.screenshot(path=str(a.output/'mobile.png'),full_page=True)
   if width==1440 and lang=='en':page.goto(a.url+'en/');page.screenshot(path=str(a.output/'desktop.png'))
   if width==820:
    page.evaluate('location.hash="history"');page.locator('#history').wait_for(state='visible')
    preview=page.locator('[data-play-video="video-history"]');preview.focus();page.keyboard.press('Enter')
    page.wait_for_function('()=>document.getElementById("video-history")?.currentTime>0')
    history=page.locator('#video-history');assert history.evaluate('(v)=>v.playbackRate')==0.75
    assert history.evaluate('(v)=>v===document.activeElement')
    page.locator('[data-play-overview]').click();page.wait_for_timeout(300)
    page.wait_for_function('()=>document.getElementById("video-overview")?.currentTime>0')
    page.wait_for_function('()=>document.getElementById("video-overview").webkitAudioDecodedByteCount>0')
    assert not page.locator('#video-overview').evaluate('(v)=>v.muted')
    assert f'/narrated/{lang}/overview.mp4' in page.locator('#video-overview').evaluate('(v)=>v.currentSrc')
    assert history.evaluate('(v)=>v.paused')
    assert all(path.endswith(('/history.mp4','/overview.mp4','/history.vtt','/overview.vtt')) for path in media_requests),media_requests
    page.locator('#video-overview').evaluate('(v)=>v.pause()')
    video=page.locator('#video-overview');video.evaluate('(v)=>v.load()');video.evaluate('(v)=>new Promise(resolve=>{if(v.readyState>=1)resolve();else v.addEventListener("loadedmetadata",resolve,{once:true})})');assert video.evaluate('(v)=>v.duration')>=60
    video.evaluate('(v)=>v.play()');page.wait_for_timeout(300);assert not video.evaluate('(v)=>v.paused');video.evaluate('(v)=>v.pause()')
    check_captions(page,'overview',lang)
    for chapter in transcripts[lang]:
     if chapter=='overview':continue
     page.evaluate('(id)=>location.hash=id',chapter);page.locator('#'+chapter).wait_for(state='visible')
     if not page.locator('#video-'+chapter).count():page.locator('[data-play-video="video-'+chapter+'"]').click()
     check_captions(page,chapter,lang)
   media_requests.clear()
   page.goto(a.url+lang+'/')
   page.locator('.hero a[href$="/download/"]').click()
   assert urlsplit(page.url).path.endswith('/'+lang+'/download/')
   assert page.locator('.download-choices article').count()==2
   if width==390:
    assert page.locator('.download-jump').is_visible()
    assert page.locator('.download-jump a').count()==2
   assert page.locator('a[href$="-demo.apk"]').count()==1 and page.locator('a[href$="-live.apk"]').count()==1
   assert page.locator('.live-choice a').get_attribute('href')=='#live-guide'
   assert page.locator('#live-download a[href$="-live.apk"]').count()==1
   assert not page.evaluate('document.documentElement.scrollWidth > innerWidth'),(lang,width,'download overflow')
   assert page.locator('.install-guide>li').count()==6
   assert page.locator('.install-shot').count()==5
   assert page.locator('.download-gallery, .app-shot').count()==0
   assert page.locator('.install-guide .install-shot').count()==5
   assert all(link.get_attribute('href').endswith('/download/') for link in page.locator('.languages a').all())
   assert page.locator('link[rel="canonical"]').get_attribute('href').endswith('/'+lang+'/download/')
   assert page.locator('.checksums code').count()==4
   page.locator('.live-choice a').click()
   assert page.url.endswith('#live-guide')
   shot=page.locator('.install-shot').first
   shot.focus();page.keyboard.press('Enter')
   assert page.locator('dialog').evaluate('(d)=>d.open')
   page.locator('dialog img').wait_for(state='visible')
   page.wait_for_function('()=>document.querySelector("dialog img").naturalWidth===540')
   page.keyboard.press('Escape')
   assert shot.evaluate('(e)=>e===document.activeElement')
   for img in page.locator('.install-shot img').all():
    img.scroll_into_view_if_needed()
    img.evaluate('(i)=>i.decode()')
   if (lang,width) in (('en',1440),('en',390),('ru',390),('de',820)):
    page.goto(a.url+lang+'/download/')
    page.screenshot(path=str(a.output/f'download-{lang}-{width}.png'),full_page=True)
   assert not media_requests,('Download guide requested media',lang,width,media_requests)

   page.goto(a.url+lang+'/privacy/');assert page.locator('h1').inner_text();assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
   page.get_by_role('link',name='GitHub',exact=True).first.wait_for()
   results.append({'language':lang,'width':width,'passed':True});page.close()
 # JPG previews and direct MP4 links remain useful without JavaScript.
 page=browser.new_page(java_script_enabled=False,viewport={'width':390,'height':844})
 page.goto(a.url+'en/')
 assert page.locator('[data-play-video]').count()==14
 assert page.locator('video').count()==0
 assert page.locator('[data-play-video="video-overview"]').get_attribute('href').split('?')[0].endswith('overview.mp4')
 assert page.locator('#history [data-play-video]').is_visible()
 page.goto(a.url+'en/download/')
 assert page.locator('a[href$="-demo.apk"]').count()==1 and page.locator('a[href$="-live.apk"]').count()==1
 assert page.locator('.install-guide>li').count()==6
 assert page.locator('.risk-notice').is_visible()
 page.close()
 browser.close()
assert not errors,errors
(a.output/'captions.json').write_text(json.dumps(caption_results,indent=2)+'\n')
(a.output/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print('Browser checks passed:',len(results),'language/viewport combinations;',len(caption_results),'localized players with native captions matching all rendered transcript cues; no media before Play, keyboard playback, player isolation, speed, JPG previews without JavaScript, dialogs, chapters, transcripts, privacy, edition choice, illustrated guides and versioned downloads.')
