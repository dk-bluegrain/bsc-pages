#!/usr/bin/env python3
"""Trim recorded idle holds and render seven localized, self-hosted voice-overs.

Inputs are pinned Git objects, so rerunning never speeds up an already edited
video or accumulates another generation of encoding loss. Speech clips are
content-addressed in the ignored work directory; only final media is published.
"""
import argparse
import asyncio
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile
import wave

ROOT = Path(__file__).resolve().parents[1]
SOURCE = '91f22e0031683e2ab6616be70a37abe72720d566'
FPS = 15
SAMPLE_RATE = 24000
VOICES = {
    'es': 'es-DO-RamonaNeural', 'en': 'en-US-JennyNeural',
    'de': 'de-DE-KatjaNeural', 'fr': 'fr-FR-DeniseNeural',
    'ru': 'ru-RU-SvetlanaNeural', 'uk': 'uk-UA-PolinaNeural',
    'pt': 'pt-BR-FranciscaNeural',
}
AUDIO_LANGUAGES = dict(es='spa', en='eng', de='deu', fr='fra', ru='rus', uk='ukr', pt='por')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def command(*args):
    return subprocess.check_output([str(arg) for arg in args], stderr=subprocess.PIPE)


def source_bytes(ref, path):
    return command('git', '-C', ROOT, 'show', f'{ref}:{path}')


def source_json(ref, path):
    return json.loads(source_bytes(ref, path))


def seconds(stamp):
    h, m, s = stamp.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)


def stamp(value):
    ms = round(value * 1000)
    return f'{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d}.{ms % 1000:03d}'


def parse_captions(data):
    return [(seconds(a), seconds(b), text.strip()) for a, b, text in re.findall(
        r'(\d+:\d+:\d+\.\d+) --> (\d+:\d+:\d+\.\d+)\n([^\n]+)', data)]


def mapped_time(value, cuts):
    return value - sum(max(0, min(value, end) - start) for start, end in cuts)


def idle_cuts(events, duration, groups, minimum_lengths, ratio=.68):
    """Remove whole frames only inside holds, away from every recorded action.

    Keep at least 1.2 seconds after input, 0.6 before input, and the same guards
    around scenario/excerpt boundaries. Group budgets reserve narration space.
    """
    boundaries = [begin for begin, end in groups] + [groups[-1][1]]
    protected = [e['timeSeconds'] for e in events if e['type'] not in ('hold', 'screenshot')]
    protected += boundaries
    budgets = [max(0, math.floor((end - begin - minimum) * FPS))
               for (begin, end), minimum in zip(groups, minimum_lengths)]
    used = [0] * len(groups)
    removed = set()
    for event in events:
        if event['type'] != 'hold':
            continue
        start = event['timeSeconds']
        end = min(duration, start + event.get('durationMs', 0) / 1000)
        minimum = 2 if event.get('cue') in ('opening', 'navigation', 'sms-wait') else 3
        desired = max(0, math.floor((end - start - max(minimum, (end - start) * ratio)) * FPS))
        candidates = range(math.ceil((start + 1.2) * FPS), math.floor((end - .6) * FPS))
        for frame in candidates:
            if not desired:
                break
            at = frame / FPS
            group = next((i for i, (a, b) in enumerate(groups) if a <= at < b), None)
            if group is None or used[group] >= budgets[group] or frame in removed:
                continue
            if any(point - .6 <= at < point + 1.2 for point in protected):
                continue
            removed.add(frame)
            used[group] += 1
            desired -= 1
    cuts = []
    for frame in sorted(removed):
        if cuts and abs(cuts[-1][1] - frame / FPS) < .00001:
            cuts[-1] = (cuts[-1][0], (frame + 1) / FPS)
        else:
            cuts.append((frame / FPS, (frame + 1) / FPS))
    return cuts


def groups_for(id, info, events):
    if id == 'overview':
        starts = [e['overviewStart'] for e in info['excerpts']]
        return list(zip(starts, starts[1:] + [info['duration']]))
    starts = [e['timeSeconds'] for e in events if e['type'] == 'scene-start']
    return list(zip(starts, starts[1:] + [info['duration']]))


