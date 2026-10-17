# Santa Cruz Modern — fewer steps, more clarity

Seven-language static app showcase at https://dk-bluegrain.github.io/bsc-pages/.
Spanish is the default; English, German, French, Russian, Ukrainian and Portuguese
have direct URLs and matching privacy pages. Native fictional screenshots and a
feature tour show SMS autofill, remembered biometric access, searchable history
and recipients, separate currencies, native PDFs, QR requests and clear reviews.

The private Android source is https://github.com/dk-bluegrain/bsc. APKs and checksums
are public versioned Release assets, excluded from website history. The live
edition is independent and experimental: bank authorization, current compatibility
and owner-account validation remain unresolved. No Google Play submission.

## Build and preview

Requires Python3, FFmpeg and FFprobe; HTML generation uses the Python standard
library. Optional voice generation uses `requirements-media.txt`. Approved
media is canonical in `docs/media/`; HTML generation preserves it. Preview
images use reviewed frames from the final video masters, pinned in `src/poster-
frames.json`; `python3 scripts/refresh-posters.py` reproduces them. After a
video edit, review and update its frame selection before refreshing. The
checker rejects stale frame pins, and preview URLs include the image hash so
browsers discard old thumbnails.

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory docs
```

Routes are `/<language>/`, `/<language>/download/` and `/<language>/privacy/`;
`/` renders Spanish. All landing-page download actions lead to the separate
edition-choice page. The unofficial APK link follows the bank-independence,
security and liability disclosures and the illustrated Android installation guide.
Chapter anchors stay shareable and persist when changing languages. The language selector
remains available while scrolling. JPG previews appear before playback; chapter
previews load lazily. Video players and caption tracks stay in inert templates
until a visitor clicks Play, so browsing chapters requests no video data. Native
controls, playback speed, seven caption tracks, transcripts and keyboard-accessible
screenshot dialogs are available. Each video displays its file size. Without
JavaScript the JPG links open MP4s directly and all chapter content remains readable.
Playback uses the selected page language's pre-rendered narration; other language
videos are not requested. Speech generation never runs in a visitor's browser.

The site has no banking login, credential collection, analytics or backend.

## Copy and media context

- `src/ux-copy.json` and `src/UX-COPY.md`: localized hero, six concrete benefits,
  SMS spotlight, task-focused chapter intros and ordered main-video cues.
- `src/download-copy.json` and `src/DOWNLOAD-COPY.md`: seven-language edition
  choices, developer-attributed publication rationale, security/risk notices and
  six installation steps with Android download, installer and source-permission
  screenshots.
- `src/content.json` and `src/CONTENT.md`: edition/download, support, installation
  and privacy copy. Original-app feature absences are not inferred or invented.
- `src/narration-actions.json`: canonical seven-language spoken actions, with
  per-phrase context and explicit event anchors for every final video.
- `src/captions.json`, `src/scenario-captions.json`, `src/scene-captions.json` and
  `src/CAPTIONS.md`: localized scene and reading-hold cues, with scope/context.
  `src/transcripts.json` is generated from the actual timed cues.
- `src/video-scripts.json` and [VIDEO-SCRIPTS.md](VIDEO-SCRIPTS.md): scripts written
  before recording. `src/overview-cuts.json` resolves authored anchors against
  actual recorded events.
- `docs/privacy/app/`: complete APK privacy notices exported from the app's seven
  language resources. Website privacy separately describes static hosting/links.

Videos show fictional identities, synthetic documents and fake bank transports.
Android approval results and biometrics are clearly identified synthetic callbacks,
not personal-session recordings or proof of live access. Advanced walkthroughs do
not imply every feature is in the simpler downloadable demo. Translation checks
and visual review do not certify native-speaker or independent legal review.

## Capture and reproduce videos

Use the private source's `DISTRIBUTION.md` and capture preparation/recording tools.
Recording helpers exist only in disposable QA checkouts. Production banking
screens retain screenshot protection. Select emulator serials explicitly and
never target a connected personal phone.

Revision 4 starts non-authentication videos inside the feature. Quiet fixture
sign-in happens before `scene-start` and is excluded from the export/gallery.
Metadata and static checks reject login input events outside authentication/setup.
Financial feature videos use native fake-bank SMS flows; no typed offline demo
code substitutes for SMS autofill. The first SMS walkthrough shows an empty field, the actual automatic-fill
callback, a readable filled state and continuation. Later transfer/payment
variants omit the repeated wait/autofill footage and resume on the filled code
before their own explicit Verify tap; each variant retains its review,
confirmation and actual bank result. SMS-only
login can continue after approved one-message sharing; financial and combined-
question flows retain explicit Verify. Assistance is enabled except initial
pre-choice onboarding and the explicit settings off/on demonstration.

Source capture pauses are intentional: opening 5 s, navigation 3.5 s, SMS empty 3 s and filled
5.5 s, review/receipt 8 s, important consent/uncertain outcomes 10–12 s. The native
UI stays at normal speed. Presentation exports shorten idle holds and remove explicitly reviewed repeated
steps, failed setup and unavailable controls in `src/editorial-cuts.json`. Retained native actions keep their
touch markers and readable SMS/review states. Original events and reasoned
exclusions remain in the event provenance. A synthetic bank-response delay makes the automatic
login transition legible without changing production timing. The main tour leads
with complete SMS-login and financial-fill/Verify sequences, then useful native
interactions across all 13 groups; its total stays between 90 and 120 seconds.
Complex chapter videos may exceed 120 seconds for readable multi-case coverage.

```sh
python3 scripts/process-media.py --captures /absolute/private/revision4-raw
python3 scripts/build.py
python3 scripts/check.py
```

Only passing `complete.json` scenarios matching the current script revision/hash
are accepted. Later capture directories override the same chapter/scenario pair,
allowing retakes. Failed attempts and raw recordings stay outside Git. Fast fixture
rehearsals are explicitly rejected as publication media. Partial `--chapter`
encoding runs sequentially because it updates shared manifests. `--captions-only`
refreshes timed tracks/transcripts without re-encoding video. The overview builds
only after every chapter matches the current script and expected scene count.

Canonical video is H.264 MP4, 540×1200, 15 fps, YUV420p and fast-start. The public
players use seven localized versions with AAC mono narration. Every media
file stays below 100 MB; the complete deployment stays below 250 MB. Actual native
tap/swipe events retain coordinates and timestamps. An expanding contrasting ring
lasts one second; native frame calibration aligns the persistent final overlay so
markers survive window changes. No taps are invented. Spotlight SMS images are
selected from the actual empty/filled hold frames. Media URLs include content
hashes so browsers request retaken footage.

To reproduce the shorter narrated presentation from its original capture export:

```sh
python3 -m venv /tmp/bsc-pages-narration
/tmp/bsc-pages-narration/bin/pip install -r requirements-media.txt
/tmp/bsc-pages-narration/bin/python scripts/narrate-media.py
python3 scripts/build.py
python3 -m unittest discover -s scripts/tests
python3 scripts/check.py
```

The default source is the unedited media at `91f22e0`. Content-addressed speech
clips remain in ignored `media-work/narration/`; reruns reuse them and always edit
the original frames. `--chapter overview` renders one preview. For new captures,
rebuild all original media, commit the source export, and pass that commit with
`--source-ref`. Partial raw/caption regeneration over narrated exports is blocked
because it would mix timelines. Voice selection, free alternatives and editing
rules are recorded in [VIDEO-SCRIPTS.md](VIDEO-SCRIPTS.md#narrated-presentation).

`docs/media/provenance.json` records the final capture source, script and exact
QA APK digests. The release APK source commit is recorded separately when the
update changes only recording tooling. Visual review covers every chapter and
all overview excerpts, especially the complete leading SMS transitions.

## Verify in browsers

Use an isolated development environment and installed Chromium:

```sh
python3 -m venv /tmp/bsc-pages-qa
/tmp/bsc-pages-qa/bin/pip install -r requirements-dev.txt
/tmp/bsc-pages-qa/bin/python scripts/browser-check.py \
  --browser /absolute/path/to/chromium --output /tmp/bsc-pages-browser-results
