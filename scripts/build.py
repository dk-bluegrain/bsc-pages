#!/usr/bin/env python3
"""Generate the benefit-led, seven-language static showcase and privacy pages."""
from pathlib import Path
from html import escape as E
import json, shutil, hashlib
ROOT=Path(__file__).resolve().parents[1]; DOCS=ROOT/'docs'
LANGS=json.loads((ROOT/'src/content.json').read_text())['languages']
UX=json.loads((ROOT/'src/ux-copy.json').read_text())['languages']
DOWNLOAD=json.loads((ROOT/'src/download-copy.json').read_text())['languages']
DOWNLOADS=json.loads((ROOT/'src/downloads.json').read_text())
VERSION='1.12.1'; CODE=28; TAG='v1.12.1-preview.1'; BASE='https://dk-bluegrain.github.io/bsc-pages'
RELEASE=f'https://github.com/dk-bluegrain/bsc-pages/releases/download/{TAG}'
ORDER=['login','accounts','history','transfers','payments','statements','qr','beneficiaries','cards','token','settings','verification','first-use']
CAPTIONS=json.loads((ROOT/'src/transcripts.json').read_text())['languages']
MEDIA=json.loads((ROOT/'src/media.json').read_text())
(DOCS/'assets').mkdir(parents=True,exist_ok=True)
for name in ('style.css','site.js','mark.svg'): shutil.copy2(ROOT/'src'/name,DOCS/'assets'/name)
(DOCS/'.nojekyll').touch()
ASSETS={name:hashlib.sha256((ROOT/'src'/name).read_bytes()).hexdigest()[:12] for name in ('style.css','site.js')}

def languages(lang,prefix,section=''):
    label=dict(es='Idioma',en='Language',de='Sprache',fr='Langue',ru='Язык',uk='Мова',pt='Idioma')[lang]
    links=''.join(f'<a lang="{code}" hreflang="{code}" href="{prefix}{code}/{section}"'+(' aria-current="page"' if code==lang else '')+f'>{E(value["name"])}</a>' for code,value in LANGS.items())
    return f'<nav class="languages" aria-label="{label}">{links}</nav>'

def header(lang,prefix,section=''):
    return f'<header><div class="wrap header"><a class="brand" href="{prefix}{lang}/"><img width="38" height="38" src="{prefix}assets/mark.svg" alt=""><span>Santa Cruz Modern<small>Android · {VERSION}</small></span></a>{languages(lang,prefix,section)}</div></header>'

def image_button(file,title,prefix,revision,classes='shot-button',loading='lazy'):
    url=f'{prefix}media/{file}?v={revision}'
    return f'<button class="{classes}" data-enlarge="{url}" aria-label="{E(title)}"><img loading="{loading}" width="540" height="1200" src="{url}" alt="{E(title)}"></button>'

