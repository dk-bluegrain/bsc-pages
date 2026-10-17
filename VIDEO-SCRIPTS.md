# Video scripts — revision 3

These scripts are written before the retake. Each numbered beat states what the viewer should understand and where the operator must wait. The executable timing policy is `scripts/capture/video-scripts.json`.

## Shared recording rules

- Spanish native UI, fictional identities/documents and fake transports only.
- Opening context: 5 s. Before ordinary actions: 1.5 s. After navigation: at least 3.5 s.
- Financial/recipient reviews and receipts: 8 s. Consent, loss/theft warnings and uncertain outcomes: 10 s where specified.
- SMS assistance is enabled, with one-message Android consent available, in every recording except initial pre-choice onboarding. Only the settings scene disables and restores it. SMS delivery is preset to SMS in every recording. Only the configuration scene changes it temporarily and restores SMS.
- SMS code fields remain empty for 3 s, receive only a synthetic Android autofill callback, then remain filled for 5.5 s before explicit Verify. Keyboard autofill never submits. One-message consent may auto-verify an SMS-only login, shown separately and explicitly as a synthetic result.
- Offline demo code 123456 and generated Token BSC codes are not SMS; do not relabel them.
- Skip repeated authentication setup outside login/verification. Paste long QR payloads once; type only short human-readable inputs.
- Every scene ends with a 6 s hold on its actual native result before the test activity closes.
- Caption timing follows recorded hold/scene events, with special cues during SMS arrival, filled-code review and configuration.

## first-use

Understand the independent-app notice before accepting anything.

Privacy before consent. Open the privacy policy; hold the opening explanation for 10 seconds. Return without accepting.

Terms are a separate choice. Open terms; hold for 10 seconds. Return; pause 5 seconds with Continue disabled. Check agreement, pause 5 seconds, then Continue. Show the optional SMS choice, enable it after its reading hold, and end on the login form backed by the capture-only non-network client. Do not record a missing-integration setup error as the normal completion.

Language selection. Open the language list, hold 6 seconds, choose Spanish, and hold the selected setting for 5 seconds.

Capture fixtures: `FirstUseNoticeTest.privacyIsAvailableBeforeTermsAndNeverAcceptsThem`, `FirstUseNoticeTest.bankingStaysBlockedUntilTermsOpenedAndExplicitlyAcceptedThenAcceptancePersists`, `ShowcaseExtraTest.languageSelection`.

## login

Distinguish local remembered access, simulated biometrics, and bank approval.

First remembered login. Show the remember checkbox and explain local biometric protection. Type fictional credentials slowly; hold 5 seconds before login. Pause 8 seconds on the resulting accounts.

Biometric unlock. Show the prefilled identity and simulated unlock for 6 seconds. Approve the fixture callback, then hold the resulting account list for 8 seconds.

SMS without typing a code. With remembered SMS delivery already selected, leave the empty code field visible for 3 seconds. Inject only the synthetic Android autofill callback. Hold the filled field for 5 seconds; no login replay is allowed yet. Tap Verify, then hold the result for 8 seconds.

Capture fixtures: `LiveScreenTest.rememberingCredentialsDefaultsOnAndRequiresBiometricSaveBeforeLogin`, `LiveScreenTest.savedLoginWaitsForBiometricsThenSubmitsAutomatically`, `LiveScreenTest.rememberedSmsChannelRequestsDeliveryThenWaitsForExplicitVerification`.

## verification

Show the independent security steps and who controls each outcome.

Question plus SMS. Enter only the fictional security answer. Leave SMS code empty for 3 seconds; autofill it; hold 5 seconds before Verify. Assert no submission happened during autofill.

Device approval. Show the unapproved-device screen for 10 seconds. Do not claim registration or account access.

Required setup. Show the password requirements; enter fictional values. Hold mismatch feedback for 5 seconds, then correct it. Hold review for 8 seconds; explicitly submit and explain the return to login for 8 seconds.

Capture fixtures: `LiveScreenTest.systemSmsAutofillKeepsCombinedQuestionAndWaitsForVerify`, `LiveScreenTest.untrustedDeviceCannotFetchAccountsOrEnrollSilently`, `LoginPrerequisitesScreenTest.requiredPasswordIsConfirmedAndReturnsToLoginWithoutReadingAccounts`.

## accounts

Read balances and currency before taking action.

Orient. Start at fictional account overview, not another login. Hold for 5 seconds.

