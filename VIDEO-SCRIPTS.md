# Feature-first native videos — revision 4

Write and review this script before recording. The main tour demonstrates fewer
steps and clearer decisions through the actual UI. It does not claim unsupported
original-app feature absences or use competitive slogans. Lead with SMS arrival,
automatic fill and continuation; do not substitute a static filled field.

No repeated login: only authentication and device-setup chapters may contain it.
Every other scene starts in an authenticated native feature; fixture sign-in is
quiet and excluded from published footage and screenshot selection. No demo test-
code typing in the financial feature videos. All required bank SMS steps show
arrival/approval, automatic fill and the actual continuation. Financial operations,
combined questions and enrollment retain their real explicit Verify step.

Overview: approximately 109 seconds, silent at native speed. First 14 seconds show
approved SMS-only login; next 18 show financial SMS fill, Verify and receipt. Then
11 seven-second native examples: language choice, registration continuation,
balance privacy/currencies, history search, PDF pages, service payment result,
recipient review, masked card copying, token, QR request and SMS settings. Use the
machine script's exact scene/event anchors. Do not crop an input ring halfway or
choose login frames for unrelated flows. A short contextual caption accompanies
each real interaction. Synthetic SMS/biometric/bank callbacks are identified;
never draw a fake Android approval prompt or fake a bank result.

The demo and advanced simulated interface are explained once near the main video
and in edition details. Scripts/captions should lead with user benefits, keeping
meaningful approval, money-review, unsupported-card-service and uncertain-outcome
boundaries accurate. Full numbers stay masked to their last four digits.

## Pacing and capture rules

5-second opening; 1.5 seconds before ordinary actions; 3.5 seconds after
navigation. SMS fields remain empty for 3 seconds, then filled for 5.5 seconds.
Reviews/receipts hold 8 seconds; important consent and uncertain-result states
hold 10–12 seconds. No speedup. All code-entry sequences show real callbacks,
not a typed code or a static screenshot. A 1.8-second fake bank response delay
makes the SMS-only automatic continuation legible without changing production.

## first-use

Understand the independent-app notice before accepting anything.

Entry: Authentication/setup only.

### first-use-01 — Privacy before consent

Open the privacy policy; hold the opening explanation for 10 seconds. Return without accepting.

### first-use-02 — Terms are a separate choice

Open terms; hold for 10 seconds. Return; pause 5 seconds with Continue disabled. Check agreement, pause 5 seconds, then Continue.

### first-use-03 — Language selection

Open the language list, hold 6 seconds, choose Spanish, and hold the selected setting for 5 seconds.

Fixtures:

- `FirstUseNoticeTest.privacyIsAvailableBeforeTermsAndNeverAcceptsThem`.
- `FirstUseNoticeTest.bankingStaysBlockedUntilTermsOpenedAndExplicitlyAcceptedThenAcceptancePersists`.
- `ShowcaseExtraTest.languageSelection`.

## login

Distinguish local remembered access, simulated biometrics, and bank approval.

Entry: Authentication/setup only.

### login-01 — SMS arrives; access continues

Begin on the pending SMS field after credentials were supplied off-camera. Hold empty field 3 seconds; explain the synthetic one-message approval without fabricating an Android dialog. Deliver approved fake SMS; capture automatic verification and the resulting accounts. No keyboard typing or extra Verify tap.

### login-02 — Remembered biometric access

Show saved access once; approve the clearly simulated biometric callback and hold the resulting native accounts. Do not replay credentials or pretend bank approval was bypassed.

Fixtures:

- `LiveScreenTest.approvedSmsMessageCompletesOnlyTheCurrentSmsLoginWithoutAnExtraVerifyTap` — SMS autofill required.
- `LiveScreenTest.savedLoginWaitsForBiometricsThenSubmitsAutomatically`.

## verification

Show the independent security steps and who controls each outcome.

Entry: Authentication/setup only.

### verification-01 — Question plus SMS

Enter only the fictional security answer. Leave SMS code empty for 3 seconds; autofill it; hold 5 seconds before Verify. Assert no submission happened during autofill.

### verification-02 — Registration return stays inside the app

Show device registration requirement, pause 10 seconds on consent. Request registration explicitly. Explain required fresh login, pause 6 seconds on biometric re-entry fixture. Approve biometric callback and hold accounts 8 seconds. No password is retained for silent replay.

Fixtures:

- `LiveScreenTest.systemSmsAutofillKeepsCombinedQuestionAndWaitsForVerify` — SMS autofill required.
- `LiveScreenTest.registrationResumesThroughBiometricsWithoutExitingOrReusingPassword`.

