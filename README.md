# Santa Cruz Modern — showcase and Android downloads

Public static showcase for an independent Android app. Seven directly
addressable languages (Spanish default), native fictional screenshots, silent
H.264 walkthroughs, localized captions/transcripts and separate downloadable APKs.
The private Android source is `https://github.com/dk-bluegrain/bsc`.

Live site: https://dk-bluegrain.github.io/bsc-pages/

This repository contains website source, translations, approved fictional media,
and privacy pages only. No bank login, credential collection, analytics or backend.
APKs and SHA-256 checksums are versioned public GitHub Release assets, excluded
from this Git history. Live banking is experimental and independent: bank
authorization and owner-account validation remain unresolved. Shared client
configuration does not establish current compatibility. No Play submission.

## Build and preview

Requires Python3 and FFmpeg/FFprobe for media validation. Site generation uses
only Python's standard library. Approved media is canonical in `docs/media/`;
building the HTML preserves it rather than duplicating large files.

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory docs
```

Routes: `/es/`, `/en/`, `/de/`, `/fr/`, `/ru/`, `/uk/`, `/pt/` and
`/<language>/privacy/`. The root duplicates the Spanish page. Chapter anchors
remain shareable and are preserved when switching language. The language
selector stays available while scrolling. Native video controls do not autoplay;
all videos have speed controls and seven WebVTT tracks. Screenshot dialogs
support keyboard activation, Escape and focus restoration. Without JavaScript,
all chapters and native controls remain available.

`src/content.json` and `src/CONTENT.md` define seven-language site copy and its
context. `src/captions.json` and `src/CAPTIONS.md` define the exact caption and
transcript text and distinguish visible simulations from downloadable demo
capabilities. These are authored translations, not native-speaker certification.
`docs/privacy/app/` contains the matching complete APK privacy policies from the
private source; website privacy pages separately describe GitHub hosting and
external links. Keep both scopes current when application behavior changes.

## Reproduce media

Use only explicit disposable Android emulators, fictional identities, synthetic
PDFs and fake transports. See `DISTRIBUTION.md` in the private source for the
capture checkout, harness and recording commands. Production builds never
include recording helpers or disable protected banking screenshots.

```sh
python3 scripts/process-media.py --captures /absolute/private/raw-media \
  --captures /absolute/private/supplemental-captures
python3 scripts/build.py
python3 scripts/check.py
```

Later capture directories override the same chapter/scenario pair, enabling a
clean retake. Only scenarios with `complete.json`, passing instrumentation and
fictional/native-ring provenance are accepted. Each chapter combines approved
scenarios in order. H.264 MP4s are 540 × 1200 at 15 fps, silent, YUV420p, fast-start;
chapters are at least 30 s and complex chapters may exceed 120 s for readability.
The overview is 104 s, with thirteen 8-second excerpts in chapter order. Source
footage is never sped up. Native screenshots supply posters and enlargement
images. No generated or original-bank UI images are substituted.

Actual touch coordinates/epoch timestamps stay with retained raw evidence;
`docs/media/events/` supplies scaled coordinates and MP4-relative timings.
Native rings and swipe arrows are drawn inside the actual Android input action.
The encoder aligns recorded event times against the first visible native ring
and adds a one-second vector ring layer, preserving markers when a dialog or
external activity replaces the window. No taps are invented. `docs/media/provenance.json` records exact scenarios and selected emulators.
Individual files stay below 100 MB; the Pages deployment stays below 250 MB.
Raw captures, test logs, personal material and private configurations must never
enter this public repository.

## Browser verification

Use an isolated development environment and an installed Chromium:

```sh
python3 -m venv /tmp/bsc-pages-qa
/tmp/bsc-pages-qa/bin/pip install -r requirements-dev.txt
/tmp/bsc-pages-qa/bin/python scripts/browser-check.py \
  --browser /absolute/path/to/chromium --output /tmp/bsc-pages-browser-results
```

The suite checks seven languages at 390 px, 820 px and 1440 px; keyboard dialog
activation/Escape/focus, chapter links, playback speed, transcripts, media,
privacy pages, download links and horizontal overflow. The same command accepts
`--url https://dk-bluegrain.github.io/bsc-pages/` for the public site.
Static checks validate all local links/media, 14 silent H.264 videos, 98 captions,
versioned downloads and deployment budgets. Automated QA and sampled visual
review do not certify linguistic correctness or actual bank compatibility.

## Publish an update

1. Build and verify signed APKs in the private source using its retained
   distribution key. Keep version, tag, filenames and checksums consistent.
2. Update `VERSION`/`TAG` in `scripts/build.py`, release notes and site copy.
3. Generate/review native media, then build and run static/browser checks.
4. Push website source and generated `docs/` to `main`. For the first publication,
   enable Pages only after release assets exist. For later updates, publish
   release assets before pushing new download links.
5. Publish the versioned APKs, `SHA256SUMS` and release notes as Release assets.
   The initial release is `v1.11.0-preview.1`.
6. Configure GitHub Pages branch deployment to `main:/docs` (build type legacy).
   Verify anonymous page/media/privacy/download access and compare downloaded
   APK hashes against `SHA256SUMS`.

Example release publication after the source is committed:

```sh
gh release create v1.11.0-preview.1 \
  /absolute/private-source/distribution/santa-cruz-modern-1.11.0-demo.apk \
  /absolute/private-source/distribution/santa-cruz-modern-1.11.0-live.apk \
  /absolute/private-source/distribution/SHA256SUMS \
  --repo dk-bluegrain/bsc-pages --prerelease \
  --title 'Santa Cruz Modern 1.11.0 — independent preview' \
  --notes-file RELEASE-NOTES.md
```

Changing signing keys prevents updates over existing installs. Preserve the
owner's installation and pending-operation/token state; the `.demo` package can
coexist with the ordinary app. This repository never carries signing keys or
bank integration files. The explicitly requested experimental live APK carries
its client configuration as part of the public downloadable binary.
