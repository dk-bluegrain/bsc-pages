# Download page content context

`download-copy.json` contains complete Spanish (authoritative meaning), English,
German, French, Russian, Ukrainian and Brazilian Portuguese catalogues. Its
`context` map accompanies every key in all seven languages. Values are plain
text, have no arguments and are escaped by `scripts/build.py`. No bank-provided
text or personal data is translated or rewritten. These are website catalogues;
Android XML resources and their acceptance flow are unchanged.

| Keys | Rendering and meaning |
| --- | --- |
| `action` | Landing-page hero and demo-card link to the separate download page. Uses the download action wording and opens the edition choices before an APK is selected. |
| `title`, `intro` | Download document title, metadata and opening heading/paragraph. Exactly two editions; no promise of live eligibility. |
| `demoBadge`, `demoTitle`, `demoBody` | First edition card: offline, fictional, no bank credentials, no real transactions, limited feature scope. |
| `liveBadge`, `liveTitle`, `liveBody` | Second edition card: explicitly unofficial and experimental, real accounts/money possible, unresolved bank permission and validation. |
| `guideAction` | Link from live edition cards to the full disclosure and guide, never directly to an APK. |
| `whyTitle`, `whyBody` | Developer-attributed explanation for avoiding app stores because of the stated conflict with BSC terms. Not a legal determination, bank statement or claim that direct distribution resolves it. |
| `permissionBody` | Explains APK, source-specific installer permission, temporary use, and absence of any need for root. Does not confuse installation permission with banking authorization. |
| `securityTitle`, `securityBody` | Developer's security intent, no intentionally included malware, digitally signed project releases and published SHA-256 sums. No unsupported scanning, certification or audit claim. |
| `verificationBody` | Explicit limits of signatures/checksums and security assurances. A checksum is file matching, not proof of safety. Points to full APK privacy. |
| `riskTitle`, `riskBody` | Prominent own-risk notice including financial/data loss, access, bank changes/restrictions and terms conflicts. No guarantee of login/token/transaction compatibility. |
| `liabilityBody` | As-is/no-warranty and liability disclaimer only to the extent permitted by applicable law; preserves non-waivable rights and liabilities. Not an enforceability guarantee or independent legal review. |
| `guideTitle`, `guideIntro` | Installation heading and Android 8+ scope. Both APKs require source permission; unofficial live use needs additional disclosures. |
| `screensNote` | Actual English Android 15 emulator screenshots with the demo APK, illustrative of device-dependent UI; no personal banking data or operations. |
| `steps[*].title`, `steps[*].body` | Six numbered installation steps: verify the release/edition/hash; open APK/find source settings; temporarily allow only that installer; review/install and respect scans; revoke permission; read app terms and preserve existing app/token/uncertain-operation state on signing mismatch. No suggestion to uninstall to fix a mismatch. |
| `protectBody` | Keep Play Protect enabled, review scans, stop on harmful-app detection, and respect managed-device/Advanced Protection restrictions. Never instructs bypassing these controls. |
| `downloadTitle`, `downloadBody`, `downloadAction` | Real-banking APK download appears after disclosures and guide. Voluntary informed choice, no bank approval or legally protected rights waiver. Not an acceptance form or proof of consent. |
| `checksumLabel` | Visible hashes and filenames from existing `downloads.json`; no manually copied digest or new release. |
| `sourcesLabel` | External primary-source Android installation/Play Protect help, localized via supported `hl` query. |
| `backLabel` | Return to matching-language tour. The header language selector stays on the download route. |

Primary sources checked on 2026-10-16:

- https://support.google.com/android/answer/9457058
- https://support.google.com/googleplay/answer/2812853

The store-publication explanation is the owner's supplied rationale, attributed
to the developer. No specific BSC clause or bank approval was independently
established. Security wording is an intent statement with explicit limits, not
an unsupported virus-free guarantee. No native-speaker or legal certification
is claimed.
