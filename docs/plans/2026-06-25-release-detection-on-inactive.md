# Release Detection When Inactive

status: completed

## Context

The sample bounded stalled detectors with a timer but retained the active
detector and timeout when the app resigned active. That allowed sensitive
installed-app work and callback ownership to outlive the foreground action.

UIKit's lifecycle guidance says `applicationWillResignActive` should pause
ongoing tasks and disable timers while the inactive app does minimal work.

## Design

- Extend `finishDetection` with an announcement flag that defaults to the
  existing user-visible behavior.
- Add `cancelDetectionForInactiveApp`, routing the current generation through
  the existing failure cleanup with announcements disabled.
- Have `AppDelegate.applicationWillResignActive` call that method on the root
  `ViewController` before entering the inactive state.

The accepted terminal path invalidates and clears the timeout, releases the
detector, marks detection idle, restores retry UI, and leaves late callbacks
rejected by the existing in-progress and generation checks.

## Test First

The static baseline required lifecycle routing, the default announcement
parameter, and two state-dependent announcement uses before implementation. It
failed on the unchanged source.

## Verification

- `python3 scripts/check-baseline.py`
- `/usr/bin/make check`
- Isolated hostile mutations removing delegate routing or announcement
  suppression
- Isolated hostile mutation commenting out delegate routing
- Isolated hostile mutation block-commenting delegate routing
- `python3 -m py_compile scripts/check-baseline.py`
- `git diff --check`
- Current Xcode compilation is not claimed for this Swift 1-era source-review
  sample.

## Scope Boundaries

- Detection remains explicit and user-triggered; success, timeout, construction
  failure, stale callback, dependency, project, and completed-state behavior are
  unchanged.
- The retired `iHasApp` API exposes no documented cancellation method. This
  change releases sample ownership and ignores late callbacks rather than
  claiming the dependency's internal work is forcibly interrupted.

## References

- https://developer.apple.com/documentation/uikit/uiapplicationdelegate/applicationwillresignactive%28_%3A%29
- https://cocoapods.org/pods/iHasApp
