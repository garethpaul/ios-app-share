# Release Detection On Memory Warning

status: completed

## Context

The controller releases active detection when the app resigns active or its
view hides, but `didReceiveMemoryWarning` only calls `super`. The retained
detector, timeout, and callback ownership therefore survive a direct UIKit
request to release recreatable memory and restrict active work.

## Design

- Keep the required `super.didReceiveMemoryWarning()` call first.
- Route any in-progress scan through `cancelDetectionForInactiveApp`, the
  existing silent, generation-guarded retry cleanup.
- Preserve success, failure, timeout, stale callback, accessibility, dependency,
  inactive-app, and hidden-view behavior.

## Test First

Require the comment-stripped memory-warning override, UIKit `super` call, and
silent cleanup routing before implementation. The baseline must fail on the
unchanged source.

## Verification

- `python3 scripts/check-baseline.py`
- `/usr/bin/make lint`, `/usr/bin/make test`, `/usr/bin/make build`, and
  `/usr/bin/make check` from the checkout and through the absolute Makefile path
  from `/tmp`
- Hostile mutations removing cleanup, reversing `super` ordering, and commenting
  out cleanup
- `python3 -m py_compile scripts/check-baseline.py`
- `git diff --check`
- Current Xcode compilation is not claimed for this Swift 1-era source-review sample.

The red-first baseline failed on the missing cleanup and incomplete plan. The
completed implementation passed every Make alias from the checkout, the
absolute-Makefile gate from `/tmp`, Python compilation, and `git diff --check`.
Hostile mutations removing cleanup, reversing `super` ordering, and commenting
out cleanup all failed closed.
Hosted static checks and CodeQL Actions/Python passed. `$codex-review` stopped
before analysis with OpenAI HTTP 401 authentication failure; immutable manual
review of exact head `d9cbb22be847bdb61f54b39bce6dc9f103e96f1a` found no
actionable issue.

## Scope Boundaries

- The retired `iHasApp` API exposes no documented cancellation method. This
  change releases sample ownership and ignores late callbacks rather than
  claiming dependency-internal work is forcibly interrupted.
- No dependency, project, storyboard, result handling, storage, logging,
  transmission, or public interface changes are made.

## Reference

- https://developer.apple.com/documentation/uikit/uiviewcontroller/didreceivememorywarning%28%29
