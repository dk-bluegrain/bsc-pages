# Translation update and signed app release — 1.12.2 (29)

Five sequential translation review/fix passes ran in separate agents across the
Android interface and website. Adjacent comments identify display context,
actions, source references and argument/data boundaries in all seven languages.
Website metadata is validated and stripped before rendering/media processing.

The authoritative app source is merged at
`ab11715dcc734e88e14b956e0b2163473f110f16`, tagged `v1.12.2` in the private
`dk-bluegrain/bsc` repository. Its release verification records 1,046 translation
entries, 23 Python tests, 281 JVM tests per debug/demo/live variant, and 22 language
integration tests at each of normal and 150% text size. Both signed editions pass
lint, package isolation, signature/ZIP alignment and native 16 KiB alignment.
They update over the exact previously published 1.12.1 APKs with the retained
signing certificate. Offline demo/live startup checks use an explicit disposable
emulator, no banking credentials and no real operations.

Current version, code, tag, merged source, certificate and historical capture
pins live in `src/release.json`; exact APK filenames, sizes and SHA-256 hashes
live in `src/downloads.json`. Release assets include both APKs, `SHA256SUMS`,
release notes and a machine-readable release manifest. The existing installer
screenshots and feature videos retain their genuine 1.12.1 provenance; localized
installation copy makes that distinction explicit.

Website build, all 16 unit tests and full static/media checks pass. Final
Chromium validation covers 21 language/viewport combinations and 98 localized
players, native captions against all transcript cues, lazy playback, keyboard
focus, edition routing, installation guides, privacy and no-JavaScript links.

No native-speaker/legal certification, live-account compatibility or bank
approval is established by these checks. Earlier sections below retain their
historical validation scope and artifact identities.

# Feature-first website and native media verification

## Edition choice and illustrated installation guide

The tour's download actions lead to a separate localized `/download/` page.
Demo and unofficial banking choices are distinct; on mobile, two quick links
keep both choices visible before the full cards. The banking APK link appears
after developer-attributed publication rationale, security limits, own-risk and
qualified liability notices, APK privacy and six installation steps.

Five real Android 15 screenshots illustrate the installation instructions:
the Santa Cruz Modern live APK in Downloads, Android's blocked-source prompt,
source permission enabled for the file manager, the native Santa Cruz Modern
installer, and that permission disabled after installation. Source permission
names the app opening the APK, not the app being installed; all seven languages
now explain this explicitly. No app dashboard or feature gallery appears here.

Captures use explicit serial `emulator-5590`, a disposable read-only QA emulator,
and File Manager 1.6.2 to open the existing signed live APK. The APK was copied
into the emulator's Downloads folder and installed without launching it, logging
in or contacting the bank. No personal phone or bank data was used. Source and
image hashes are recorded in `docs/media/install/provenance.json`.

Local verification covers all seven catalogues and routes, download ordering,
unchanged release filenames and hashes, installation screenshot provenance, local assets and
file budgets. Chromium covers 21 language/viewport combinations, edition routing,
mobile quick links, screenshot decoding, keyboard dialogs/focus return, matching
language/canonical routes, zero video requests on download pages and access
without JavaScript. At that installation-guide baseline, eight unit tests and the Android
translation checker (1,029 entries in seven languages) passed. Desktop/mobile English and
sampled German/Russian layouts received visual review.

Both existing public APKs match their published SHA-256 values. This is a
website-only change; Android resources, APKs, signing keys and release tags are
unchanged. The security statement describes developer intent and verifiable
release safeguards, not an independent audit or virus-free guarantee. The BSC
terms conflict is the owner's stated rationale, not an independently established
legal conclusion. No native-speaker or legal certification is claimed.


## Current narrated presentation

Six sequential, independent agent passes reviewed and corrected the videos,
spoken actions, captions, transcripts and browser presentation. The final edit
keeps all 13 feature groups and the overview. The 14 original exports total
1,979.398 seconds; the current exports total 1,195.732 seconds, 39.6% shorter.
Explicit reviewed cuts remove 187.067 seconds of repeated or nonessential footage;
idle holds account for another 596.598 seconds. Retained native actions run at
original speed. The overview is 92.6 seconds (about 1:33).

