#!/usr/bin/env python3
"""Extract reviewed preview frames from the exact final video masters."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chapter', action='append')
    args = parser.parse_args()
    policy_path = ROOT / 'src/poster-frames.json'
    policy = json.loads(policy_path.read_text())
    media = json.loads((ROOT / 'src/media.json').read_text())
    assert set(policy['frames']) == set(media)
    manifest_path = ROOT / 'docs/media/posters.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {'revision': 1, 'frames': {}}
    selected = args.chapter or list(media)
    assert len(selected) == len(set(selected)) and set(selected) <= set(media)
    for chapter in selected:
        choice = policy['frames'][chapter]
        video = ROOT / f'docs/media/{chapter}.mp4'
        assert sha(video) == choice['sourceSha256'], f'{chapter}: re-review poster after changing the video'
        assert choice['context'] and 0 <= choice['timeSeconds'] < media[chapter]['duration']
        poster = ROOT / f'docs/media/{chapter}.jpg'
        temporary = poster.with_name(chapter + '.poster-tmp.jpg')
        try:
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(choice['timeSeconds']),
                            '-i', str(video), '-frames:v', '1', '-q:v', '3',
                            str(temporary)], check=True)
            temporary.replace(poster)
        finally:
            temporary.unlink(missing_ok=True)
        manifest['frames'][chapter] = {
            'source': f'{chapter}.mp4', 'sourceSha256': choice['sourceSha256'],
            'timeSeconds': choice['timeSeconds'], 'context': choice['context'],
            'poster': f'{chapter}.jpg', 'sha256': sha(poster), 'bytes': poster.stat().st_size,
        }
    manifest['policySha256'] = sha(policy_path)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(f'Refreshed {len(selected)} reviewed video previews.')


if __name__ == '__main__':
    main()
