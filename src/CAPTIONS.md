# Caption copy and recording context

Source caption fields now carry adjacent `_fieldContext` English metadata in
all seven languages, including a separate comment for each string-list item.
Each comment identifies the recorded context, display stage, source and absence
of interpolation arguments. The catalogue loader strips metadata before media
processing; `scripts/check.py` verifies coverage and mirrored context. Final
transcripts/WebVTT are generated from the timed `narration-actions.json` phrases,
whose existing per-phrase context stays adjacent to the seven translations.
Never edit generated text independently of its spoken/timed source.

The current recording specification is
`/extra/dkropachev/bsc-distribution/publishing/VIDEO-SCRIPTS.md`, revision 3,
with executable policy in `scripts/capture/video-scripts.json`. These scripts
were written before the retakes. Earlier revision-2 assumptions that no
approved-message login can auto-verify, that settings have only delivery
preferences, or that card administration is demonstrated are superseded.

`captions.json` has this shape:

```text
languages → es/en/de/fr/ru/uk/pt → chapter ID or overview → string array
```

Each of thirteen chapters has four semantically aligned summary cues in every
language. `overview` has thirteen cues in chapter order. These summaries explain
the scope of a scenario rather than narrating a click at an invented instant.
They retain fictional-data, fake-bank and basic-demo boundaries.

`scene-captions.json` has this shape:

```text
languages → es/en/de/fr/ru/uk/pt → scene key → string
```

There are twenty-three scene keys per language. Timed scene text describes
actual recorded holds, not an instruction to invent a result. Both catalogues
use UTF-8 plain text, no formatted placeholders, and a maximum of 160 Unicode
characters per cue. Escape text when rendering HTML. Spanish supplies the
source meaning; translations follow the project's established language styles.

## Current SMS behavior

The source was checked directly in `ui/SmsSettings.kt`, `ui/SmsUserConsent.kt`,
`ui/BankSmsCodeReader.kt` and the login challenge in `ui/LiveBankScreen.kt`.

First-use assistance is optional. Users can enable it or continue manually.
The actual `sms_assistance` setting is an on/off switch. Enabling it also chooses
SMS delivery. The separate SMS/EMAIL/Ask preference chooses a bank-offered code
delivery channel; it does not replace the assistance switch or control every
Android autofill service.

With assistance enabled, Android's one-message User Consent flow requests
approval to share one SMS. This does not request `READ_SMS` or provide inbox
access. Only an approved one-message result for the active **SMS-only login**
can automatically verify that login. The recorded approval/result uses a
fictional SMS fixture; do not imply a real bank approved the account.

Keyboard/system autofill is a separate path: filling a code never submits it.
Combined security-question challenges, transfers, payments and beneficiary
changes retain explicit Verify even after a one-message approval. Token
challenges also retain their explicit action. Manual fallback remains available
in the app, even though the video policy does not type bank SMS codes.

Every video has assistance enabled after any initial pre-choice onboarding.
Only the settings scene switches assistance off and restores it on. Only that
configuration scene temporarily changes delivery preferences before restoring
SMS. Offline DEMO authorization code **123456** is not an SMS. A generated
**Token BSC** code is not an SMS either. Short passwords/security answers remain
explicit entry; long fictional recipient payloads are pasted once.

## Current card behavior

The live route uses `UnavailableCardServices` in `ui/LiveCardsUi.kt`.
`network/LiveCards.kt` supplies the read-only fields. Card-service entry is
informational: it sends no activation, block/unblock, loss/theft or travel
administration request. Do not retain the earlier control-change/loss/theft/
travel recordings as advertised app capabilities.

Holder names appear only if supplied by the bank. Revealing/copying the bank's
identifier preserves that identifier; it does not infer a card number. A full
card number can appear only if the bank explicitly provides it. Masked digits
are never reconstructed into a PAN. The new cards chapter and overview describe
these conditions without promising the fixture actually displays a full PAN.
The basic demo has no card administration.

## Summary-cue context

Each chapter starts with its fictional native UI or demo scope and ends with a
relevant limitation. Basic offline-demo features are distinct from the native
banking UI exercised against fake transports. First-use explains optional SMS
assistance. Login distinguishes simulated biometrics, one-message approval and
keyboard autofill. Verification preserves combined-question/device/setup
requirements. Cards now describe read-only data and informational services.
Settings distinguish the assistance switch, delivery preference and uncertain
operation reconciliation.