def narration_candidates(ref, id, groups):
    tracks = {lang: parse_captions(source_bytes(ref, f'docs/media/captions/{lang}/{id}.vtt').decode())
              for lang in VOICES}
    reference = tracks['es']
    overrides = json.loads((ROOT / 'src/narration-copy.json').read_text())['languages']
    scene_texts = source_json(ref, 'src/scene-captions.json')['languages']['en']
    overview = source_json(ref, 'src/media.json')['overview']['excerpts'] if id == 'overview' else []
    assert all(len(track) == len(reference) for track in tracks.values())
    result = []
    seen = set()
    for index, (begin, end, text) in enumerate(reference):
        group = next(i for i in reversed(range(len(groups))) if groups[i][0] <= begin + .002)
        if (group, text) in seen:
            continue
        seen.add((group, text))
        required = not any(cue['group'] == group for cue in result)
        key = f'overview-{overview[group]["chapter"]}' if overview else ''
        if not overview:
            key = next(('scene-' + name for name, text in scene_texts.items() if text == tracks['en'][index][2]), '')
        result.append({'sourceStart': begin, 'sourceEnd': end, 'group': group,
                       'required': required,
                       'text': {lang: overrides[lang].get(key, tracks[lang][index][2]) for lang in VOICES}})
    return result


def clip_path(cache, voice, text):
    key = digest(json.dumps([voice, '+5%', text], ensure_ascii=False).encode())
    return cache / (key + '.mp3')


async def synthesize(candidates, cache):
    import edge_tts
    jobs = {(VOICES[lang], text) for cue in candidates for lang, text in cue['text'].items()}
    semaphore = asyncio.Semaphore(3)
    completed = 0

    async def one(voice, text):
        nonlocal completed
        path = clip_path(cache, voice, text)
        async with semaphore:
            if not path.exists():
                for attempt in range(4):
                    temporary = path.with_suffix('.partial.mp3')
                    try:
                        await edge_tts.Communicate(text, voice, rate='+5%',
                                                  connect_timeout=15, receive_timeout=30).save(str(temporary))
                        command('ffprobe', '-v', 'error', '-show_entries', 'format=duration', str(temporary))
                        temporary.replace(path)
                        break
                    except Exception:
                        temporary.unlink(missing_ok=True)
                        if attempt == 3:
                            raise
                        await asyncio.sleep(2 ** attempt)
            completed += 1
            if completed % 20 == 0 or completed == len(jobs):
                print(f'Speech clips ready: {completed}/{len(jobs)}', flush=True)

    await asyncio.gather(*(one(voice, text) for voice, text in sorted(jobs)))


def decode_clip(path):
    data = command('ffmpeg', '-v', 'error', '-i', path, '-f', 's16le',
                   '-ac', 1, '-ar', SAMPLE_RATE, 'pipe:1')
    assert data and any(data), f'Speech clip is empty or silent: {path.name}'
    return data


def schedule(candidates, groups, cuts, clips):
    result = []
    cursor = 0
    for cue in candidates:
        lengths = {lang: len(clips[(lang, text)]) / (SAMPLE_RATE * 2)
                   for lang, text in cue['text'].items()}
        maximum = max(lengths.values())
        start = max(mapped_time(cue['sourceStart'], cuts) + .1, cursor + .25)
        # Scene summaries describe the whole scene; specific state explanations
        # must finish while that state is still represented by its source cue.
        deadline = mapped_time(groups[cue['group']][1], cuts) - .1
        if not cue['required']:
            deadline = min(deadline, mapped_time(cue['sourceEnd'], cuts) + .25)
        if start + maximum > deadline:
            if cue['required']:
                raise ValueError(f'Narration does not fit scene: {cue["text"]["en"]}')
            continue
        result.append(dict(cue, start=round(start, 3), lengths=lengths))
        cursor = start + maximum
    return result


