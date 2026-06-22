# ios-app-share

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/ios-app-share` is a historical Swift iOS installed-app detection
sample. The Xcode project contains an application target and a unit-test target;
despite the repository name, it does not contain an iOS Share Extension.

The sample is preserved for source review rather than as a supported current-iOS
application. Its pinned `iHasApp` 2.2.0 dependency is archived and relies on
broad `canOpenURL:` probing that is no longer a viable detection model under
current Apple platform and App Store restrictions.

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: Swift (3), C/C++ headers (1).

## Repository Contents

- `CHANGES.md` - concise history of maintenance changes
- `Makefile` - local verification entry point
- `Podfile` - Apple platform dependency metadata
- `AppShare` - source or example code
- `AppShare.xcodeproj` - Xcode project file
- `AppShare.xcworkspace` - Xcode workspace including the CocoaPods project
- `AppShareTests` - source or example code
- `Podfile.lock` - Apple platform dependency metadata
- `SECURITY.md` - security reporting and disclosure guidance
- `scripts/check-baseline.py` - static iOS app-detection verifier
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: AppShare, AppShareTests
- Dependency and build manifests: Podfile, Podfile.lock
- Entry points or build surfaces: `make check`, AppShare.xcworkspace, AppShare.xcodeproj
- Test-looking files: AppShareTests/AppShareTests.swift, AppShareTests/Info.plist

## Getting Started

### Prerequisites

- Git
- macOS with Xcode for building Apple platform projects
- CocoaPods 0.36.1 era tooling if dependencies need to be installed or regenerated
- Python 3 for local static verification on non-macOS hosts

### Setup

```bash
git clone https://github.com/garethpaul/ios-app-share.git
cd ios-app-share
make lint
make test
make build
make check
```

Run `pod install` only from a compatible CocoaPods environment when you intentionally need to regenerate the workspace support files.

## Running or Using the Project

- `AppShare.xcworkspace` records the historical app and CocoaPods project
  relationship, but opening it does not imply that the Swift 1-era source or
  retired dependency builds or runs with a current toolchain.
- Do not treat the detection button as a supported current-iOS capability.
  `iHasApp` scans a broad dictionary of third-party URL schemes with
  `canOpenURL:`. Current builds must declare queried schemes, and apps linked on
  or after iOS 15 are limited to 50 declarations, so this broad probing model is
  nonviable rather than something to restore with a scheme allow-list.
- The first-party Swift flow keeps results local-only and does not persist, log,
  or upload them. However, the selected `iHasApp` dictionary API reports
  detected App Store identifiers to `http://itunes.apple.com/lookup` over
  cleartext HTTP. Installed-app results are sensitive device metadata; do not
  use this sample as a privacy-safe implementation.

## Testing and Verification

Run the local static baseline:

```bash
make lint
make test
make build
make check
```

The `lint`, `test`, and `build` targets intentionally alias the static baseline
on hosts without the legacy Xcode toolchain, so the standard local gate commands
stay available while preserving the single source of truth.
GitHub Actions runs the same baseline on macOS and requires current Xcode to
parse `AppShare.xcodeproj` without selecting a simulator.
The hosted `check` job and repository CodeQL analysis do not install CocoaPods,
compile the Swift application, build either Xcode target, or run XCTest. A green
hosted result therefore verifies the static repository contracts only and does
not imply current runtime support.

