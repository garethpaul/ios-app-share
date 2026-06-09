# AppShare Callback UI Main Queue

status: completed

## Context

`detectAppDictionariesWithIncremental` invokes success and failure callbacks
that update detection button state. Because the callback queue is not explicit
in the sample, UI updates should be routed back to the main queue before
changing button title, enabled state, or detection flags.

## Objectives

- Keep installed-app detection user-triggered and local-only.
- Preserve duplicate-run guards and failure retry behavior.
- Dispatch success and failure UI state updates to the main queue.
- Extend the static baseline so callback UI updates stay main-queue guarded.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
