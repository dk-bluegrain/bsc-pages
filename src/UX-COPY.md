# Benefit-led website copy

`ux-copy.json` supplies the presentation copy for the redesigned showcase.
It contains `languages` with complete `es`, `en`, `de`, `fr`, `ru`, `uk`, and
Brazilian `pt` catalogues. Spanish supplies the meaning; German uses Sie,
French vous, and Russian/Ukrainian polite plural actions. Every locale has the
same schema and stable identifiers.

The writing shows useful outcomes: a code without copying, remembered access,
separate currencies, search, PDFs and legible reviews. It makes no comparison
with another app's feature set, no claim about missing original-app features,
and no promise of live compatibility, affiliation, store availability, speed
or measurable performance. Existing download warnings and edition details
remain necessary alongside this presentation copy.

All values are UTF-8 plain text with no formatted placeholders. Escape strings
when rendering HTML. The fixed labels and descriptions below provide shared
context for all seven translations; JSON itself cannot contain comments.

## String contexts

| Field | Display and meaning |
| --- | --- |
| `eyebrow` | Small hero identifier: product name and Android platform. Does not claim bank affiliation. |
| `headline` | Main hero heading. Spanish is “Menos pasos. Más claridad.” and English is “Fewer steps. More clarity.”; other languages preserve that direction without adding a quantified performance claim. |
| `intro` | Hero paragraph introducing filled codes, distinct currencies and reviewing amounts. Leads into the visible feature tour, not banking credential entry. |
| `watchLabel` | Action to watch the feature tour. It does not start a download, login or operation. |
| `benefitsTitle` | Heading above the six concrete benefits. |
| `benefitsIntro` | Short progression from access to finding and reviewing; no unsupported comparison or guaranteed result. |
| `proofLabel` | Link to see the relevant native UI walkthrough. “Proof” in the schema name does not mean proof of a real banking session or bank approval. |
| `flowTitle` | Heading for browsing focused chapters by task. |
| `flowIntro` | Explains that non-authentication chapters start at the task rather than replaying login. The media edit must actually follow that presentation requirement. |
| `smsSpotlightTitle` | Attention heading about code arrival and the user's next choice. It must sit beside the explanation of Android message approval. |
| `smsSpotlightBody` | Optional SMS assistance, Android approval to share one message, code filling, SMS-only login continuation and explicit Verify for operations. Do not separate this qualification from the spotlight heading. |
| `mediaNote` | One clear, visible scope note near the tour and chapter browser: fictional data, advanced fake-bank flows, labeled synthetic SMS approvals/results, and a simpler downloadable basic demo. This avoids repeating the same disclaimer in every benefit. It is not a substitute for edition/download warnings. |
| `benefits[*].id` | Stable non-visible identifier, never translated. |
| `benefits[*].title` | Concrete benefit-card heading, without a comparative claim. |
| `benefits[*].body` | Two short descriptions of the useful feature and any material choice/limit. These are introductions, not exact video transcripts. |
| `benefits[*].chapter` | Canonical chapter ID for the demonstration link; never translated. |
| `chapters[id].title` | Concise task/outcome heading for the chapter. |
| `chapters[id].body` | Exactly two sentences per language. Describes the user outcome and preserves material SMS, handoff, storage, validation or availability limits where relevant. |
| `overviewCues[*].id` | Canonical chapter ID for an overview segment, in the separately agreed overview order. |
| `overviewCues[*].text` | Short, localized tour cue, at most 160 Unicode characters. It describes the matching segment and is not interchangeable with unrelated scenario/stage captions. |

## Benefit map

| ID | Outcome | Linked chapter |
| --- | --- | --- |
| `sms` | Fill SMS codes without copying, after Android one-message approval; only SMS-only login may continue automatically, operations keep Verify. | `login` |
| `biometrics` | Opt-in remembered username AND password, unlocked with biometrics; device/login checks remain separate when needed. | `verification` |
| `balances` | DOP and USD remain distinct; hide amounts for a more private view. | `accounts` |
| `search` | Search recipients by bank-supplied details and find transactions with search/filters. | `beneficiaries` |
| `statements` | Native PDF reading and single/batch period saving to the chosen destination. | `statements` |
| `qr-reviews` | Readable QR request details and recipient/currency/amount review before confirmation. | `qr` |

## Canonical chapter context

