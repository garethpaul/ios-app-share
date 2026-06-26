# Release Detection When the View Hides

status: completed

## Context

App deactivation already releases an active detector, but an app can remove a
view controller's view while remaining active. The scan, timeout, and callback
ownership could therefore outlive the visible user-triggered screen.

UIKit documents `viewWillDisappear` as the notification that a view is about to
leave the hierarchy and requires subclasses to call `super`.

## Design

- Override `viewWillDisappear` and call `super` first.
- Route cleanup through `cancelDetectionForInactiveApp`, the existing silent,
  generation-guarded retry path.
- Preserve success, timeout, construction failure, stale callback, button,
  accessibility, dependency, and app-deactivation behavior.

## Test First

The comment-stripped baseline required the lifecycle override, UIKit `super`
call, and silent cleanup routing before implementation. It failed on the
unchanged source.

## Verification

- `python3 scripts/check-baseline.py`
- `/usr/bin/make lint`, `/usr/bin/make test`, `/usr/bin/make build`, and
  `/usr/bin/make check` from the checkout and through the absolute Makefile path
  from `/tmp`
- Three isolated hostile mutations removing cleanup, reversing cleanup before
  `super`, or commenting out cleanup
- `python3 -m py_compile scripts/check-baseline.py`
- `git diff --check`
- Current Xcode compilation is not claimed for this Swift 1-era source-review sample.

## Scope Boundaries

- The retired `iHasApp` API exposes no documented cancellation method. This
  change releases sample ownership and ignores late callbacks rather than
  claiming dependency-internal work is forcibly interrupted.
- No dependency, project, storyboard, result handling, storage, logging,
  transmission, or public interface changes were made.

## Reference

- https://developer.apple.com/documentation/uikit/uiviewcontroller/viewwilldisappear%28_%3A%29
