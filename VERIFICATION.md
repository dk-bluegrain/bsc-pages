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
without JavaScript. The existing eight unit tests and the Android translation
checker (1,029 entries in seven languages) pass. Desktop/mobile English and
sampled German/Russian layouts received visual review.

Both existing public APKs match their published SHA-256 values. This is a
website-only change; Android resources, APKs, signing keys and release tags are
unchanged. The security statement describes developer intent and verifiable
release safeguards, not an independent audit or virus-free guarantee. The BSC
terms conflict is the owner's stated rationale, not an independently established
legal conclusion. No native-speaker or legal certification is claimed.


## Current narrated presentation

The quicker edit removes idle hold frames while keeping recorded actions at
normal speed. The original 14 exports total 1,979.398 seconds; the edited exports
total 1,502.134 seconds, 24.1% shorter. Individual chapters are 20.9–28.7% shorter.
The tour changes from 108.533 to 91.8 seconds (about 1:32).

Every video has narration in all seven page languages: 98 H.264/AAC MP4s, with
67 synchronized speech cues per language and matching captions/transcripts. Edge
neural voices were generated with `edge-tts==7.3.1`; no paid account/API key was
used. The site serves pre-rendered local media and downloads only the selected
language after Play. Voice choices, alternatives, scope and regeneration commands
are in [VIDEO-SCRIPTS.md](VIDEO-SCRIPTS.md#narrated-presentation) and [README.md](README.md).

The voiced English tour is 1.27 MB. The largest voiced file in any language is
2.12 MB; the complete deployment is approximately 105.5 MiB, below the 250 MiB
budget. Displayed durations below omit fractional seconds; sizes use decimal MB.

| Video | Original | Edited | Voiced English MB |
| --- | --- | --- | --- |
| Overview | 1:48 | 1:31 | 1.27 |
| Login | 0:48 | 0:35 | 0.45 |
| Accounts | 1:01 | 0:48 | 0.38 |
| History | 1:27 | 1:08 | 0.58 |
| Transfers | 5:17 | 4:01 | 2.07 |
| Payments | 3:04 | 2:19 | 1.23 |
| Statements | 1:25 | 1:04 | 0.46 |
| QR | 1:46 | 1:23 | 0.63 |
| Beneficiaries | 3:09 | 2:27 | 1.14 |
| Cards | 1:20 | 0:59 | 0.33 |
| Token | 3:28 | 2:28 | 0.81 |
| Settings | 4:33 | 3:25 | 1.72 |
| Device setup | 1:15 | 0:56 | 0.68 |
| First use | 2:31 | 1:52 | 0.99 |

Verification performed locally:

- Eight unit tests passed for protected action windows, hold budgets, overlapping
  holds, translation lengths, scene boundaries and optional narration deadlines.
- All 21 language/viewport browser combinations passed, including zero MP4/VTT
  requests before Play, keyboard playback, the correct localized MP4, decoded
  unmuted audio in seven languages, playback isolation and no-JavaScript links.
- Static checks passed for all 14 paced masters, 98 narrated MP4s and 98 caption
  tracks: language tags, durations, ordered speech cues, hashes, fast-start metadata,
  retained input events, edited event mapping, provenance and file budgets.
- All seven voiced tours decoded with non-silent audio and peaks between -2.2
  and -1.5 dBFS. These measurements do not replace native-speaker listening review.
- At simulated 50,000 download bytes/second (400 kbps) with 400 ms latency,
  voiced playback began 6.49 seconds after Play. Initial load requested one JPG
  and no MP4 or captions; only the English MP4 was requested after the click.
  This is a local Chromium simulation, not a hosting/device guarantee.
- Regenerating the tour from the pinned unedited source preserved all 19 tested
  media, caption, manifest and event hashes. Partial raw caption regeneration is
  rejected before it can mix original and edited timelines.
- Sampled edited-tour frames retain both leading SMS sequences' empty/filled
  fields and their actual simulated account/receipt results.

Reports and visual samples: `/tmp/bsc-pages-narration-browser-results`.
These website/media changes have not been published. No production APK or live
banking behavior changed, and the earlier owner-account validation limits remain.

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

## Video loading and size audit

The published site already uses `preload="none"`: a Chromium network inspection
confirmed no MP4 requests on entry or while changing chapters. However, its 14
video posters request 1,035,042 bytes immediately. The local update uses an eager
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