Privacy. Hide balances, hold 5 seconds; reveal, hold 5 seconds.

Separate currencies. Choose USD and hold 6 seconds. Return to DOP and hold 6 seconds.

Scroll and details. Show real swipe direction; pause after each scroll. Open account details and hold account identity/currency/actions for 8 seconds.

Capture fixtures: `ShowcaseExtraTest.accountsAndPrivacy`.

## history

Understand visible records and what the CSV contains.

Read/search/filter. Start already signed into the fake bank. Reveal account identity, search and filter with 4-second pauses after changed results.

Export. Open the demo CSV Sharesheet, hold 8 seconds, then return. Do not claim an external recipient received it.

Capture fixtures: `LiveScreenTest.loadedHistorySearchDirectionAndAccountDetailsWorkWithoutExtraBankCalls`, `ShowcaseExtraTest.csvExport`.

## statements

Separate viewing, sharing, and persistent saving.

Catalogue. Hold available/unavailable periods for 6 seconds before opening.

PDF. Hold the synthetic PDF for 8 seconds. Pause 5 seconds after page/zoom actions. Explain sharing is explicit.

Save selection. Select available periods and hold the selection for 6 seconds. Press Save selected. Explain the folder callback is simulated; pause 5 seconds before it and 8 seconds after successful synthetic writes.

Capture fixtures: `StatementsScreenTest.listDoesNotDownloadUntilSelectedAndViewerPagesAndSharesOriginalPdf`, `StatementSavingScreenTest.bulkSelectionDoesNotDownloadUntilFolderChosenAndKeepsExactBytesAndNames`.

## transfers

Make the review, money confirmation and SMS verification readable.

Offline own-account example. Show source/destination, amount and currency. Hold review 8 seconds. Show a wrong DEMO code once, explain for 6 seconds; correct with DEMO code 123456, then hold the fictional receipt 8 seconds. Demo codes are not SMS.

Advanced bank/SMS example. Start in an authenticated fake transfer form. Select recipient/amount, hold quote review 8 seconds, then hold the real-money confirmation dialog for 8 seconds. After confirmation, show empty SMS field 3 seconds, autofill without typing, hold filled field 5 seconds. Tap Verify explicitly; hold the fake-bank receipt 8 seconds.

Recipient search. Show the pending/read/search/selection distinction; do not submit a bank transfer.

Saved-recipient demo. Show same-bank and other-bank offline examples as separate cases, each with an 8-second review/receipt. Local test authorization is explicitly distinct from SMS.

Capture fixtures: `BankingFlowTest.transferRequiresCorrectAuthorizationAndPersistsOnceAcrossActivityRestart`, `AutomaticOperationCodeTest.transferRetainsExplicitReviewThenFillsSmsAndWaitsForVerify`, `LiveScreenTest.beneficiaryPreloadWaitsOnlyWhenPickerOpensAndSearchSelectsExactRecipient`, `ShowcaseExtraTest.savedBeneficiaryTransfers`.

## payments

Review the service and amount before authorization.

Offline service. Hold bill/amount review 8 seconds and fictional receipt 8 seconds; the DEMO code remains a local test code.

Advanced SMS. Start in the fake-bank payment form. Read review and money confirmation for 8 seconds each. Empty SMS field 3 seconds, autofill callback, filled field 5 seconds, explicit Verify, fake receipt 8 seconds.

Capture fixtures: `BankingFlowTest.servicePaymentReviewDoesNotDebitUntilConfirmed`, `AutomaticOperationCodeTest.paymentRetainsExplicitReviewThenFillsSmsAndWaitsForVerify`.

## beneficiaries

A scanned/pasted recipient is not automatically validated or saved.

Code review. Paste the long fictional recipient payload as one paste, not dozens of seconds of character typing. Hold the decoded recipient/currency for 8 seconds before continuation.

Deletion with SMS. Read deletion review for 8 seconds; confirm separately. Use SMS autofill only, hold before Verify, then explain the fake bank response for 8 seconds.

Local save. Create a clearly fictional other-bank recipient locally, then hold the saved result for 8 seconds. This is a separate offline scene.

Capture fixtures: `LiveScreenTest.scannedOtherBankRecipientPrefillsBeneficiaryFormWithoutValidatingOrSavingAutomatically`, `AutomaticOperationCodeTest.beneficiaryDeletionRetainsReviewAndExplicitSmsVerification`, `ShowcaseExtraTest.saveFictionalBeneficiary`.

## cards

