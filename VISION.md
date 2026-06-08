## iOS App Share Vision

iOS App Share is a Swift sample that uses `iHasApp` to detect installed apps and
inspect app dictionaries.

The repository is useful as a legacy iOS app-detection sample with CocoaPods and
a minimal view-controller flow.

The goal is to keep the sample understandable while making device privacy and
legacy API constraints explicit.

The current focus is:

Priority:

- Preserve the app-detection example flow
- Keep CocoaPods setup and `iHasApp` dependency context visible
- Avoid collecting or uploading installed-app data
- Keep security policy aligned with app-detection behavior

Next priorities:

- Add README setup, privacy, and verification instructions
- Document iOS version limitations around installed-app detection
- Modernize Swift and dependency usage in a dedicated pass
- Add tests or manual checks around success and failure callbacks

Contribution rules:

- One PR = one focused app-detection, build, or documentation change.
- Verify behavior on a device when changing detection logic.
- Keep generated signing files and local paths out of git.
- Document any change that stores or transmits detected app data.

## Security And Privacy

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

Installed-app lists are sensitive. The sample should remain local-only unless a
future design explicitly explains user consent, storage, and data flow.

## What We Will Not Merge (For Now)

- Uploading or logging detected installed-app lists
- Background app inventory collection
- Broad Swift migration mixed with detection behavior changes
- Real signing material or private device data

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