def encode_paced(source, target, duration, cuts, work):
    excluded = '+'.join(f'between(n,{round(a * FPS)},{round(b * FPS) - 1})' for a, b in cuts)
    filters = (f"select='not({excluded})'," if cuts else '') + f'setpts=N/({FPS}*TB)'
    graph = work / 'pace.ffgraph'
    graph.write_text(filters)
    command('ffmpeg', '-v', 'error', '-y', '-i', source, '-filter_script:v', graph,
            '-map', '0:v:0', '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', 24,
            '-threads', 4, '-pix_fmt', 'yuv420p', '-r', FPS, '-movflags', '+faststart', target)
    return float(command('ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                         '-of', 'csv=p=0', target))


def render_language(lang, id, cues, clips, silent, duration, work):
    pcm = bytearray(math.ceil(duration * SAMPLE_RATE) * 2)
    timed = []
    for cue in cues:
        text = cue['text'][lang]
        data = clips[(lang, text)]
        offset = round(cue['start'] * SAMPLE_RATE) * 2
        assert offset + len(data) <= len(pcm), (lang, id, 'speech overrun')
        pcm[offset:offset + len(data)] = data
        timed.append({'start': cue['start'], 'end': round(cue['start'] + len(data) / (SAMPLE_RATE * 2), 3),
                      'sourceStart': cue['sourceStart'], 'sourceEnd': cue['sourceEnd'],
                      'scene': cue['group'] + 1, 'summary': cue['required'], 'text': text})
    audio = work / f'{lang}-{id}.wav'
    with wave.open(str(audio), 'wb') as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(SAMPLE_RATE)
        output.writeframes(pcm)
    target = work / f'{lang}-{id}.mp4'
    command('ffmpeg', '-v', 'error', '-y', '-i', silent, '-i', audio,
            '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '48k',
            '-ar', SAMPLE_RATE, '-ac', 1, '-af', 'loudnorm=I=-18:TP=-1.5:LRA=7',
            '-t', duration, '-metadata:s:a:0', f'language={AUDIO_LANGUAGES[lang]}', '-movflags', '+faststart', target)
    vtt = ['WEBVTT', '']
    for i, cue in enumerate(timed, 1):
        vtt.extend([str(i), f'{stamp(cue["start"])} --> {stamp(cue["end"])}', cue['text'], ''])
    return target, '\n'.join(vtt), timed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-ref', default=SOURCE)
    parser.add_argument('--work-dir', type=Path, default=ROOT / 'media-work/narration')
    parser.add_argument('--chapter', action='append')
    args = parser.parse_args()
    ref = command('git', '-C', ROOT, 'rev-parse', '--verify', args.source_ref + '^{commit}').decode().strip()
    cache = args.work_dir.resolve() / 'speech'
    cache.mkdir(parents=True, exist_ok=True)
    original = source_json(ref, 'src/media.json')
    assert not any(info.get('pacing') or info.get('narration') for info in original.values()), 'Use the original, unedited capture export as source-ref'
    manifest = json.loads((ROOT / 'src/media.json').read_text())
    transcripts = json.loads((ROOT / 'src/transcripts.json').read_text())
    provenance = json.loads((ROOT / 'docs/media/provenance.json').read_text())
    selected = args.chapter or list(original)
    assert len(selected) == len(set(selected)) and set(selected) <= set(original)
    plans = {}
    for id in selected:
        events = source_json(ref, f'docs/media/events/{id}.json')
        groups = groups_for(id, original[id], events['events'])
        candidates = narration_candidates(ref, id, groups)
        plans[id] = (events, groups, candidates)
    asyncio.run(synthesize([cue for _, _, candidates in plans.values() for cue in candidates], cache))
    clips = {}
    for _, _, candidates in plans.values():
        for cue in candidates:
            for lang, text in cue['text'].items():
                if (lang, text) not in clips:
                    clips[(lang, text)] = decode_clip(clip_path(cache, VOICES[lang], text))
    for id, (events, groups, candidates) in plans.items():
        minimums = []
        for group in range(len(groups)):
            required = next(cue for cue in candidates if cue['group'] == group and cue['required'])
            minimums.append(max(len(clips[(lang, text)]) / (SAMPLE_RATE * 2)
                                for lang, text in required['text'].items()) + .6)
        cuts = idle_cuts(events['events'], original[id]['duration'], groups, minimums,
                         ratio=.76 if id == 'overview' else .68)
        cues = schedule(candidates, groups, cuts, clips)
        with tempfile.TemporaryDirectory(prefix=id + '-', dir=args.work_dir) as folder:
            work = Path(folder)
            source = work / 'source.mp4'
            source.write_bytes(source_bytes(ref, f'docs/media/{id}.mp4'))
            silent = work / f'{id}.mp4'
            duration = encode_paced(source, silent, original[id]['duration'], cuts, work)
            outputs = {lang: render_language(lang, id, cues, clips, silent, duration, work) for lang in VOICES}
            info = dict(original[id])
            info.update(duration=round(duration, 3), durationLabel=f'{int(duration) // 60}:{int(duration) % 60:02d}',
                        assetRevision=digest(silent.read_bytes())[:12])
            info['pacing'] = {'sourceRef': ref, 'sourceDuration': original[id]['duration'],
                              'removedIdleSeconds': round(sum(b - a for a, b in cuts), 3),
                              'cuts': [{'start': round(a, 6), 'end': round(b, 6)} for a, b in cuts],
                              'actionsAtOriginalSpeed': True}
            info['narration'] = {'engine': 'Microsoft Edge neural TTS via edge-tts 7.3.1',
                                 'rate': '+5%', 'revision': 1, 'languages': {}}
            for lang, (video, vtt, timed) in outputs.items():
                path = ROOT / f'docs/media/narrated/{lang}/{id}.mp4'
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(video.read_bytes())
                (ROOT / f'docs/media/captions/{lang}/{id}.vtt').write_text(vtt)
                transcripts['languages'][lang][id] = list(dict.fromkeys(cue['text'] for cue in timed))
                info['narration']['languages'][lang] = {'voice': VOICES[lang], 'file': f'narrated/{lang}/{id}.mp4',
                    'sha256': digest(video.read_bytes()), 'bytes': video.stat().st_size, 'cues': timed}
            (ROOT / f'docs/media/{id}.mp4').write_bytes(silent.read_bytes())
        for event in events['events']:
            at = event['timeSeconds']
            event['sourceTimeSeconds'] = at
            event['timeSeconds'] = round(mapped_time(at, cuts), 3)
            if 'durationMs' in event:
                event['sourceDurationMs'] = event['durationMs']
                event['durationMs'] = round((mapped_time(at + event['durationMs'] / 1000, cuts) - mapped_time(at, cuts)) * 1000)
        events['timing'] = events.get('timing', 'Offsets within the original authored overview excerpts.') + ' Presentation cuts remove idle hold frames only; sourceTimeSeconds preserves the pinned input timeline.'
        (ROOT / f'docs/media/events/{id}.json').write_text(json.dumps(events, indent=2) + '\n')
        if id == 'overview':
            for cut in info['excerpts']:
                begin = cut['overviewStart']
                cut['playbackStart'] = round(mapped_time(begin, cuts), 3)
                cut['playbackDuration'] = round(mapped_time(begin + cut['duration'], cuts) - mapped_time(begin, cuts), 3)
        manifest[id] = info
        provenance['chapters'][id] = info
        (ROOT / 'src/media.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
        (ROOT / 'src/transcripts.json').write_text(json.dumps(transcripts, ensure_ascii=False, indent=2) + '\n')
        provenance['audio'] = 'Localized synthetic narration in seven languages; self-hosted AAC mono, no music or runtime speech service.'
        (ROOT / 'docs/media/provenance.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n')
        print(f'{id}: {original[id]["duration"]:.1f}s -> {duration:.1f}s; {len(cues)} narration cues, seven languages', flush=True)


if __name__ == '__main__':
    main()