Keep the `chapters` object in this order even when the renderer changes its
presentation order. No chapter ID or translation depends on display position.

| ID | Two-sentence introduction context |
| --- | --- |
| `first-use` | Terms/privacy before express acceptance, seven languages and optional SMS assistance/manual fallback. |
| `login` | Android one-message approval fills the code; only SMS-only login can continue automatically. Keyboard autofill still retains Verify. |
| `verification` | Remembered access with biometrics and device registration inside the app. Combined questions retain Verify; external checks use the indicated channel. |
| `accounts` | DOP/USD account details and balance hide/show. |
| `history` | Search and incoming/outgoing filters, then explicit account-transaction CSV sharing. Does not claim the exported file contains only currently filtered rows or every historical bank record. |
| `statements` | Native PDF pages/zoom and saving one or several offered periods. Saved destination copies remain there independently of session closure. |
| `transfers` | Source/recipient, amount, currency and fees before separate transfer confirmation; SMS arrival, approved sharing, filled-code review and explicit Verify. |
| `payments` | Service/source/amount before confirmation; SMS code fills after message approval, with explicit Verify. No silent money authorization. |
| `beneficiaries` | Search, review, separate save/delete; validation is not automatic saving or a payment. |
| `cards` | Bank-supplied read-only details. Card numbers ALWAYS stay masked to the LAST FOUR digits, even after revealing details; full-number copying requires an explicit action and an actual bank-supplied full number. No inferred number and no advertised activation/block/loss/theft/travel administration. Services provide official-channel information only. |
| `token` | Contract and enrollment/storage choices, external identification in the indicated channel, generated code versus SMS distinction and confirmed unlinking. |
| `qr` | Request memo/amount and readable recipient details, saving/printing. Reading a QR does not authorize payment or registration. |
| `settings` | Language, actual SMS-assistance switch, separate delivery preferences, profile/help/logout; history before uncertain-result reconciliation, which neither repeats nor cancels an operation. |

The central media note establishes fictional native recordings, labeled
synthetic SMS approval/results and the simpler basic demo. The individual
chapter texts keep consequential conditions without describing transports,
keys, callbacks, test method names or other implementation details.

## Overview sequence and timing

The thirteen `overviewCues` use canonical IDs, but intentionally start with two
SMS benefits. Their order is:

```text
login, transfers, first-use, verification, accounts, history, statements,
payments, beneficiaries, cards, token, qr, settings
```

The agreed edit reserves about 14 seconds for SMS-only login, about 18 seconds
for financial review → filled code → explicit Verify → result, then about
7 seconds for each remaining group: approximately 109 seconds total. These
are editing targets, not invented timestamps; final cues must follow the
actual footage and its approval/filled-code holds.

The first cue describes arrival → approval to share ONE message in Android →
code fills → SMS-only login may continue. The second describes a financial
operation's approved message → filled code → review and explicit Verify before
the result. The synthetic nature of recorded approvals/results must remain
visible in the media note and the actual video labels. No real Android consent
dialog may be fabricated or claimed absent. Other SMS challenges follow the
same arrival/fill behavior; the tour does not show bank SMS codes typed manually.
DEMO code 123456 and generated Token BSC codes remain separate, non-SMS cases.

The other eleven segments cover first-use/language, biometrics/registration,
accounts, history, PDFs/batch saving, payments, beneficiaries, read-only cards,
token, QR and settings. Do not repeat login setup to introduce those tasks.

## Sources and verification

Copy was checked against current `src/content.json`, `src/CONTENT.md`, the
revision-3 video directions, and the latest `LiveCardsUi.kt` masking/copy logic.
The new asset is separate from existing content, subtitle catalogues, scripts,
media and build files. No existing file was rewritten for this bounded task.

Validation checks all seven schemas, six benefit objects and valid chapter
links, canonical thirteen-chapter order, two sentences per chapter body,
exactly thirteen unique overview IDs in the agreed order, nonempty strings,
no accidental English paragraph fallback, and the 160-character overview
ceiling. It does not certify native-speaker review, new footage timing or
visual fit. The site owner handles renderer integration, media validation and
publication.

Final tour cues after the two SMS sequences describe only the visible seven-second
interaction: language choice, registration re-entry, privacy, search, PDF paging,
receipt, recipient review, masked copy, active token, QR review and SMS settings.
Broader chapter features belong in the chapter introductions and full videos.
