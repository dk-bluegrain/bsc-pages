# Caption copy and recording context

`captions.json` has this schema:

```text
languages → es/en/de/fr/ru/uk/pt → chapter ID or overview → string array
```

Each chapter has four concise, semantically aligned cues in every language.
`overview` has exactly thirteen cues, in the same order as the chapter list.
All cues are UTF-8 plain text and require escaping if inserted in HTML. Strings
contain no formatted arguments, credentials, private identities or personal
banking data. Spanish is the source of meaning. Language conventions follow
`TRANSLATIONS.md` (German Sie, French vous, polite Russian/Ukrainian, Brazilian
Portuguese). Catalogue names and chapter IDs follow `content.json`.

These are silent instructional/overview captions. They describe what the
recorded scenario covers and its boundaries; they are not narration of a click
at a particular instant. They deliberately do not say “now”, “here we click”,
or claim that an unrecorded bank request has succeeded. No wording asserts
current live-bank compatibility or bank authorization.

## Context shared by all four-cue chapter arrays

1. **Cue 1:** native UI demonstration/simulation and fictional-data scope.
   `accounts` specifically identifies the offline demo; `history`, `transfers`,
   `payments` and `settings` identify mixed offline-demo and advanced simulated
   content.
   `login` explicitly clarifies that biometric approval is simulated rather than
   a filmed physical biometric interaction. First-use uses notice/privacy
   screens and a Spanish-language selection without claiming a personal bank
   session.
2. **Cue 2:** first recorded feature or relevant prerequisite, described as an
   overview rather than an event tied to the current tap.
3. **Cue 3:** second recorded scenario/feature or explicit confirmation control.
   This can occur in another source clip; it must not imply one continuous
   session across test resets.
4. **Cue 4:** limitation, basic-demo distinction, or unresolved bank permission
   and compatibility. These notes remain necessary on directly linked videos.

Do not reuse a chapter array as an assertion that its four sentences are
complete accessibility descriptions of everything shown. Screens contain
additional Spanish text; all seven subtitle languages describe the same
selected flow at a readable summary level.

## Scenario-to-copy review

The catalogue was reviewed against
`/extra/dkropachev/bsc-distribution/scripts/capture-showcase.py`, the selected
instrumentation methods in that checkout and the current website renderer
`scripts/build.py`.