The `content.json` chapter introductions are broader prose, separate from these
short cue arrays. Relevant first-use/login/verification/settings bodies and the
banking privacy summary were reconciled with the new consent behavior. The cards
title/body no longer promote simulated card changes; they explain read-only
fields, conditional full-number availability and official-channel information.
Other chapter prose and existing installation/signing guidance are preserved.

## Selected scenario coverage

| Chapter | Current capture coverage and limits |
| --- | --- |
| `first-use` | `FirstUseNoticeTest.privacyIsAvailableBeforeTermsAndNeverAcceptsThem` and `bankingStaysBlockedUntilTermsOpenedAndExplicitlyAcceptedThenAcceptancePersists`: independent-app notice, opening privacy/terms and explicit acceptance; the actual first-use assistance choice is optional. `ShowcaseExtraTest.languageSelection` opens the picker and selects Spanish. No filmed switch through all seven languages is claimed. |
| `login` | `LiveScreenTest.rememberingCredentialsDefaultsOnAndRequiresBiometricSaveBeforeLogin` and `savedLoginWaitsForBiometricsThenSubmitsAutomatically` use simulated biometric callbacks. `rememberedSmsChannelRequestsDeliveryThenWaitsForExplicitVerification` uses synthetic system autofill and explicit Verify. Added `approvedSmsMessageCompletesOnlyTheCurrentSmsLoginWithoutAnExtraVerifyTap` demonstrates the distinct synthetic approved-message result: only the current SMS-only login auto-verifies. No filmed physical fingerprint prompt, personal SMS or real-bank approval claim. |
| `verification` | `LiveScreenTest.systemSmsAutofillKeepsCombinedQuestionAndWaitsForVerify` preserves separate security-answer and code fields with explicit Verify. `untrustedDeviceCannotFetchAccountsOrEnrollSilently` shows a blocked device. `LoginPrerequisitesScreenTest.requiredPasswordIsConfirmedAndReturnsToLoginWithoutReadingAccounts` shows mismatch, correction and return to login. Revision 3 also selects `registrationResumesThroughBiometricsWithoutExitingOrReusingPassword`; a resumed fixture flow does not establish current bank compatibility. |
| `accounts` | `ShowcaseExtraTest.accountsAndPrivacy`: basic demo hide/reveal balances, USD/DOP switching, real upward/downward swipes with direction arrows and account detail. No live-bank read. |
| `history` | `LiveScreenTest.loadedHistorySearchDirectionAndAccountDetailsWorkWithoutExtraBankCalls`: fake-bank account reveal, search and incoming/outgoing filters. `ShowcaseExtraTest.csvExport`: actual Android Sharesheet for a fictional offline CSV, then return without choosing a receiving app. No external-send completion claim. |
| `statements` | `StatementsScreenTest.listDoesNotDownloadUntilSelectedAndViewerPagesAndSharesOriginalPdf`: synthetic PDF, periods, pages, zoom and explicit sharing; the intent is intercepted. `StatementSavingScreenTest.bulkSelectionDoesNotDownloadUntilFolderChosenAndKeepsExactBytesAndNames`: native period selection and saving, with fictional folder callback and fake file destination preserving synthetic bytes/names. No filmed real folder provider or actual bank PDF claim. |
| `transfers` | `BankingFlowTest.transferRequiresCorrectAuthorizationAndPersistsOnceAcrossActivityRestart` and `ShowcaseExtraTest.savedBeneficiaryTransfers`: offline own/same-bank/other-bank cases with local DEMO code 123456 and fictional receipts. `AutomaticOperationCodeTest.transferRetainsExplicitReviewThenFillsSmsAndWaitsForVerify`: fake-bank review, money confirmation, SMS fill, reading hold and explicit Verify. `LiveScreenTest.beneficiaryPreloadWaitsOnlyWhenPickerOpensAndSearchSelectsExactRecipient` is a separate read/search/selection case, not itself a submitted transfer. |
| `payments` | `BankingFlowTest.servicePaymentReviewDoesNotDebitUntilConfirmed`: offline review and DEMO code 123456, not SMS. `AutomaticOperationCodeTest.paymentRetainsExplicitReviewThenFillsSmsAndWaitsForVerify`: fake-bank review, separate money confirmation, SMS code fill and explicit Verify. No real payment or filmed credit-card payment is claimed. |
| `beneficiaries` | `LiveScreenTest.scannedOtherBankRecipientPrefillsBeneficiaryFormWithoutValidatingOrSavingAutomatically`: pasted fictional code and recipient review, no automatic validation/save. `AutomaticOperationCodeTest.beneficiaryDeletionRetainsReviewAndExplicitSmsVerification`: reviewed fake-bank deletion with separate confirmation, SMS fill and explicit Verify. `ShowcaseExtraTest.saveFictionalBeneficiary`: separate local offline save. |
| `cards` | Only `LiveCardsScreenTest.cardServicesExplainUnavailabilityWithoutAdministrationRequests`: read-only detail, reveal/copy of bank-provided fixture identifier, informational services and return. It asserts no administration request. Earlier usage-control, loss/theft and travel scenarios are no longer selected or advertised. Full-number copying is conditional on explicit bank fields. Only the last four digits are displayed, even after opening details or copying. |
| `token` | `NativeTokenScreenTest.contractConsentAndBankProofPrecedeCodeDisplayAndUnlinkNeedsConfirmation`: fake contract/store, consent, simulated approval, generated token and separate unlink confirmation. `nativeTokenSmsAutofillStillRequiresVerify`: separate enrollment challenge with explicit Verify; it does not itself establish completed enrollment. Generated Token BSC codes are not SMS. |
| `qr` | `RecipientShareScreenTest.savePreservesSelectedRequestAndCancelAllowsRetry`: test-picker cancellation/retry and fictional PNG save. `RecipientScanScreenTest.paymentRequestShowsAmountAndPurposeBeforeExplicitRecipientReview`: injected scanner result. `RecipientShareScreenTest.printOpensAndroidPrintPreview`: actual Android print preview. No camera capture, physical printout or payment authorization claim. |
| `settings` | `ShowcaseSmsSettingsTest.deliveryPreferenceReturnsToSms`: actual assistance off/on switch, optional one-message guidance and separate delivery preferences, restoring enabled assistance and SMS. `ShowcaseExtraTest.settingsProfileHelpAndLogout`: offline profile/security/help/logout. `LiveScreenTest.moneyReconciliationNeedsLoadedHistoryAndFreshCheckedConfirmation`: fake-bank history and a fresh acknowledgement; no repeated or cancelled operation. |

