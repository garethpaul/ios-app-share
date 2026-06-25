# Changes

## 2026-06-25 05:36 - P1 - Release detection when the app becomes inactive

### Summary
Routed in-progress installed-app detection through generation-guarded retry
cleanup when UIKit moves the app out of the active state.

### Work completed
- Added an app-deactivation cleanup entry point on the view controller.
- Reused terminal cleanup while suppressing off-screen accessibility output.
- Wired `applicationWillResignActive` to release timeout and detector ownership.

### Threads
- Started: none — work completed directly in the current repository.
- Continued: none.
- Stopped: none.

### Files changed
- `AppShare/ViewController.swift` — added announcement-aware lifecycle cleanup.
- `AppShare/AppDelegate.swift` — invoked cleanup before app deactivation.
- `scripts/check-baseline.py` — enforced lifecycle routing and plan evidence.
- Documentation and plan files — recorded privacy behavior and validation.

### Validation
- `python3 scripts/check-baseline.py` — failed on the missing inactive-app
  lifecycle contract before implementation and passed afterward.
- `/usr/bin/make check` — passed the complete static privacy and project gate.
- Two isolated hostile mutations removing delegate routing or announcement
  suppression were rejected.
- Codex review found that commented-out delegate routing could satisfy the raw
  source contract; the checker now strips Swift line and nested block comments
  without truncating comment markers inside string literals before extracting
  lifecycle methods, and both hostile mutations are rejected.
- Python compilation and `git diff --check` — passed.
- Hosted static and CodeQL checks — pending PR verification.

### Bugs / findings
- P1: a user-triggered detector, timeout, and callback ownership could remain
  active after the app resigned active, conflicting with the no-background-
  inventory privacy boundary.
- P2: the first lifecycle contract inspected raw delegate source, so a required
  cleanup call copied into a line comment could produce a false pass.

### Blockers
- The pinned Swift 1-era project and retired CocoaPod are source-review only;
  current Xcode does not compile or execute the placeholder XCTest target.

### Next action
- Rerun Codex and hosted review on PR #11 before merge.

## 2026-06-18

- Added a generation-owned detector completion timeout so a missing terminal
  callback returns the local UI to retry state, releases the detector, and
  leaves any late callback unable to overwrite newer work.
- Routed timeout delivery through a weak timer target and invalidated the active
  timer during controller teardown so timeout recovery does not retain the
  controller lifecycle.

## 2026-06-17

- Extended the pinned, read-only hosted baseline from default-branch pushes to
  every branch push while preserving pull-request validation.

## 2026-06-13

- Made every Make verification target derive the checkout root so the static
  app-detection baseline works from external directories.
- Routed detector construction failure through the generation-scoped retry
  state before retention or callback registration.
- Replaced both machine-local AppShare target bridge paths with the
  repository-relative bridging header at `AppShare/Bridge-Header.h`.

## 2026-06-10

- Added pinned, least-privilege macOS GitHub Actions validation for the
  app-detection baseline and current-Xcode project parsing.
- Removed the detector callback retain cycle by capturing the view controller
  weakly in both terminal detector callbacks and main-queue UI updates.
- Preserved explicit detector lifetime through successful and failed scans.
- Guarded terminal scan state with a generation token so a stale callback from
  an earlier retry or a duplicate terminal result cannot overwrite active work.

## 2026-06-09

- Added accessibility announcements for user-triggered detection state changes.
- Added local `make lint`, `make test`, and `make build` gate aliases for the
  static app-detection baseline.
- Added an explicit disabled `Detecting...` title while installed-app detection
  is running so the user-triggered action has visible in-progress state.
- Kept the detection button disabled in the completed state so a finished scan
  cannot look retryable after callback ordering changes.
- Added state-specific accessibility labels and hints for detection running,
  completed, and retry states.
- Added accessibility text that describes the local-only installed-app
  detection action.
- Guarded detector lifetime by retaining the asynchronous `iHasApp` scan until
  success or failure callbacks finish.

## 2026-06-08

- Removed installed-app count debug logging from the detection callback.
- Made installed-app detection user-triggered instead of starting automatically when the view loads.
- Routed detection success and failure UI updates through the main queue.
- Added `make check` and a static iOS app-detection baseline for plist/storyboard XML, CocoaPods lockfiles, Xcode metadata, source inventory, and privacy guardrails.
- Documented the legacy Xcode, CocoaPods 0.36.1, `iHasApp`, workspace, and local-only installed-app detection expectations.