| Chapter ID | Selected recorded coverage and caption boundary |
| --- | --- |
| `first-use` | `FirstUseNoticeTest.privacyIsAvailableBeforeTermsAndNeverAcceptsThem` and `bankingStaysBlockedUntilTermsOpenedAndExplicitlyAcceptedThenAcceptancePersists`: privacy access, independent-app notice, terms opening and explicit acceptance. Supplemental `ShowcaseExtraTest.languageSelection` opens the native language picker and selects Spanish. No claim of a filmed switch through all seven languages. |
| `login` | `LiveScreenTest.rememberingCredentialsDefaultsOnAndRequiresBiometricSaveBeforeLogin` and `savedLoginWaitsForBiometricsThenSubmitsAutomatically`: fake saved-login callbacks, fake credentials and fake bank. No claim that a real system fingerprint dialog is shown or real bank approval occurs. |
| `verification` | `combinedQuestionAndTokenRemainSeparateBeforeBankAuthentication`, `untrustedDeviceCannotFetchAccountsOrEnrollSilently`, `LoginPrerequisitesScreenTest.requiredPasswordIsConfirmedAndReturnsToLoginWithoutReadingAccounts`: separate question/token, blocked unapproved device, confirmed required password change. No filmed identity-browser handoff or successful device enrollment claim. |
| `accounts` | `ShowcaseExtraTest.accountsAndPrivacy`: basic demo balance hide/reveal, USD/DOP switching, actual upward/downward swipes with native direction arrows, and account detail. No live-bank read. |
| `history` | `LiveScreenTest.loadedHistorySearchDirectionAndAccountDetailsWorkWithoutExtraBankCalls`: simulated bank history, reveal account number, search, incoming/outgoing filters. Supplemental `ShowcaseExtraTest.csvExport` opens the actual Android Sharesheet with a fictional offline-demo CSV and returns without selecting a receiving app. No external-send completion claim. |
| `statements` | `StatementsScreenTest.listDoesNotDownloadUntilSelectedAndViewerPagesAndSharesOriginalPdf`: synthetic PDF, available/unavailable periods, open, page navigation, zoom, explicit share action. The sharing intent is intercepted; receiving-app completion is not shown. Supplemental `StatementSavingScreenTest.bulkSelectionDoesNotDownloadUntilFolderChosenAndKeepsExactBytesAndNames` selects offered periods and initiates Save selected; a fake picker callback supplies a fictional folder and the fake file destination preserves the exact synthetic bytes/names. No real folder-picker screen or live-bank PDF claim. |
| `transfers` | `BankingFlowTest.transferRequiresCorrectAuthorizationAndPersistsOnceAcrossActivityRestart`: offline own-account demo review, wrong/correct test code, fictional receipt and persistence. `LiveScreenTest.beneficiaryPreloadWaitsOnlyWhenPickerOpensAndSearchSelectsExactRecipient`: advanced simulated recipient picker/search, no transfer submitted. Supplemental `ShowcaseExtraTest.savedBeneficiaryTransfers` completes local same-bank and other-bank saved-recipient transfers with test code and fictional receipts. Bank-category transfers shown end to end are offline simulations, not real submissions. |
| `payments` | `BankingFlowTest.servicePaymentReviewDoesNotDebitUntilConfirmed`: local demo review/test code. `AutomaticOperationCodeTest.paymentRetainsExplicitReviewThenFillsSmsAndWaitsForVerify`: advanced fake-bank review, SMS autofill and explicit verification. No claim of a filmed credit-card payment. |
| `beneficiaries` | `LiveScreenTest.scannedOtherBankRecipientPrefillsBeneficiaryFormWithoutValidatingOrSavingAutomatically`: manual code input and prefill without writing. `bankBeneficiaryDeletionRequiresReviewAndFinalConfirmationThenReloadsList`: reviewed simulated bank deletion. Supplemental `ShowcaseExtraTest.saveFictionalBeneficiary` saves a fictional other-bank recipient locally in the basic demo. No successful live-bank validation/save is claimed. |
| `cards` | `LiveCardsScreenTest.nativeUsageControlRequiresReviewThenExplicitChallengeAndOneLoadingModal`, `CardOperationsScreenTest.lossAndTheftRequireSeparateReviewBeforeSubmitting`, `travelCollectsDestinationsBeforeReviewAndSendsOnlyOnConfirmation`: fake cards, usage challenge and distinct loss/theft/travel scenarios. No real card control or universal availability claim. |
| `token` | `NativeTokenScreenTest.contractConsentAndBankProofPrecedeCodeDisplayAndUnlinkNeedsConfirmation`: fake bank/store, contract/consent setup, approval checks, code and explicit unlink. No real token seed, owner identification or active live-bank token claim. |
| `qr` | `RecipientShareScreenTest.savePreservesSelectedRequestAndCancelAllowsRetry`: cancel/retry and chosen-document save with test picker; `RecipientScanScreenTest.paymentRequestShowsAmountAndPurposeBeforeExplicitRecipientReview`: injected scanner response; `RecipientShareScreenTest.printOpensAndroidPrintPreview`: actual Android print preview. No claim of physical camera capture, printer output or payment authorization. |
| `settings` | `ShowcaseExtraTest.settingsProfileHelpAndLogout`: demo profile/security/help/logout. `LiveScreenTest.moneyReconciliationNeedsLoadedHistoryAndFreshCheckedConfirmation`: fake-bank history then fresh acknowledgement, no repeated operation. No claim of a filmed profile edit or language change. |

## Overview timing contract

The planned overview is 104 seconds: thirteen consecutive eight-second clips.
Cue index maps directly to the chapter ID at the same index:

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

Generate overview WebVTT from those boundaries only if the assembled footage
still follows that exact order and duration. Chapter cue arrays do not carry
invented timestamps. The media owner must place them against the final chapter
edit; use section boundaries where available. A general caption may cover a
scenario's setup as well as its core sequence, but it must remain readable and
must not claim a different scene is visible.

## Renderer integration and verification limits

The current renderer reads `captions.json` for transcript disclosures: four
ordered cue strings per chapter and thirteen for overview. Broader feature
introductions from `content.json` remain separate. The basic-demo badge applies
to `accounts`; other chapter videos receive the simulation badge, including
mixed demo/advanced chapters. Renderer changes are outside this asset task's
ownership.

Supplemental cue text was checked against the additional selected test methods
and the revised `capture-showcase.py` scenario map. The subtitle catalogue does
not certify that a final recording passed: final synchronized retakes and the
assembled footage remain subject to the media owner's acceptance checks.

Verified JSON decoding, exact locale and media-key parity, four cues per chapter,
exactly thirteen overview cues, nonempty plain-text cues, matching counts across
languages and maximum cue length of 125 Unicode characters. Timing, final footage
coverage, line wrapping, native-speaker review and final WebVTT rendering still
require media QA. No code outside these caption assets was changed for this
follow-up.
