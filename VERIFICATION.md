# Feature-first website and native media verification

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
