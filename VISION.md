## iOS App Share Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

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
- Keep installed-app detection user-triggered rather than automatic on launch
- Keep security policy aligned with app-detection behavior
- Keep `scripts/check-baseline.py` passing for local-only detection, plist
  metadata, CocoaPods lockfiles, Xcode metadata, callback UI threading, and
  detector lifetime, accessibility announcements, and accessibility/source
  inventory
- Keep `make lint`, `make test`, `make build`, and `make check` available as
  local verification gates
- Keep pinned macOS CI parsing `AppShare.xcodeproj` through the canonical gate
- Ignore stale callbacks from earlier retries and duplicate terminal results
- Bound detector completion with a timeout that returns an abandoned scan to
  retry state and ignores any late callback
- Release active detector and timeout ownership when the app resigns active,
  without announcing state changes off-screen
- Release temporary detector ownership when UIKit reports memory pressure
- Route detector construction failure through generation-scoped retry state
- Keep a repository-relative bridging header in every AppShare configuration

Next priorities:

- Modernize Swift and dependency usage in a dedicated pass

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

Current baseline: `make lint`, `make test`, `make build`, and `make check` run
`scripts/check-baseline.py` without Xcode. It verifies the CocoaPods/iHasApp
metadata, app plist and workspace XML, installed-app logging guardrails, and
local-only detection expectations. It also verifies that detection remains
behind an explicit user action and is not started from `viewDidLoad`, that the
disabled button shows in-progress state while detection is running, and that
callback-driven button state changes return to the main queue. The completed state
keeps the detection button disabled after success. State-specific accessibility
text should describe the local-only detection action with labels and hints.
Accessibility announcements should describe user-triggered state changes for
running, completed, and retry states.
Detector lifetime should remain explicit while asynchronous scans are running.
Terminal detector and main-queue callbacks should avoid a controller retain cycle
while preserving main-queue UI updates.
Only the active in-progress scan generation should apply a terminal result, so
stale callback work cannot release a newer detector or overwrite its UI state.
A completion timeout should route a detector that never finishes through the
same generation-scoped retry path, release it, and leave any late callback
inert.
Timeout delivery should use a weak target and controller teardown should
invalidate the active timer so lifecycle cleanup does not depend on the timeout
firing.
The inactive app lifecycle should use the same generation-guarded retry cleanup
so installed-app detection state is not retained across deactivation.
View disappearance should use that silent cleanup before the screen leaves the
hierarchy so detector ownership remains bounded to visible user interaction.
Memory warnings should use the same silent cleanup after `super` so temporary
detector and timeout ownership are released under system pressure.
The repository-relative bridging header should keep Objective-C dependency
resolution independent of the original developer's checkout path.

## What We Will Not Merge (For Now)

- Uploading or logging detected installed-app lists
- Background app inventory collection
- Broad Swift migration mixed with detection behavior changes
- Real signing material or private device data

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