The baseline runs `scripts/check-baseline.py`, parses plist/storyboard/workspace
XML, checks CocoaPods lockfile and Xcode metadata, verifies the Swift source
inventory, and guards the first-party UI against automatic startup detection,
duplicate scans, missing in-progress detection UI state, missing completed state
button disabling, missing accessibility text for the local-only detection
action, callback UI updates that skip the main queue, logging, or added
network/upload handling. These static checks do not inspect the resolved
CocoaPod's own network behavior.
It also checks state-specific accessibility text for the running, completed,
and retry states of the installed-app detection button.
Accessibility announcements are posted for those user-triggered state changes
so assistive technologies hear detection progress and completion.
Detector lifetime is guarded so the asynchronous `iHasApp` scan remains
retained until success or failure callbacks finish.
Terminal detector and main-queue callbacks capture the controller weakly so the
explicit detector lifetime does not create a retain cycle if the dependency
never completes.
Each scan carries a generation token, so a stale callback from an earlier retry
or a duplicate terminal callback cannot overwrite the active detector state.
A detector construction failure enters the same generation-scoped retry state
before callback registration, avoiding a nil dereference or stuck progress UI.
Each constructed detector also receives a completion timeout. If the retired
dependency never reports success or failure, the active generation returns to
the existing retry state, releases the detector, and ignores any late callback.
Timeout delivery uses a weak timer target and the controller invalidates the
active timeout during teardown, so bounded recovery does not become a controller
lifecycle retain path.
Both AppShare target configurations use the repository-relative bridging header
at `AppShare/Bridge-Header.h`, so checkouts do not depend on a developer home
directory.

For full legacy verification on macOS, use Xcode's test action or `xcodebuild test` with the appropriate scheme and destination.

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.

## Security and Privacy Notes

- Review changes touching network requests, sockets, or service endpoints; examples from the scan include AppShare/Info.plist, AppShareTests/Info.plist.
- Review changes touching file, media, JSON, XML, CSV, OCR, or data parsing; examples from the scan include AppShare/Info.plist, AppShareTests/Info.plist.
- Installed-app detection is sensitive device metadata. The first-party UI is
  user-triggered and handles results local-only, but `iHasApp` 2.2.0's
  dictionary lookup transmits detected App Store identifiers over cleartext
  HTTP. Do not describe the complete dependency path as local-only or reuse it
  without a new privacy and platform design.
- Keep the detection button accessibility text aligned with the first-party
  UI's local result handling without implying that the dependency path is
  local-only.
- Keep accessibility announcements aligned with user-triggered detection state
  changes.

## Maintenance Notes

- Every Make verification target derives the checkout root from the loaded
  Makefile, so an absolute Makefile path works from any working directory.
- See `docs/plans/2026-06-10-hosted-project-validation.md` for the hosted Xcode
  project parsing boundary.
- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-callback-ui-main-queue.md` for the detection callback UI threading guardrail.
- See `docs/plans/2026-06-09-detection-progress-state.md` for the installed-app detection in-progress UI guardrail.
- See `docs/plans/2026-06-09-detection-completed-state.md` for the installed-app detection completed state guardrail.
- See `docs/plans/2026-06-09-detection-accessibility-affordance.md` for the detection accessibility guardrail.
- See `docs/plans/2026-06-09-detection-accessibility-state.md` for
  state-specific accessibility text on the detection button.
- See `docs/plans/2026-06-09-detection-accessibility-announcements.md` for
  detection state accessibility announcements.
- See `docs/plans/2026-06-09-detector-lifetime-guard.md` for the asynchronous
  detector lifetime guardrail.
- See `docs/plans/2026-06-10-detector-callback-retain-cycle.md` for the detector
  callback ownership guardrail.
- See `docs/plans/2026-06-12-stale-detector-callback-guard.md` for stale callback
  and duplicate terminal-result handling.
- See `docs/plans/2026-06-13-relative-bridging-header.md` for checkout-independent
  Objective-C bridge configuration.
- See `docs/plans/2026-06-09-make-gate-aliases.md` for the local gate alias guardrail.
- See `docs/plans/2026-06-10-ci-baseline.md` for the GitHub Actions static
  baseline.
- See `docs/plans/2026-06-17-all-push-checks.md` for canonical hosted checks on
  every branch push and pull request.
- Run `make lint`, `make test`, `make build`, and `make check` before pushing changes to Swift sources, plist/storyboard files, CocoaPods metadata, app-detection behavior, or privacy documentation.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
