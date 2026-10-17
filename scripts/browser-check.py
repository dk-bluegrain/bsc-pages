#!/usr/bin/env python3
"""Run against a local static server, or the published Pages URL with --url."""
import argparse,json
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8765/');p.add_argument('--browser');p.add_argument('--output',type=Path,default=Path('/tmp/bsc-browser-check'));a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
results=[];errors=[]
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
   assert '1.12.1' in page.locator('header .brand small').inner_text()
   assert page.locator('.hero a[href$="/download/"]').count()==1
   assert page.locator('a[href$=".apk"]').count()==0
   assert not page.evaluate('document.documentElement.scrollWidth > innerWidth'),(lang,width,'overflow')
   assert page.locator('video[autoplay]').count()==0
   assert page.locator('video').count()==0
   assert page.locator('[data-play-video]').count()==14
   assert page.locator('[data-play-video]').first.get_attribute('data-play-video')=='video-overview'
   page.locator('[data-play-video="video-overview"] img').wait_for(state='visible')
   assert page.locator('[data-play-video="video-overview"] img').evaluate('(i)=>i.complete && i.naturalWidth>0')
   assert not media_requests,('Media loaded before Play',lang,width,media_requests)
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
   assert page.locator('#live-guide .app-shot').count()==4
   assert page.locator('.install-guide img').count()==0
   assert all('/media/install/' not in img.get_attribute('src') for img in page.locator('.app-shot img').all())
   assert all(link.get_attribute('href').endswith('/download/') for link in page.locator('.languages a').all())
   assert page.locator('link[rel="canonical"]').get_attribute('href').endswith('/'+lang+'/download/')
   assert page.locator('.checksums code').count()==4
   page.locator('.live-choice a').click()
   assert page.url.endswith('#live-guide')
   shot=page.locator('.app-shot').first
   shot.focus();page.keyboard.press('Enter')
   assert page.locator('dialog').evaluate('(d)=>d.open')
   page.locator('dialog img').wait_for(state='visible')
   page.wait_for_function('()=>document.querySelector("dialog img").naturalWidth===540')
   page.keyboard.press('Escape')
   assert shot.evaluate('(e)=>e===document.activeElement')
   for img in page.locator('.app-shot img').all():
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
(a.output/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print('Browser checks passed:',len(results),'language/viewport combinations; no media before Play, keyboard playback, player isolation, speed, JPG previews without JavaScript, dialogs, chapters, transcripts, privacy, edition choice, illustrated guides and versioned downloads.')