def video(id,lang,prefix,c):
    info=MEDIA[id]; revision=info['assetRevision']
    poster_revision=hashlib.sha256((DOCS/'media'/f'{id}.jpg').read_bytes()).hexdigest()[:12]
    tracks=''.join(f'<track kind="captions" srclang="{code}" label="{E(value["name"])}" src="{prefix}media/captions/{code}/{id}.vtt?v={hashlib.sha256((DOCS/"media/captions"/code/f"{id}.vtt").read_bytes()).hexdigest()[:12]}"'+(' default' if code==lang else '')+'>' for code,value in LANGS.items())
    title=c['overviewTitle'] if id=='overview' else UX[lang]['chapters'][id]['title']
    watch=UX[lang]['watchLabel' if id=='overview' else 'proofLabel']
    loading='eager' if id=='overview' else 'lazy'
    narration=info.get('narration',{}).get('languages',{}).get(lang,{})
    playback=narration.get('file',f'{id}.mp4')
    playback_revision=narration.get('sha256',revision)[:12]
    playback_url=f'{prefix}media/{playback}?v={playback_revision}'
    size=(DOCS/'media'/playback).stat().st_size/1_000_000
    # Templates are inert: neither MP4 nor caption tracks can load before a click.
    # The JPG link also opens the native MP4 player when JavaScript is disabled.
    return f'''<div class="video-shell"><a class="video-preview" data-play-video="video-{id}" href="{playback_url}" aria-label="{E(watch)} · {E(title)}"><img loading="{loading}" width="540" height="1200" src="{prefix}media/{id}.jpg?v={poster_revision}" alt=""><span class="video-play"><span aria-hidden="true">▶</span>{E(watch)}</span></a><template id="template-video-{id}"><video id="video-{id}" width="540" height="1200" controls playsinline preload="none" poster="{prefix}media/{id}.jpg?v={poster_revision}" aria-label="{E(title)}"><source src="{playback_url}" type="video/mp4">{tracks}</video></template></div><div class="video-tools"><span class="meta">{info['durationLabel']} · MP4 · {size:.2f} MB</span><label for="speed-{id}">{E(c['speedLabel'])}</label><select id="speed-{id}" data-speed="video-{id}"><option value="0.5">0.5×</option><option value="0.75">0.75×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option><option value="2">2×</option></select></div>'''

def transcript(id,lang,c):
    return f'<details><summary>{E(c["transcriptLabel"])}</summary>'+''.join(f'<p>{E(text)}</p>' for text in CAPTIONS[lang][id])+'</details>'