## Scene-key context

A cue belongs to its recorded stage. Do not use a post-fill or post-consent cue
before the field/result exists. First-use assistance selection is distinct from
approval of a particular SMS. No cue certifies a completed real-bank operation.

| Key | Recorded stage and interpretation |
| --- | --- |
| `opening` | Native UI established: fictional data, simulated bank responses and no personal banking session. Works for offline and fake-bank scenes. |
| `navigation` | New screen, title and available actions; allow orientation before continuing. |
| `read` | Reading hold on actual information/settings/currency/PDF/language state. |
| `review` | Pre-action or newly opened details. Opening the screen is not authorization; do not assume every review has money fields. |
| `consent` | Terms/privacy/token-contract text or acceptance decision. Merely opening a document does not accept it. |
| `confirm` | Separate confirmation stage; fake/local transports never reach the real bank. It does not claim the confirmation has already been pressed. |
| `verify` | Review and explicit continuation. Keyboard autofill does not submit. SMS-only login's approved-message exception is a separate flow; do not use this cue to hide that exception. |
| `receipt` | Actual native result or acknowledgement, not necessarily success. Fictional result is no proof of real completion. |
| `sms-wait` | Empty field while a fictional message is expected. Optional assistance requires one-message approval, never inbox access. |
| `sms-filled` | Synthetic keyboard/system autofill has filled a code. Review, then explicit Verify. Use `sms-login` for the distinct approved-message auto-verifying login result. |
| `settings-sms` | SMS delivery preference selected when bank-offered, distinct from the actual assistance switch. Not a universal Android autofill switch. |
| `settings-ask` | Ask delivery preference selected temporarily. Bank-offered alternatives are chosen each time; this is not the assistance on/off switch. |
| `settings-email` | Email delivery preference selected temporarily, then SMS restored. No email inbox/autofill claim. |
| `uncertain` | History/reconciliation hold. A real case requires actual bank status/history checking; acknowledgement neither repeats nor cancels the old operation. |
| `token` | Fake token proof/generated-code/unlink stage. Generated token codes are not SMS; no claim of real enrollment. |
| `configuration` | Optional Android one-message consent versus inbox access; keyboard autofill remains device-dependent and waits Verify. The assistance switch is separate from delivery chips. |
| `paste` | One paste of a long fictional recipient payload; decoded review remains necessary. Pasting neither saves nor sends money. |
| `demo-code` | Offline authorization in `BankingFlowTest`/`ShowcaseExtraTest`. Manually entered 123456 is a local test code, not SMS. Banking operations still require Verify; consent-based SMS-only login is a separate exception. Never use for bank SMS or generated token codes. |
| `sms-consent` | Optional first-use assistance choice or explanation of per-message Android approval. General wording avoids falsely claiming a particular SMS dialog is currently visible. Approval grants one message, not inbox access; manual fallback remains available. |
| `sms-login` | Separate synthetic approved-message result for the current SMS-only login, which auto-verifies. Combined questions and operations retain Verify. No real-bank success or filmed personal consent result is claimed. |
| `settings-enabled` | Assistance is actually on, including after restoration. Android approval remains per message, and only SMS-only login has automatic verification after approval. |
| `settings-disabled` | Assistance is actually off in the one configuration scene; it is restored on before leaving. Keyboard/manual entry remain available. |
| `cards-readonly` | Bank-supplied card data and informational services only. No card changes; only the last four digits are visible, and a full number is available only through explicit copying when supplied. Never overlay old operational card footage with this cue as a substitute for replacing that footage. |