## accounts

Read balances and currency before taking action.

Entry: Already in the feature; login excluded from exported footage.

### accounts-01 — Orient

Start at fictional account overview, not another login. Hold for 5 seconds.

### accounts-02 — Privacy

Hide balances, hold 5 seconds; reveal, hold 5 seconds.

### accounts-03 — Separate currencies

Choose USD and hold 6 seconds. Return to DOP and hold 6 seconds.

### accounts-04 — Scroll and details

Show real swipe direction; pause after each scroll. Open account details and hold account identity/currency/actions for 8 seconds.

Fixtures:

- `ShowcaseExtraTest.accountsAndPrivacy`.

## history

Understand visible records and what the CSV contains.

Entry: Already in the feature; login excluded from exported footage.

### history-01 — Read/search/filter

Start already signed into the fake bank. Reveal account identity, search and filter with 4-second pauses after changed results.

### history-02 — Export

Open the demo CSV Sharesheet, hold 8 seconds, then return. Do not claim an external recipient received it.

Fixtures:

- `LiveScreenTest.loadedHistorySearchDirectionAndAccountDetailsWorkWithoutExtraBankCalls`.
- `ShowcaseExtraTest.csvExport`.

## statements

Separate viewing, sharing, and persistent saving.

Entry: Already in the feature; login excluded from exported footage.

### statements-01 — Catalogue

Hold available/unavailable periods for 6 seconds before opening.

### statements-02 — PDF

Hold the synthetic PDF for 8 seconds. Pause 5 seconds after page/zoom actions. Explain sharing is explicit.

### statements-03 — Save selection

Select available periods and hold the selection for 6 seconds. Press Save selected. Explain the folder callback is simulated; pause 5 seconds before it and 8 seconds after successful synthetic writes.

Fixtures:

- `StatementsScreenTest.listDoesNotDownloadUntilSelectedAndViewerPagesAndSharesOriginalPdf`.
- `StatementSavingScreenTest.bulkSelectionDoesNotDownloadUntilFolderChosenAndKeepsExactBytesAndNames`.

## transfers

Make the review, money confirmation and SMS verification readable.

Entry: Already in the feature; login excluded from exported footage.

### transfers-01 — Own accounts, SMS assisted

Start in the authenticated native transfer form, with no login footage. Select exact payer/payee, enter amount and show readable quote/fees and a separate money confirmation. Show the empty SMS field, let it fill automatically, pause to read, then explicitly Verify and hold the fake-bank receipt. No manual bank code or offline test-code detour.

### transfers-02 — Same bank, SMS assisted

Start in the authenticated native transfer form, with no login footage. Select exact payer/payee, enter amount and show readable quote/fees and a separate money confirmation. Show the empty SMS field, let it fill automatically, pause to read, then explicitly Verify and hold the fake-bank receipt. No manual bank code or offline test-code detour.

### transfers-03 — Other bank, SMS assisted

Start in the authenticated native transfer form, with no login footage. Select exact payer/payee, enter amount and show readable quote/fees and a separate money confirmation. Show the empty SMS field, let it fill automatically, pause to read, then explicitly Verify and hold the fake-bank receipt. No manual bank code or offline test-code detour.

### transfers-04 — Search the exact recipient

Begin at authenticated accounts. Open the destination picker and search by recipient name or digits. Pause on the exact matching recipient; no login and no transfer submission in this search-only example.

Fixtures:

- `ShowcaseMoneyUxTest.ownAccountsSms` — SMS autofill required.
- `ShowcaseMoneyUxTest.sameBankSms` — SMS autofill required.
- `ShowcaseMoneyUxTest.otherBankSms` — SMS autofill required.
- `LiveScreenTest.beneficiaryPreloadWaitsOnlyWhenPickerOpensAndSearchSelectsExactRecipient`.

## payments

Review the service and amount before authorization.

Entry: Already in the feature; login excluded from exported footage.

### payments-01 — Service payment with autofill

Begin in the payment form, without login. Read the bank-supplied service/card balance and select the amount. Hold review and separate money confirmation, then show empty SMS, automatic fill, readable filled field, explicit Verify and the fictional receipt. Never type a bank or demo code.

### payments-02 — Credit-card payment with autofill

Begin in the payment form, without login. Read the bank-supplied service/card balance and select the amount. Hold review and separate money confirmation, then show empty SMS, automatic fill, readable filled field, explicit Verify and the fictional receipt. Never type a bank or demo code.

Fixtures:

- `ShowcaseMoneyUxTest.servicePaymentSms` — SMS autofill required.
- `ShowcaseMoneyUxTest.creditCardPaymentSms` — SMS autofill required.