def main_page(lang,prefix):
    c=LANGS[lang];u=UX[lang];d=DOWNLOAD[lang]
    benefit_rows=''.join(f'<a class="benefit" href="#{b["chapter"]}"><span class="benefit-index">{i+1:02d}</span><div><h3>{E(b["title"])}</h3><p>{E(b["body"])}</p><span class="text-link">{E(u["proofLabel"])} <span aria-hidden="true">↗</span></span></div></a>' for i,b in enumerate(u['benefits']))
    chapter_nav=''.join(f'<a href="#{id}"><span>{i+1:02d}</span>{E(u["chapters"][id]["title"])}</a>' for i,id in enumerate(ORDER))
    chapters=[]
    for i,id in enumerate(ORDER):
        ch=u['chapters'][id];info=MEDIA[id];revision=info['assetRevision']
        gallery=''.join(image_button(shot,f'{ch["title"]} · {c["screenshotsLabel"]} {j+1}',prefix,revision) for j,shot in enumerate(info['screenshots']))
        label=c['demoLabel'] if id=='accounts' else c['simulatedLabel']
        chapters.append(f'<article class="chapter" id="{id}"><div class="chapter-heading"><span class="tag">{E(label)}</span><span class="meta">{i+1:02d} / 13</span></div><h3>{E(ch["title"])}</h3><p class="chapter-intro">{E(ch["body"])}</p>{video(id,lang,prefix,c)}{transcript(id,lang,c)}<h4>{E(c["screenshotsLabel"])}</h4><div class="shot-list">{gallery}</div></article>')
    # Exact captured SMS frames are selected by their recorded reading-hold events.
    sms=MEDIA['transfers']; frames=sms.get('featuredFrames',{})
    empty=frames.get('sms-wait',sms['screenshots'][0]);filled=frames.get('sms-filled',sms['screenshots'][min(1,len(sms['screenshots'])-1)])
    sms_images=image_button(empty,u['smsSpotlightTitle'],prefix,sms['assetRevision'],'phone sms-frame')+image_button(filled,u['smsSpotlightTitle'],prefix,sms['assetRevision'],'sms-frame')
    steps=''.join(f'<li>{E(step)}</li>' for step in c['installSteps'])
    return f'''<main id="main">
<section class="wrap hero"><div class="hero-copy"><p class="eyebrow">{E(u['eyebrow'])}</p><h1>{E(u['headline'])}</h1><p class="lead">{E(u['intro'])}</p><div class="actions"><a class="button" data-play-overview href="#overview">{E(u['watchLabel'])} <span aria-hidden="true">▶</span></a><a class="button secondary" href="{prefix}{lang}/download/">{E(d['action'])} ↗</a></div><p class="platform-note">Android 8.0+ <span aria-hidden="true">/</span> ES · EN · DE · FR · RU · UK · PT</p><a class="text-link edition-link" href="#editions">{E(c['compareTitle'])} ↓</a></div><div id="overview" class="hero-film"><div class="film-label"><span class="status-dot" aria-hidden="true"></span>{E(c['overviewTitle'])}<span class="meta">{MEDIA['overview']['durationLabel']}</span></div>{video('overview',lang,prefix,c)}</div></section>
<section class="wrap media-context"><p>{E(u['mediaNote'])}</p>{transcript('overview',lang,c)}</section>
<section class="wrap section benefits-section"><div class="section-heading"><div><span class="eyebrow">SANTA CRUZ MODERN</span><h2>{E(u['benefitsTitle'])}</h2></div><p>{E(u['benefitsIntro'])}</p></div><div class="benefit-grid">{benefit_rows}</div></section>
<section class="sms-section"><div class="wrap sms-layout"><div><span class="eyebrow">SMS</span><h2>{E(u['smsSpotlightTitle'])}</h2><p>{E(u['smsSpotlightBody'])}</p><a class="button mint" href="#login">{E(u['proofLabel'])} ↗</a></div><div class="sms-frames">{sms_images}</div></div></section>
<section id="chapters" class="wrap section"><div class="section-heading"><div><span class="eyebrow">ANDROID</span><h2>{E(u['flowTitle'])}</h2></div><p>{E(u['flowIntro'])}</p></div><div class="chapter-layout"><nav class="chapter-list" aria-label="{E(c['chaptersTitle'])}">{chapter_nav}</nav><div>{''.join(chapters)}</div></div></section>
<section id="editions" class="wrap section"><div class="section-heading"><div><span class="eyebrow">APK · ANDROID 8.0+</span><h2>{E(c['compareTitle'])}</h2></div></div><div class="edition-grid"><article class="edition"><span class="meta">.demo · {E(c['demoLabel'])}</span><h3>{E(c['demoTitle'])}</h3><p>{E(c['demoBody'])}</p><a class="button" href="{prefix}{lang}/download/#demo">{E(d['action'])} ↗</a></article><article class="edition"><span class="meta">APK · {E(c['liveTitle'])}</span><h3>{E(c['liveTitle'])}</h3><p>{E(c['liveBody'])}</p><a class="button secondary" href="{prefix}{lang}/download/#live-guide">{E(d['guideAction'])} ↗</a></article></div><p class="subtle">{E(c['versionLabel'])} {VERSION} ({CODE}) · <a href="{RELEASE}/SHA256SUMS">SHA-256</a> · <a href="https://github.com/dk-bluegrain/bsc-pages/releases/tag/{TAG}">GitHub Release</a></p><p class="warning">{E(c['warning'])}</p></section>
<section class="wrap section installation"><div><h2>{E(c['requirementsTitle'])}</h2><p>{E(c['requirementsBody'])}</p><p><a href="{prefix}{lang}/privacy/">{E(c['privacyLabel'])}</a> · <a href="{prefix}privacy/app/{lang}.html">Android APK</a></p></div><div><h3>{E(c['installTitle'])}</h3><ol>{steps}</ol></div></section><section class="wrap section support"><h2>{E(c['supportLabel'])}</h2><p>{E(c['supportBody'])}</p><a class="text-link" href="https://github.com/dk-bluegrain/bsc-pages/issues">GitHub ↗</a></section></main><dialog aria-label="{E(c['screenshotsLabel'])}"><img alt=""><button type="button">{E(c['closeLabel'])}</button></dialog>'''

