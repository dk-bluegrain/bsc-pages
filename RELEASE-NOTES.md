Santa Cruz Modern 1.12.2 (29) updates all seven interface languages: Spanish, English, German, French, Russian, Ukrainian and Portuguese. Android 8.0 (API 26) or later is required. This signed APK release updates existing installations signed with the retained distribution key; no Google Play publication is included.

Changes in this preview:

- Clearer wording for recipient identity, requesting bank quotes, loaded transaction history and uncertain outcomes.
- Corrected saved-login, biometric, Token BSC, statement and demo transaction labels.
- Context comments beside app and website translations document where text appears, its action, arguments and data boundaries.
- Updated website translations, accessible language navigation, localized Android Help links and privacy-page descriptions.

Choose the correct edition:

- **Offline demo** (`com.santacruz.modern.demo`): fictional accounts and simulated operations; no Internet permission, banking credentials or real-money movement. It does not contain every advanced flow shown in the videos.
- **Experimental live banking** (`com.santacruz.modern`): independent client using the existing sideload configuration. Bank authorization, current compatibility and owner-account validation remain unresolved. It is not an official or bank-endorsed application. Existing TLS checks, SMS message consent, explicit financial verification, read-only card services and uncertain-outcome guards are preserved.

Both APKs use the existing distribution certificate, SHA-256:
`ee060319af55793ea750a3f9b0dc4f372a2ba072812d664416a704548f8f5ecd`.
Verify `SHA256SUMS` before installing. Do not uninstall an existing app to bypass a signing mismatch: it may hold token state or unresolved-operation markers. The separate demo package can coexist with the banking edition.

Website videos retain fictional data and fake banking transports. Translation corrections do not establish successful live banking or native-speaker/legal certification. Privacy and download guides: https://dk-bluegrain.github.io/bsc-pages/
