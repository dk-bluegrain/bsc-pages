Santa Cruz Modern 1.12.1 (28) is an independent Android preview for Android 8.0
(API 26) and later, targeting Android 16/API 36. This is a direct APK distribution;
no Google Play submission is included.

- **Demo** (`com.santacruz.modern.demo`): separately labeled, non-debuggable,
  offline fictional accounts and transactions. No integration credentials,
  Internet permission or native live-login entry. Includes the existing basic
  demo's search, own/saved-recipient transfers, service/card payments, reviews,
  test-code confirmation, receipts, beneficiaries, profile, QR and CSV actions.
- **Experimental live banking** (`com.santacruz.modern`): independently signed
  app with the locally retained original client's shared configuration restored
  only in the sideload variant. Bank authorization and owner-account validation
  remain unresolved. This does not establish current service compatibility.
  Platform TLS/hostname validation, bank login, device approval, token consent,
  explicit financial review/confirmation and uncertain-outcome guards remain.

The seven-language website's advanced recordings use fake bank transports,
fictional identities and synthetic documents. Those walkthroughs do not imply
that advanced statements, native token or live authentication are
available in the simpler downloadable demo.

Both APKs use the dedicated retained distribution key. Verify `SHA256SUMS`
before installing. Signing certificate SHA-256:
`ee060319af55793ea750a3f9b0dc4f372a2ba072812d664416a704548f8f5ecd`.
A different existing signing key prevents an in-place update. Do not uninstall
an owner's app merely to bypass that check: it may contain token state or
unresolved-operation markers. The separate demo can coexist with the normal app.

Changes in this preview:

- Card numbers remain masked to their last four digits throughout details and
  copying. PAN-shaped bank identifiers are masked too. The complete bank-supplied
  number remains available only through the explicit sensitive clipboard action.
- The card walkthrough, screenshots and overview were regenerated from native
  fictional fixtures and show the masked card details.
- Optional SMS assistance, registration re-entry, grouped home services and
  unavailable card-service explanations from 1.12.0 are retained.

The versioned privacy notice is updated. Tests use fake transports only; no
personal credentials or real bank operations are submitted. Owner-device/account
validation remains outstanding.

Privacy policies and current downloads:
https://dk-bluegrain.github.io/bsc-pages/
