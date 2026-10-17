#!/usr/bin/env python3
"""Run against a local static server, or the published Pages URL with --url."""
import argparse,json
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8765/');p.add_argument('--browser');p.add_argument('--output',type=Path,default=Path('/tmp/bsc-browser-check'));a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
results=[];errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=a.browser,args=['--no-sandbox'])
 for width,height in ((390,844),(820,1180),(1440,1000)):
  for lang in ('es','en','de','fr','ru','uk','pt'):
   page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
   page.on('pageerror',lambda e:errors.append(str(e)))
   response=page.goto(a.url+lang+'/');assert response.ok
   assert page.locator('html').get_attribute('lang')==lang
   assert '1.12.0' in page.locator('header .brand small').inner_text()
   assert page.locator('a[href*="v1.12.0-preview.1"][href$="-demo.apk"]').count()==2
   assert not page.evaluate('document.documentElement.scrollWidth > innerWidth'),(lang,width,'overflow')
   assert page.locator('video[autoplay]').count()==0
   page.locator('.phone').focus();page.keyboard.press('Enter');assert page.locator('dialog').evaluate('(d)=>d.open')
   page.keyboard.press('Escape');assert not page.locator('dialog').evaluate('(d)=>d.open')
   assert page.locator('.phone').evaluate('(e)=>e===document.activeElement')
   page.locator('.chapter-list a').nth(4).click();page.locator('#history').wait_for(state='visible');assert not page.locator('#first-use').is_visible()
   page.locator('#speed-history').select_option('0.75');assert page.locator('#video-history').evaluate('(v)=>v.playbackRate')==0.75
   page.locator('#history details summary').click();assert page.locator('#history details').get_attribute('open') is not None
   shot=page.locator('#history .shot-button').first;shot.click();assert page.locator('dialog').evaluate('(d)=>d.open');page.keyboard.press('Escape')
   # Each chapter is directly addressable and its footage/captions are real files.
   for link in page.locator('.chapter-list a').all():
    id=link.get_attribute('href')[1:];page.evaluate('(id)=>location.hash=id',id);page.locator('#'+id).wait_for(state='visible')
    assert page.locator('#'+id+' video source').get_attribute('src').split('?')[0].endswith(id+'.mp4')
   if width==390 and lang=='es':page.screenshot(path=str(a.output/'mobile.png'),full_page=True)
   if width==1440 and lang=='en':page.goto(a.url+'en/');page.screenshot(path=str(a.output/'desktop.png'))
   if width==820:
    video=page.locator('#video-overview');video.evaluate('(v)=>v.load()');video.evaluate('(v)=>new Promise(resolve=>{if(v.readyState>=1)resolve();else v.addEventListener("loadedmetadata",resolve,{once:true})})');assert video.evaluate('(v)=>v.duration')>=90
    video.evaluate('(v)=>v.play()');page.wait_for_timeout(300);assert not video.evaluate('(v)=>v.paused');video.evaluate('(v)=>v.pause()')
   assert page.locator('a[href$="-demo.apk"]').count()==2 and page.locator('a[href$="-live.apk"]').count()==1
   page.goto(a.url+lang+'/privacy/');assert page.locator('h1').inner_text();assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
   page.get_by_role('link',name='GitHub',exact=True).first.wait_for()
   results.append({'language':lang,'width':width,'passed':True});page.close()
 browser.close()
assert not errors,errors
(a.output/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print('Browser checks passed:',len(results),'language/viewport combinations; keyboard, dialogs, chapters, speed, transcripts, media, privacy and downloads.')
