# Changes

## 2026-06-09

- Added an explicit disabled `Detecting...` title while installed-app detection
  is running so the user-triggered action has visible in-progress state.
- Kept the detection button disabled in the completed state so a finished scan
  cannot look retryable after callback ordering changes.
- Added accessibility text that describes the local-only installed-app
  detection action.

## 2026-06-08

- Removed installed-app count debug logging from the detection callback.
- Made installed-app detection user-triggered instead of starting automatically when the view loads.
- Routed detection success and failure UI updates through the main queue.
- Added `make check` and a static iOS app-detection baseline for plist/storyboard XML, CocoaPods lockfiles, Xcode metadata, source inventory, and privacy guardrails.
- Documented the legacy Xcode, CocoaPods 0.36.1, `iHasApp`, workspace, and local-only installed-app detection expectations.