## Timing and overview

The overview remains 104 seconds: thirteen eight-second excerpts in chapter order.

| Index | Start–end seconds | Chapter |
| --- | --- | --- |
| 0 | 0–8 | first-use |
| 1 | 8–16 | login |
| 2 | 16–24 | verification |
| 3 | 24–32 | accounts |
| 4 | 32–40 | history |
| 5 | 40–48 | statements |
| 6 | 48–56 | transfers |
| 7 | 56–64 | payments |
| 8 | 64–72 | beneficiaries |
| 9 | 72–80 | cards |
| 10 | 80–88 | token |
| 11 | 88–96 | qr |
| 12 | 96–104 | settings |

Use these boundaries only if the assembled order/duration matches. The cards
excerpt must use the new read-only/information scene. Prefer already readable
reviews/results; avoid cuts through tap rings or incomplete confirmations.

The machine policy gives 5 seconds of opening context, 1.5 seconds before ordinary
actions, at least 3.5 seconds after navigation, 8 seconds for reviews/results and
specified 10-second consent/uncertain holds. Each scene retains 6 seconds on its
actual native result before closure. The keyboard-autofill path retains the
empty-code hold, synthetic fill and filled-code reading hold before Verify.
The separate approved-message login must not invent an extra Verify tap.
Recorded event boundaries, not evenly spaced summaries, control scene cues.

## Integration and verification limits

The four-cue chapter arrays remain summaries. If final WebVTT uses recorded
scene cues, generate its transcript from the actual final timed cue text in
order and in the chosen language. Broader chapter prose is not a verbatim
transcript. Only basic-demo features receive a demo badge; mixed or advanced
fake-bank recordings retain simulation scope.

Checks cover JSON decoding, all seven locale catalogues, thirteen chapter IDs,
four cues per chapter, thirteen overview cues, twenty-three aligned scene keys,
nonempty text and the 160-character ceiling. There are 616 localized cues in the
two caption catalogues: 455 summaries and 161 scene cues. Relevant content bodies
retain the existing schema and all five installation steps.

Source review is not proof that the new tests or final retakes passed. Timing,
actual final footage, subtitle wrapping, native-speaker review and publication
remain the media owner's checks. This task changes only caption/content assets
and this context file; it does not build, render, record or publish media.

## Per-scenario default introductions

`scenario-captions.json` adds a scene-specific default caption to prevent the
four broad chapter summaries from describing a different case on screen. Its
schema is:

```json
{
  "revision": 3,
  "languages": {
    "es": {
      "first-use-01": "One introductory caption for this scripted case"
    }
  }
}
```

All seven language maps have exactly the same 34 keys and order, derived from
`video-scripts.json` revision 3: **chapter ID plus a two-digit scene index**.
Index the chapter's `scenes` list, not its `beats` list. Some chapters have
several beats inside one scene; for example `accounts` has only `accounts-01`.
There are 238 localized introductory captions. Each is nonempty plain text of
at most 160 Unicode characters, without placeholders or implementation names.

Use the current scene's introduction during its generic reading/navigation
holds. Specific event-timed text from `scene-captions.json` overrides the default
only at that actual stage. Restore the same scene introduction afterwards and
switch to the next introduction at the recorded scene boundary. Do not divide
chapter-summary cues globally by chapter duration: that can incorrectly describe
consent-based automatic login during the keyboard-autofill case. Final subtitle
transcripts must still follow the actual exported timed text, in order.