def download_page(lang,prefix):
    c=LANGS[lang];d=DOWNLOAD[lang]
    # APK links live here so that every landing-page path presents the edition choice.
    demo=f'{RELEASE}/{DOWNLOADS["demo"]["filename"]}'
    live=f'{RELEASE}/{DOWNLOADS["live"]["filename"]}'
    images={0:'download.png',1:'open-apk.png',2:'allow-source.png',3:'install.png',4:'disable-source.png'}
    steps=[]
    for index,step in enumerate(d['steps']):
        shot=''
        if index in images:
            file=images[index]
            revision=hashlib.sha256((DOCS/'media/install'/file).read_bytes()).hexdigest()[:12]
            shot=image_button('install/'+file,step['title'],prefix,revision,'install-shot')
        steps.append(f'<li><div><h3>{E(step["title"])}</h3><p>{E(step["body"])}</p></div>{shot}</li>')
    checksums=''.join(f'<div><strong>{E(d[edition+"Title"])}</strong><code>{E(data["filename"])}</code><code>{data["sha256"]}</code></div>' for edition,data in DOWNLOADS.items())
    return f'''<main id="main" class="wrap downloads">
<a class="text-link" href="{prefix}{lang}/">← {E(d['backLabel'])}</a>
<div class="download-intro"><p class="eyebrow">APK · ANDROID 8.0+ · {VERSION}</p><h1>{E(d['title'])}</h1><p class="lead">{E(d['intro'])}</p></div>
<nav class="download-jump" aria-label="{E(d['action'])}"><a href="#demo">01 · {E(d['demoTitle'])} ↓</a><a href="#banking-choice">02 · {E(d['liveTitle'])} ↓</a></nav>
<div class="edition-grid download-choices"><article id="demo" class="edition demo-choice"><span class="edition-badge">{E(d['demoBadge'])}</span><h2>{E(d['demoTitle'])}</h2><p>{E(d['demoBody'])}</p><a class="button" href="{demo}">{E(c['demoAction'])} ↗</a><a class="text-link" href="#installation">{E(d['guideTitle'])} ↓</a></article>
<article id="banking-choice" class="edition live-choice"><span class="edition-badge">{E(d['liveBadge'])}</span><h2>{E(d['liveTitle'])}</h2><p>{E(d['liveBody'])}</p><a class="button secondary" href="#live-guide">{E(d['guideAction'])} ↓</a></article></div>
<section id="live-guide" class="download-section"><h2>{E(d['whyTitle'])}</h2><p>{E(d['whyBody'])}</p><p>{E(d['permissionBody'])}</p></section>
<section class="download-section"><h2>{E(d['securityTitle'])}</h2><p>{E(d['securityBody'])}</p><p>{E(d['verificationBody'])}</p><div class="checksums"><h3>{E(d['checksumLabel'])} · {VERSION} ({CODE})</h3>{checksums}<p><a href="{RELEASE}/SHA256SUMS">SHA256SUMS ↗</a> · <a href="https://github.com/dk-bluegrain/bsc-pages/releases/tag/{TAG}">GitHub Release ↗</a></p></div><p><a href="{prefix}privacy/app/{lang}.html">Android APK · {E(c['privacyLabel'])}</a></p></section>
<section class="download-section risk-notice"><h2>{E(d['riskTitle'])}</h2><p>{E(d['riskBody'])}</p><p>{E(d['liabilityBody'])}</p></section>
<section id="installation" class="download-section"><h2>{E(d['guideTitle'])}</h2><p>{E(d['guideIntro'])}</p><p class="subtle">{E(d['screensNote'])}</p><ol class="install-guide">{''.join(steps)}</ol><p class="warning">{E(d['protectBody'])}</p><p>{E(d['sourcesLabel'])}: <a href="https://support.google.com/android/answer/9457058?hl={lang}">Android Help ↗</a> · <a href="https://support.google.com/googleplay/answer/2812853?hl={lang}">Google Play Protect ↗</a></p></section>
<section id="live-download" class="download-section final-download"><span class="edition-badge">{E(d['liveBadge'])}</span><h2>{E(d['downloadTitle'])}</h2><p>{E(d['downloadBody'])}</p><a class="button" href="{live}">{E(d['downloadAction'])} ↗</a><p><a href="{prefix}privacy/app/{lang}.html">Android APK · {E(c['privacyLabel'])}</a></p><p class="subtle">{E(c['versionLabel'])} {VERSION} ({CODE}) · <a href="{RELEASE}/SHA256SUMS">SHA-256</a></p></section>
<section class="download-section support"><h2>{E(c['supportLabel'])}</h2><p>{E(c['supportBody'])}</p><a href="https://github.com/dk-bluegrain/bsc-pages/issues">GitHub ↗</a></section></main><dialog aria-label="{E(c['screenshotsLabel'])}"><img alt=""><button type="button">{E(c['closeLabel'])}</button></dialog>'''