Narration uses concise intent and actions, such as “Enter the amount,” “Tap
Verify” and “Check the transfer receipt.” Each instruction is tied to a recorded
event. No authored instruction may be silently dropped to fit speech. Distinct
transfer/payment variants retain their review, confirmation, Verify and bank
result; repeated waiting/autofill is omitted after the first complete example.
Unavailable card controls, failed setup and abandoned repeated attempts are cut.
Result wording follows the actual recorded outcome. Financial receipts are not
narrated as unconditional transaction completion.

All seven page languages have 14 H.264/AAC videos: 98 narrated MP4s, 98 WebVTT
tracks and 133 synchronized cues per language (931 total). Ordered transcripts
match every timed cue, including consequential actions repeated in distinct flows.
Edge neural voices use `edge-tts==7.3.1`; no paid account/API key was used. Visitors
receive pre-rendered local media in the selected language after Play. Reproduction
is documented in [VIDEO-SCRIPTS.md](VIDEO-SCRIPTS.md#narrated-presentation) and
[README.md](README.md).

The voiced English overview is 1.17 MB; the largest narrated file is 2.12 MB.
The complete deployment is approximately 98.0 MiB, below the 250 MiB budget.
Durations below omit fractional seconds; sizes use decimal MB.

| Video | Original | Current | Voiced English MB |
| --- | --- | --- | --- |
| Overview | 1:48 | 1:32 | 1.17 |
| Login | 0:48 | 0:33 | 0.41 |
| Accounts | 1:01 | 0:45 | 0.40 |
| History | 1:27 | 1:04 | 0.61 |
| Transfers | 5:17 | 3:17 | 2.07 |
| Payments | 3:04 | 1:53 | 1.21 |
| Statements | 1:25 | 0:58 | 0.47 |
| QR | 1:46 | 1:05 | 0.55 |
| Beneficiaries | 3:09 | 2:06 | 1.05 |
| Cards | 1:20 | 0:29 | 0.21 |
| Token | 3:28 | 1:16 | 0.53 |
| Settings | 4:33 | 2:33 | 1.40 |
| Device setup | 1:15 | 0:49 | 0.64 |
| First use | 2:31 | 1:29 | 0.99 |

Current verification:

- All 13 unit tests pass for action windows, speech fit, event anchors, exclusions,
  complete retained/excluded source-event accounting and chronological transcripts.
- All 21 Chromium language/viewport cases pass at 390, 820 and 1440 px, including
  every rendered transcript, lazy loading, keyboard playback, speed selection,
  player isolation, download/privacy routes and no-JavaScript links.
- All 98 localized players decode video and audio. All 931 browser-loaded native
  cues exactly match their ordered transcripts; selected-language caption tracks
  and an actual playing cue pass for every player at 820 px.
- Static checks cover all 14 silent masters, 98 narrated videos and 98 caption
  tracks: canonical action order/text, catalogue and editorial-policy hashes,
  source-event archives, language/timing, fast-start encoding and file budgets.
- Actual decoded speech fits every mandatory window in all seven languages.
  The tightest window is Spanish QR review: 4.224 s within 4.255 s available.
- All 14 final cue sheets received visual review. Fifteen contact sheets contain
  155 actual encoded-video frames covering every cue, reviewed cut boundaries and
  leading overview SMS/results; the beneficiary sheet was regenerated after the
  final acknowledgement correction. All seven languages received mobile/desktop
  caption and transcript visual review. “Statements saved” follows the actual
  2/2 saved result. The bank deletion callback only acknowledges a request;
  narration now says “Check the removal response” in every language.
- The seven current overview AAC tracks are non-silent: mean levels range from
  -23.5 to -21.9 dBFS and peaks from -1.5 to -1.1 dBFS. MP4 hashes accompany these
  measurements in `docs/verification.json`.
- Build, Python compilation and `git diff --check` pass. SHA-256 comparison preserves prior browser acceptance for 91 unchanged
  localized MP4/VTT pairs. All seven changed beneficiary players were retested
  during the actual removal-response cue, and every rendered transcript was
  checked again in all seven languages. A final 21-case locale/viewport probe
  confirms all ordered transcripts and no horizontal overflow after that fix.

The six review passes were:

| Pass | Review and correction |
| --- | --- |
| 1 | Replace explanatory narration with event-anchored actions; preserve every chronological cue. |
| 2 | Fix localized address and truthful outcomes; remove redundant token/QR/settings attempts. |
| 3 | Measure actual speech, fix overlong Copy wording and regenerate all seven-language media. |
| 4 | Review every video; correct labels and confirmation timing; cut repeated SMS and unavailable controls; regenerate. |
| 5 | Review rendered copy and captions; verify all 98 actual localized players and all 931 cues in Chromium. |
| 6 | Audit current artifacts against native outcome semantics; correct deletion acknowledgement in all languages, regenerate and retest; reconcile final evidence. |

Local evidence is retained under `/tmp/bsc-pages-six-pass/iteration4/`,
`iteration5/` and `iteration6/`, with independent pass reports at
`/tmp/bsc-pages-iteration-{1,2,3,4,5,6}.md`. Temporary evidence paths are local
working records; canonical sources, generated media, provenance and concise
machine-readable acceptance results remain in the repository.

Earlier 67-cue, 1,502.134-second narration measurements are historical. Their
slow-network timing and 19-file regeneration comparison are archived separately
in `historicalPresentationMeasurements` in `docs/verification.json`; neither was
rerun or attributed to the current edit. The loading audit below likewise
records the earlier silent-media baseline.

Publication uses `scripts/publish.py` after committing the verified sources and
media. The publisher compares every anonymously deployed file and both APK
downloads against local SHA-256 values. The current signed app remains 1.12.1
(28); changes since that app build affect capture tooling and website media. No
new Android build or owner-bank validation was needed for these media edits.

## Reviewed video preview images

All 14 images shown before Play were reviewed and replaced with frames from the
final native videos. Beneficiaries now shows readable recipient details instead
of pasted JSON. Other previews show clean search results, statement periods,
review details, an active Token BSC code, a complete QR, language selection and
the home dashboard. Keyboards, loading states, pending token setup and generic
confirmation overlays are avoided where a useful clean frame is available.

`src/poster-frames.json` pins each reviewed timestamp and source-video SHA-256.
`scripts/refresh-posters.py` reproduces the images and `docs/media/posters.json`
records their hashes. The checker rejects changed source videos or stale images
until the frame is reviewed again. Preview and player-poster URLs hash the JPG
itself, so replacing an image invalidates its browser cache independently of the
video. Narration regeneration also refreshes the reviewed frames.

Chromium checked every preview across seven languages at 390, 820 and 1440 px:
294 image decodes, matching preview/player posters and current image hashes, with
zero MP4/VTT requests before Play. All 14 actual preview displays received visual
review at mobile and desktop sizes. Evidence: `/tmp/bsc-pages-six-pass/posters/`.
The video, audio, caption and transcript content from the sixth pass is unchanged.

## Original capture and website baseline

The following baseline describes the earlier silent revision-4 exports. Its
capture evidence remains applicable; the current playback and file-size results
are recorded above.

The redesigned showcase puts the main video beside the introduction, followed by
six concrete UX benefits, actual SMS empty/filled frames and task-first chapters.
It demonstrates implemented interactions without asserting unsupported feature
absences in the original app. The full tour covers all 13 groups in about 1:48,
starting with SMS-only automatic login and financial SMS fill/Verify/receipt.

All 30 revision-4 native scenarios passed on explicitly selected disposable
emulators. All nine required bank-SMS scenes record automatic-fill callbacks;
none types a bank or demo code. SMS assistance stays enabled except the documented
initial pre-choice and settings off/on cases. Login entry events are absent from
non-authentication/setup chapters, and quiet setup is excluded from exported
footage and galleries. Financial examples use native fake-bank state machines.
Five new financial fixture rehearsals and 21 tooling tests passed.

The first SMS clip was retaken after visual review found a fixture-clock progress
hold obscuring its result. The final clip shows the empty field, filled-code
verification and authenticated accounts; the next shows empty/filled SMS,
explicit Verify and receipt. Overview checks require those actual result holds
and prohibit cuts spilling into the next scenario. No production delay or banking
control changed. Synthetic approval results are disclosed, not drawn as fake
Android dialogs. Card numbers stay masked to the last four digits.

Every chapter received sampled visual review; every final tour excerpt was
reviewed, with denser transition review for both leading SMS sequences. Captions
in all seven languages match actual scene/hold timing and transcripts. The main
seven-second cues describe the visible interaction rather than listing unrelated
features. Android sharing uses labeled QA-only targets and makes no delivery claim;
PDF saving callbacks and decoded QR input remain explicitly synthetic fixtures.

Static routes, local links, privacy, versioned downloads, 14 silent H.264 videos,
98 caption tracks, fast-start metadata, event bounds, source provenance, exclusion
rules and file budgets pass. The complete Pages deployment is approximately
20.6 MiB. Browser checks cover seven languages at 390, 820 and 1440 px: layout,
keyboard dialogs/focus, chapter links, user-started tour, playback/speed,
transcripts, media, privacy and APK links.

Production APKs remain 1.12.1 (28), built from b906472 and signed with the retained
distribution key. Their prior verification remains applicable: 281 JVM tests per
debug/demo/live variant, targeted Android/card/language checks, build/lint and
Play credential boundaries, signed offline startup and exact installed hashes.
Current changes affect website content and capture tooling only. Capture source
and distribution source commits are recorded separately in media provenance.

All identities, bank transports and documents in recordings are fictional. Bank
authorization, current live compatibility, real owner-device SMS consent and
owner-account validation remain unresolved. No independent legal/native-speaker
certification or Google Play submission is claimed.

Machine-readable results: [verification.json](docs/verification.json).
Repeatable commands: [README.md](README.md) and [VIDEO-SCRIPTS.md](VIDEO-SCRIPTS.md).

## Historical video loading and size audit

At the earlier loading audit, the published site used `preload="none"`: a Chromium network inspection
confirmed no MP4 requests on entry or while changing chapters. However, its 14
video posters request 1,035,042 bytes immediately. That local loading update introduced an eager
93 KB hero JPG, lazy chapter JPGs and inert player templates. Neither videos nor
captions can load until Play. JPG links open the MP4 directly without JavaScript.
Native controls, captions, selected speed and keyboard focus work after playback
starts. Starting another video pauses the previous player.

The mobile local check requested one 92,837-byte JPG initially, 91.0% fewer poster
bytes. Simulating 50,000 download bytes/second (400 kbps) and 400 ms latency,
playback began 4.52 seconds after Play. This is a local Chromium simulation,
not a guarantee for every device, connection or hosting response. The public
host advertises byte-range support and its MP4s already have fast-start metadata.

All 21 language/viewport browser combinations and static checks passed, including
zero video/caption requests while browsing chapters, keyboard-started playback,
speed selected before loading, playback isolation and no-JavaScript preview links.
Local reports and screenshots: `/tmp/bsc-pages-video-browser-results`.

The 14 silent H.264 videos total 11,641,965 bytes (11.64 MB), at 540×1200 and
15 fps. Sizes below use decimal MB; chapter timing and all 98 caption tracks are
preserved.

| Video | Duration | MB |
| --- | --- | --- |
| Overview | 1:48 | 0.91 |
| Login | 0:48 | 0.35 |
| Accounts | 1:01 | 0.36 |
| History | 1:27 | 0.54 |
| Transfers | 5:17 | 1.96 |
| Payments | 3:04 | 1.21 |
| Statements | 1:25 | 0.41 |
| QR | 1:46 | 0.53 |
| Beneficiaries | 3:09 | 1.01 |
| Cards | 1:20 | 0.31 |
| Token | 3:28 | 0.68 |
| Settings | 4:33 | 1.69 |
| Verification | 1:15 | 0.66 |
| First use | 2:31 | 1.01 |

Further tour compression was tested without replacing published media. H.264
`slow`, CRF 24 increased its 908,404 bytes to 1,002,441. CRF 28 reduced it to
832,345 bytes (8.4%, 76 KB saved; SSIM 0.999095 against the existing encoding).
The existing small videos are retained to avoid another lossy encoding for that
limited gain. The optimization reduces initial requests and transferred previews.
These local website changes have not been deployed.
