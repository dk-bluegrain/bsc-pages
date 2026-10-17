# Verification

Android 1.12.1 (28): 281 JVM tests passed per debug/demo/live variant. Four
targeted card and language Android cases passed, including PAN masking before
and after details/copying, exact clipboard values, app-switch privacy and all
seven languages at normal and 150% text size. Signed builds, lint and variant
boundary checks passed. Signed APK installation and offline startup passed,
and installed hashes match both distribution files. No personal credentials or banking
operations were used. Detailed private source evidence:
https://github.com/dk-bluegrain/bsc/blob/main/publishing/CARD-MASKING-VERIFICATION.md

All 34 approved revision-3 fictional capture scenarios passed. Scripts preceded
retakes and specify reading pauses, with longer holds for consent, reviews,
receipts and uncertain outcomes. SMS assistance is enabled except for initial
pre-choice onboarding and the configuration off/on example. SMS-only automatic
login uses a labeled synthetic approval result; operation codes retain Verify.
Fourteen silent H.264 videos include an approximately 104-second overview;
98 WebVTT tracks match the seven-language transcripts. Actual input coordinates
and timestamps accompany the footage. Native-ring calibration and persistent
vector rings preserve tap visibility through window changes. Complex chapters
may exceed 120 seconds for readability. The card chapter and overview were retaken/regenerated for 1.12.1 and visually
reviewed; only the last four digits are displayed, including during copying.
Unchanged chapters retain their prior approved fictional captures and review.

Static routes, local assets, privacy links, versioned downloads, codec/audio,
fast-start metadata, caption timing/parity, event bounds and deployment budgets
passed. The docs deployment is approximately 21.5 MiB. Browser checks passed all
21 language/viewport combinations (390, 820, 1440 px), including keyboard dialogs,
focus restoration, chapters, speed, transcripts, playback, privacy and downloads.

Bank authorization, owner-account validation, actual owner-device SMS consent
and current live compatibility remain unresolved. These checks do not certify
linguistic/legal correctness. No Play submission.

Machine-readable results: [verification.json](docs/verification.json).
Repeatable commands: [README.md](README.md).

The supplementary screenshot run through recording helpers stopped because a
tap overlay had no focused window. The ordinary Android language fixture was
rerun successfully and all 56 screenshots were retained and reviewed. Signed
startup/hash evidence is retained outside source in the final masking smoke run.