Understand the useful read-only fields and implementation boundary.

1. Open a card from the native fake-bank catalogue. Hold status, linked product and balances for 8 seconds.
2. Reveal exact bank identifier and copy it; hold 8 seconds. Explain an identifier is distinct from a card number. Show the holder name only when supplied. Keep the card number masked to its last four digits throughout, including after opening details or copying. Copy may use a complete supplied value, but never display or reconstruct it. Confirm the full number is absent from the captured frames.
3. Open Manage card. Hold the unimplemented-services explanation for 12 seconds. No activation/blocking/report/travel API is called. Explain official-channel handoffs and urgent loss/theft action.
4. Return to details and hold 6 seconds.

Capture fixture: `LiveCardsScreenTest.cardServicesExplainUnavailabilityWithoutAdministrationRequests`.

## token

Consent and bank approval precede any active code.

Contract and proof. Hold synthetic contract 10 seconds. Hold consent explanation 8 seconds before enrollment. Hold pending proof 10 seconds; a fixture approval is explicitly simulated.

Active and unlink. Hold generated fictitious code/status 8 seconds. Hold unlink confirmation 8 seconds before accepting, and explain result for 8 seconds.

SMS enrollment step. A separate fake enrollment challenge uses SMS autofill, never typed SMS. Show empty/filled/Verify as in other banking scenes. Do not claim this scenario itself completed enrollment. A generated Token BSC code remains a token, not an SMS.

Capture fixtures: `NativeTokenScreenTest.contractConsentAndBankProofPrecedeCodeDisplayAndUnlinkNeedsConfirmation`, `NativeTokenScreenTest.nativeTokenSmsAutofillStillRequiresVerify`.

## qr

Review the request before sharing or acting on it.

Create and save. Hold account versus payment-request modes; type short fictional purpose/amount readably. Hold completed QR card/details 8 seconds. Demonstrate save cancellation and retry without pretending a bank payment occurred.

Scanner review. Hold injected decoded amount/purpose/currency 8 seconds before explicit recipient review. No real camera capture is claimed.

Print. Hold Android print preview 8 seconds, return without claiming physical printing.

Capture fixtures: `RecipientShareScreenTest.savePreservesSelectedRequestAndCancelAllowsRetry`, `RecipientScanScreenTest.paymentRequestShowsAmountAndPurposeBeforeExplicitRecipientReview`, `RecipientShareScreenTest.printOpensAndroidPrintPreview`.

## settings

Read the SMS assistance explanation for 10 seconds. Disable the actual assistance switch, hold 6 seconds; enable it again, hold 8 seconds. Show delivery preference Ask for 6 seconds and Email for 6 seconds; restore SMS for 8 seconds. Assistance and delivery are separate settings. All subsequent recordings retain assistance enabled and SMS selected.

Show profile, security, help and logout with readable pauses. For an uncertain operation, hold history and its reconciliation acknowledgment for 10 seconds before checking it. Confirm explicitly and hold result 8 seconds; this neither repeats nor cancels the earlier operation.

Capture fixtures: `ShowcaseSmsSettingsTest.deliveryPreferenceReturnsToSms`, `ShowcaseExtraTest.settingsProfileHelpAndLogout`, `LiveScreenTest.moneyReconciliationNeedsLoadedHistoryAndFreshCheckedConfirmation`.

## Overview

104 seconds: thirteen 8-second excerpts in chapter order. Prefer an already visible review, result, or SMS-filled field; preserve a short reading pause. Avoid cuts through tap rings or partial confirmations. No sped-up footage.

## Revision 3 additions before final retakes

- First-use acceptance now leads to an SMS assistance choice; hold its disclosure 8 seconds before enabling. Declining remains supported and does not block login.
- Login adds a separate **synthetic one-message consent result** scene. Hold the pending code screen for 8 seconds, approve the fake consent callback, then hold the automatically completed SMS-only login for 8 seconds. Never draw a fake Android consent dialog or suggest system keyboard autofill has the same submission behavior.
- Verification adds device registration followed by fresh biometric login inside the app. Hold registration disclosure 10 seconds and biometric re-entry 6 seconds; no credentials are silently replayed.
- Settings demonstrates the actual SMS-assistance switch: disable, hold 6 seconds, enable, hold 8 seconds. Show delivery preferences separately and restore SMS.
- Live card administration scenes from revision 2 are superseded by read-only details and an unavailable-services explanation. No simulated loss/theft/travel operations appear in the final publication.
