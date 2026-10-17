# Website content context

`content.json` contains seven complete catalogues under `languages` in this order:
Spanish (`es`, authoritative meaning), English (`en`), German (`de`), French
(`fr`), Russian (`ru`), Ukrainian (`uk`), and Brazilian Portuguese (`pt`). All
catalogues have the same keys, chapter identifiers and section order. Language
names are autonyms. Use Spanish as the default; use each catalogue on its own
addressable page and matching privacy page.

This file is the shared context catalogue for every string in all seven
languages. JSON has no comments, so the context sits here rather than in XML
comments. These are website assets, not Android string resources. They contain
no formatted placeholders, bank-supplied personal data or user-generated text.
Do not turn prose into HTML without escaping it. Preserve punctuation, accents,
Cyrillic text and typographic apostrophes as UTF-8.

## Rendering context for every key

| Key | Context and display | Meaning and constraints |
| --- | --- | --- |
| `name` | Persistent language-selector option | Native language name; never translate it into the current page's language. |
| `title` | Document title and app introduction | Independent BSC app showcase; no bank endorsement claim. |
| `tagline` | Short hero heading | App positioning, not a promise of compatibility or financial performance. |
| `intro` | Hero paragraph | Introduces both offline demo and experimental banking edition. |
| `demoTitle` | Demo download-card heading | The basic downloadable offline demo. |
| `demoBody` | Demo download-card description and edition comparison | Lists basic local features, fictional data and lack of bank connection; explicitly excludes a promise of every advanced flow. |
| `demoAction` | Demo APK download link | Downloads the demo, not installation or account opening. |
| `liveTitle` | Banking download-card heading | Always visibly experimental. |
| `liveBody` | Banking download-card description and edition comparison | Configuration restored, bank authorization and owner-account validation unresolved, current compatibility unestablished. |
| `liveAction` | Banking APK download link | Always visibly experimental; not an official-bank download. |
| `warning` | Prominent warning beside banking download | Unresolved bank authorization and owner-account validation; restoring configuration proves no compatibility; independent app, no official-app or Google Play claim. Must not be hidden in a tooltip or only in privacy prose. |
| `overviewTitle` | Overview video heading | A short native-app tour. |
| `overviewBody` | Visible overview-video introduction | Fictional data and fake bank transports; advanced filmed UI is distinct from downloadable basic demo capabilities. |
| `chaptersTitle` | Chapter-browser heading | Introduction to focused flow chapters. |
| `simulatedLabel` | Chapter/media status badge | Fake bank transport exercises the native banking UI, never a recorded real banking session. |
| `demoLabel` | Basic-demo feature badge | Use only for features actually included in the downloadable offline demo. Not interchangeable with `simulatedLabel`. |
| `handoffLabel` | External-step badge | Continues in an official channel or the bank-supplied HTTPS page; returning is not proof of completion. |
| `compareTitle` | Editions-comparison heading | Helps choose a download. |
| `requirementsTitle` | Requirements heading | Android installation section. |
| `requirementsBody` | Requirements paragraph | Android 8.0+, API 26, signed sideload APK, banking connectivity and bank checks, no website credential entry. |
| `installTitle` | Installation heading | Direct APK installation, not Google Play. |
| `installSteps[0]` | First ordered installation step | Choose the edition and read experimental limitations first. |
| `installSteps[1]` | Second ordered installation step | Same-version APK and SHA-256 check; compare before installing. |
| `installSteps[2]` | Third ordered installation step | Android installation permission applies to the downloading app; disable it afterwards. No promise of identical Android UI wording. |
| `installSteps[3]` | Fourth ordered installation step | Read app notices and terms; demo fictional, bank controls remain. |
| `installSteps[4]` | Fifth ordered installation step | Banking APK retains `com.santacruz.modern` but uses the dedicated distribution signing key. It cannot update an existing Santa Cruz Modern installation with a different signature. If Android blocks the update, preserve the existing app and its data and use the separate demo or contact support. Never recommend uninstalling to resolve this mismatch: token state and uncertain-operation markers could be lost. This refers to Santa Cruz Modern, not an official bank app. |
| `versionLabel` | Label beside release version | Version comes from build metadata: currently 1.12.0 (27). This string is only the label. |
| `privacyLabel` | Matching-language privacy-page link | Link to that locale's privacy page, not to a generic untranslated page. |
| `supportLabel` | Support heading/link | App help and feedback, not bank support. |
| `supportBody` | Support paragraph | Preserves actual project contact; forbids sending credentials, codes, identity documents or account details; sends banking issues to official channels. |
| `transcriptLabel` | Video transcript disclosure | Accessible text alternative to a video; an actual transcript must match the footage and caption timings. |
| `screenshotsLabel` | Screenshot-gallery heading/control | Native UI captures using fictional data. |
| `speedLabel` | Video playback-speed control label | A user-selected playback rate; no autoplay. |
| `closeLabel` | Screenshot-dialog close button | Dismisses the enlargement dialog without navigation. |
| `skipLabel` | Keyboard skip-navigation link | Focuses main content. |
| `privacyTitle` | Privacy document title/heading | Covers both website and app, with distinct scopes. |
| `privacyIntro` | Privacy introduction | Explicitly separates site, offline demo and banking edition. |
| `chapters[*].id` | Stable routing/media identifier | Non-visible identifier, identical in every locale; never translate. |
| `chapters[*].title` | Chapter navigation and heading | Names a focused flow; see per-chapter context below. |
| `chapters[*].body` | Visible chapter introduction | Describes native behavior, simulation scope, confirmations and basic-demo limits. Must appear with the chapter rather than only in metadata. |
| `chapters[*].notes` | Visible safety/scope note next to chapter media | Every chapter repeats fictional identities, fake bank transport, no real submitted operation and limited basic demo scope. Intentional repetition keeps directly accessed chapters accurate. |
| `privacySections[*].title` | Privacy section heading | Same six topics and ordering across all locales. |
| `privacySections[*].body` | Privacy section paragraph | Distinct data scopes and retention; see section context below. |