## beneficiaries

A scanned/pasted recipient is not automatically validated or saved.

Entry: Already in the feature; login excluded from exported footage.

### beneficiaries-01 — Code review

Paste the long fictional recipient payload as one paste, not dozens of seconds of character typing. Hold the decoded recipient/currency for 8 seconds before continuation.

### beneficiaries-02 — Deletion with SMS

Read deletion review for 8 seconds; confirm separately. Use SMS autofill only, hold before Verify, then explain the fake bank response for 8 seconds.

### beneficiaries-03 — Local save

Create a clearly fictional other-bank recipient locally, then hold the saved result for 8 seconds. This is a separate offline scene.

Fixtures:

- `LiveScreenTest.scannedOtherBankRecipientPrefillsBeneficiaryFormWithoutValidatingOrSavingAutomatically`.
- `AutomaticOperationCodeTest.beneficiaryDeletionRetainsReviewAndExplicitSmsVerification` — SMS autofill required.
- `ShowcaseExtraTest.saveFictionalBeneficiary`.

## cards

Useful masked card details and explicit copy, without unsupported service requests.

Entry: Already in the feature; login excluded from exported footage.

### cards-01 — Read-only details and unavailable services

Begin at authenticated cards, not login. Open details; show supplied holder and identifier. Keep the card number masked to its last four digits before, during and after explicit copying. Hold the unimplemented-services information for 12 seconds, then return to details. No card-write request.

Fixtures:

- `LiveCardsScreenTest.cardServicesExplainUnavailabilityWithoutAdministrationRequests`.

## token

Consent and bank approval precede any active code.

Entry: Already in the feature; login excluded from exported footage.

### token-01 — Contract and proof

Hold synthetic contract 10 seconds. Hold consent explanation 8 seconds before enrollment. Hold pending proof 10 seconds; a fixture approval is explicitly simulated.

### token-02 — Active and unlink

Hold generated fictitious code/status 8 seconds. Hold unlink confirmation 8 seconds before accepting, and explain result for 8 seconds.

### token-03 — SMS enrollment step

A separate fake enrollment challenge uses SMS autofill, never typed SMS. Show empty/filled/Verify as in other banking scenes. Do not claim this scenario itself completed enrollment. A generated Token BSC code remains a token, not an SMS.

Fixtures:

- `NativeTokenScreenTest.contractConsentAndBankProofPrecedeCodeDisplayAndUnlinkNeedsConfirmation`.
- `NativeTokenScreenTest.nativeTokenSmsAutofillStillRequiresVerify` — SMS autofill required.

## qr

Review the request before sharing or acting on it.

Entry: Already in the feature; login excluded from exported footage.

### qr-01 — Create and save

Hold account versus payment-request modes; type short fictional purpose/amount readably. Hold completed QR card/details 8 seconds. Demonstrate save cancellation and retry without pretending a bank payment occurred.

### qr-02 — Scanner review

Hold injected decoded amount/purpose/currency 8 seconds before explicit recipient review. No real camera capture is claimed.

### qr-03 — Print

Hold Android print preview 8 seconds, return without claiming physical printing.

Fixtures:

- `RecipientShareScreenTest.savePreservesSelectedRequestAndCancelAllowsRetry`.
- `RecipientScanScreenTest.paymentRequestShowsAmountAndPurposeBeforeExplicitRecipientReview`.
- `RecipientShareScreenTest.printOpensAndroidPrintPreview`.

## settings

Show configuration once, restore SMS, and preserve uncertain outcomes.

Entry: Already in the feature; login excluded from exported footage.

### settings-01 — Delivery configuration

Read one-message SMS consent guidance for 10 seconds. Switch SMS assistance off and hold 6 seconds; switch back on and hold 8 seconds. Then demonstrate Ask and Email delivery preferences with 6-second pauses and restore SMS delivery. All other chapters keep assistance enabled, except the initial pre-choice onboarding scene.

### settings-02 — Demo settings

Show profile, security, help and logout with 6-second explanation holds.

### settings-03 — Uncertain operation

Hold the blocked state/history for 10 seconds. Read reconciliation acknowledgement for 10 seconds before checking it. Confirm explicitly and hold result 8 seconds. Never imply retrying, cancelling or reversing the old operation.

Fixtures:

- `ShowcaseSmsSettingsTest.deliveryPreferenceReturnsToSms`.
- `ShowcaseExtraTest.settingsProfileHelpAndLogout`.
- `LiveScreenTest.moneyReconciliationNeedsLoadedHistoryAndFreshCheckedConfirmation`.