def page(lang,prefix,section=''):
    c=LANGS[lang];u=UX[lang]
    title=u['headline'];description=u['intro']
    if section=='download/':
        body=download_page(lang,prefix);title=DOWNLOAD[lang]['title'];description=DOWNLOAD[lang]['intro']
    elif section=='privacy/':
        title=c['privacyTitle']
        body=f'<main id="main" class="wrap policy"><a href="../../{lang}/">← Santa Cruz Modern</a><h1>{E(c["privacyTitle"])}</h1><p>{E(c["privacyIntro"])}</p>'+''.join(f'<h2>{E(s["title"])}</h2><p>{E(s["body"])}</p>' for s in c['privacySections'])+f'<p><a href="{prefix}privacy/app/{lang}.html">Android APK · {E(c["privacyLabel"])}</a></p><p><a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub · {E(c["privacyLabel"])}</a></p><p class="meta">2026-10-16 · {VERSION} ({CODE})</p></main>'
    else:body=main_page(lang,prefix)
    footer=f'<footer><div class="wrap footer"><span>© 2026 Santa Cruz Modern · Android</span><div class="footer-links"><a href="{prefix}{lang}/privacy/">{E(c["privacyLabel"])}</a><a href="https://github.com/dk-bluegrain/bsc-pages">GitHub</a><a href="{RELEASE}/SHA256SUMS">SHA-256</a></div></div></footer>'
    canonical=BASE+f'/{lang}/'+section
    alternates=''.join(f'<link rel="alternate" hreflang="{code}" href="{BASE}/{code}/{section}">' for code in LANGS)
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#143e34"><meta name="description" content="{E(description)}"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; media-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"><meta name="referrer" content="no-referrer"><title>Santa Cruz Modern · {E(title)}</title><link rel="canonical" href="{canonical}">{alternates}<link rel="icon" href="{prefix}assets/mark.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/style.css?v={ASSETS['style.css']}"><script src="{prefix}assets/site.js?v={ASSETS['site.js']}" defer></script></head><body><a class="skip" href="#main">{E(c['skipLabel'])}</a>{header(lang,prefix,section)}{body}{footer}</body></html>'''

for lang in LANGS:
    p=DOCS/lang;p.mkdir(exist_ok=True);(p/'index.html').write_text(page(lang,'../'))
    (p/'privacy').mkdir(exist_ok=True);(p/'privacy/index.html').write_text(page(lang,'../../','privacy/'))
    (p/'download').mkdir(exist_ok=True);(p/'download/index.html').write_text(page(lang,'../../','download/'))
(DOCS/'index.html').write_text(page('es','./'))
(DOCS/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n')
(DOCS/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}/{lang}/{suffix}</loc></url>' for lang in LANGS for suffix in ('','privacy/','download/'))+'</urlset>')
print('Built showcase, download guides and privacy pages in seven languages.')