```

Checks cover all seven languages at 390, 820 and 1440 px: responsive layout,
keyboard dialogs/focus, task anchors, no video/caption requests before Play,
keyboard-started playback, speed selection before playback, the user-started tour,
single-player playback, JPG/MP4 links without JavaScript, every rendered transcript
against its canonical ordered actions, privacy and versioned downloads. At 820 px,
all 98 localized players decode video and audio with the selected page language’s
native captions; each complete caption sequence matches its transcript and an
actual playing cue is checked. Use
`--url https://dk-bluegrain.github.io/bsc-pages/` for anonymous public verification.
Static checks additionally verify all local assets, 14 silent videos, 98 timed
caption tracks, actual SMS events in the leading tour segments, login exclusions,
source metadata and file budgets. See [VERIFICATION.md](VERIFICATION.md).

## Publish

Build and verify signed APKs in the private source using its retained dedicated
key. Keep version names, codes, filenames, checksums, release tag and source pin
consistent. Never commit APKs, private bank configuration or signing material.
Commit verified website source and generated `docs/` locally before deployment.

```sh
python3 scripts/publish.py --apk-directory /absolute/private-source/distribution
```

For a new version this tags the verified website commit, checks all Release asset
hashes and publishes assets before pushing the new download links to main. Pages
uses branch deployment from `main:/docs`. The helper then anonymously compares
every deployed file and both APKs against local hashes.

A website/media-only update keeps existing APK assets and their tag immutable:

```sh
python3 scripts/publish.py --website-only \
  --apk-directory /absolute/private-source/distribution
```

Current APKs are 1.12.2 (29), tag `v1.12.2-preview.1`. Changing signing keys prevents
updates over existing installations; preserve the retained private key and owner
state. The `.demo` package coexists with the ordinary live package. The explicitly
requested experimental live binary carries shared client configuration, while
both repositories exclude the private configuration files.

`src/release.json` pins the current version, code, release tag, merged app source and signing certificate. `src/downloads.json` contains exact APK sizes and SHA-256 hashes. Installation illustrations and walkthrough provenance remain pinned to their original 1.12.1 captures.