`login-03` describes Android/keyboard SMS-code autofill with explicit Verify.
`login-04` separately describes a simulated approved-message result and automatic
verification of SMS-only login. Neither claims successful real-bank access.
`verification-01` retains explicit Verify for combined questions. The local demo
transfer/payment cases identify 123456 as a non-SMS test code. Recipient search
and local saving remain distinct from bank operations.

`cards-01` reflects the current fixture's supplied fictional holder, identifier
and full test card number, without including their values in captions. Those
fields come from the simulated bank; there is no reconstructed number. The
case includes informational, unavailable card services and no card changes.
It does not reuse the earlier operational card scenarios. The three settings
introductions separately cover assistance off/on plus delivery preferences,
offline-demo settings, and uncertain-outcome reconciliation.

Validation compares every locale's exact key set and order against the current
script, checks revision 3, seven languages, 34 keys per language and the
160-character limit. Introductions describe what a case covers; they do not
assert its final success before it occurs. Timing and final visual review remain
the media owner's work. This addition changes only the new scenario catalogue
and this appended schema/context note.

The 1.12.1 card retake keeps full numbers out of visible and accessibility text.
The cards-readonly cue documents last-four masking in all seven languages; explicit
copying remains separate. The overview uses the retaken masked card footage.

## Revision 4: feature-first narrative

`ux-copy.json` supplies the main tour cues in the authored order: SMS login,
financial SMS, first-use language, registration continuation, accounts, history,
statements, payments, recipients, masked cards, token, QR and settings. The first
14-second excerpt shows the approved automatic login transition; the next
18 seconds preserve money-code autofill and explicit Verify. All remaining
excerpts show a useful actual interaction, with no repeated login setup.

Financial chapter scenes use `ShowcaseMoneyUxTest` and fake transports, never the
offline demo test-code path. Every required SMS shows empty/wait, callback fill,
readable filled state and continuation. A synthetic bank-response delay makes
automatic login legible; this is not a production delay or a fabricated Android
dialog. Overview cuts resolve against real event anchors in overview-cuts.json.
Gallery/spotlight SMS images are taken from actual recorded hold events.

Scenario cue positions follow revision-4 scene selection: login-01 approved SMS,
login-02 saved biometrics; verification-01 combined question/SMS, verification-02
registration re-entry; transfers-01/02/03 own/same/other-bank SMS flows and
transfers-04 recipient search; payments-01 service SMS and payments-02 card SMS.
Other chapter IDs retain their existing meanings. Scripts are written before
recording; a fast fixture rehearsal cannot become publishable media.

## Concise narrated presentation

Final narration, subtitles and transcripts now use `narration-actions.json`.
Its `phrases` entries keep context adjacent to all seven translations. Each
`timelines` array follows the actual scenario or overview-excerpt order. A cue
selects a recorded event type and ordinal, optionally narrowed by hold cue;
negative ordinals count from the end. Overview `group-start` anchors are excerpt
boundaries. These instructions describe a user action at its own recorded stage.

Generic opening/navigation/read descriptions and repeated simulation disclaimers
are not spoken. Page disclosures retain simulation scope. Successful synthetic
file saves and recipient removal can be named after their result; a money receipt
is described as a receipt because the UI asks the user to check final history.
The SMS code is never described as typed when the source records autofill.
SMS-only approved-message login has no invented Verify tap; combined questions,
financial operations and token enrollment retain their recorded Verify action.

Regenerate with `scripts/narrate-media.py` from its pinned original capture source,
then build the HTML. The same scheduled speech cues produce all localized VTT
tracks, verbatim ordered transcripts and the embedded self-hosted narration.
Every authored cue is mandatory and bounded by its next task cue/scene. Missing
anchors or speech that does not fit fail generation. Unit tests validate all
recorded anchors and preserve speech windows through idle trimming. Final media
regeneration, native-language wording review and visual alignment are separate
required verification steps; source tests alone do not prove them.


`editorial-cuts.json` documents repeated QA attempts excluded from presentation.
Action ordinals always resolve against the untouched source before exclusions;
no narration may anchor inside an omitted interval. Every original event remains
archived and excluded events carry their exact source index and reason. Token
SMS activation skips the contract steps already shown in its first case. The
settings chapter keeps one complete acknowledgement flow and its recorded-review
result. QR Save remains an action instruction, without an invented save outcome.
