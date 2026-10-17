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