## Chapter context

Every `notes` value applies to its adjacent chapter and uses the same wording
within each language. A simulated flow is a recording of native live-bank UI
against a fake transport. It must not be called an implemented basic-demo
feature. None of the copy asserts current live-bank compatibility.

| Stable ID | Context for title and body |
| --- | --- |
| `first-use` | Independent-app notice, opening terms and privacy, explicit acceptance, seven-language selection; supplied bank text retains its language. |
| `login` | Manual login, remembered username AND password, strong biometric protection and removal. Biometrics never establishes bank approval. Basic demo needs no banking credentials. |
| `verification` | Bank-required login setup, code verification and device approval. Approved one-message SMS-only login can auto-verify; keyboard autofill, security questions and operations retain explicit Verify. External identity check uses bank-supplied HTTPS page. |
| `accounts` | Account-specific currencies and balances, hide/reveal balances. Basic demo includes fictional accounts and local balance privacy. |
| `history` | History/search, incoming/outgoing filters and explicit CSV sharing. Basic demo claims are limited to history/search/export. |
| `statements` | Available periods, synthetic PDF preview, individual/selected saves, Android picker and sharing; not a basic-demo feature. |
| `transfers` | Own/same-bank/other-bank contexts, currencies, amounts, fees, memo and separate review/authorization. Basic demo limited to simulated own/saved-beneficiary transfers. |
| `payments` | Services and credit cards, source account, amount, review and bank authorization; demo test receipts are not money movement. |
| `beneficiaries` | Lookup/validation, review, save and deletion. Validation is neither saving nor money authorization. Basic demo uses fictional recipients. |
| `cards` | Read-only bank-supplied fields, reveal/copy of exact identifiers and full numbers only when supplied; unimplemented administration explains the limit with official handoffs, no card-write API request. |
| `token` | Contract reading, enrollment/storage consent, verification, code generation, unlinking and official identity handoff; basic demo has no banking-token enrollment/generation. |
| `qr` | Account/recipient sharing, payment-request context, scanning/manual entry, recipient review, saving and printing where supported. QR never authorizes writes or money. Unsupported third-party formats remain unsupported. Do not interpret a shareable account QR as a universal bank payment request. |
| `settings` | Language/profile/demo settings, help, logout, and explicit reconciliation after actual bank history/status checking. Reconciliation neither repeats nor cancels prior operations. |

## Privacy section context

1. **Static website:** no banking login, credential form, analytics or own
   backend. Browser-local presentation is separate from hosting infrastructure.
2. **Hosting and external links:** GitHub Pages and Releases may process IP and
   request logs under GitHub's policy. External support/bank/service links have
   their own terms. Do not claim that using the site transmits no data anywhere.
3. **Offline demo:** fictional data, local persistence, reset/clear/uninstall
   behavior; separately exported files can outlive app data.
4. **Banking edition:** bank requests, optional Android Keystore encryption plus
   strong biometric authentication for remembered login, explicit contract and
   encrypted-seed storage consent for token; no persistent sessions/generated
   codes. This is a scope summary linking users to full in-app policy, not a
   replacement legal contract.
5. **Files and device services:** private PDF preview cache versus persistent
   user-selected save destinations; provider synchronization and receiving-app
   copies; external identification and optional Android/Google modules.
6. **Limits and contact:** independent/experimental, unresolved bank permission
   and owner-account validation, no established current compatibility, no Play
   submission, project contact and no sensitive information in support mail.

## Source review and verification

Copy was checked against the task plan, `TRANSLATIONS.md`, current project
`README.md`, `app/build.gradle.kts`, and `ui/BankingApp.kt` (welcome/demo routing,
accounts, CSV export, local reset, profile and official-channel links).
The downloaded demo is not advertised as a preview of every native live flow.
Version/minimum API were read from the Android build configuration, not inferred.
Banking security and export privacy follow the current project documentation.
The fifth installation step follows `RELEASE-NOTES.md` and the distribution
checkout’s `DISTRIBUTION.md` signing-identity boundary. The unchanged package name
does not permit updating an installation signed with a different key.

The accompanying verification checks JSON decoding, identical schema, all seven
locale codes, the exact thirteen chapter IDs, five install steps, six privacy
sections, nonempty strings and no accidental English-copy fallback for chapter
and privacy paragraphs. It does not certify native-speaker review, legal review,
video completeness or visual fit. Captions/transcripts must be written from the
actual footage; chapter introductions are not claimed to be verbatim video
transcripts. Website changes do not modify Android resource catalogues.
