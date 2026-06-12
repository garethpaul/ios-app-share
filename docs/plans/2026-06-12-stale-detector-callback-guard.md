# Stale Detector Callback Guard

status: completed

## Context

The detector's success and failure callbacks are asynchronous and both enqueue
UI work. If a detector invokes more than one terminal callback, or an earlier
failed attempt reports late after the user starts a retry, stale work can clear
the current detector and overwrite the active scan's button state. That can
also release the new detector before its own terminal callback arrives.

## Completed Scope

- Assign a monotonically increasing generation to each user-triggered scan.
- Apply success or failure state only when the callback belongs to the active
  generation and detection is still in progress.
- Centralize terminal detector cleanup and button state transitions.
- Preserve weak callback capture, main-queue UI updates, local-only handling,
  and retry behavior.
- Extend the static baseline with stale and duplicate callback guard contracts.

## Verification

- `make check`
- `git diff --check`
- Mutations that remove either the generation comparison or in-progress guard
  must fail the baseline.
- Hosted macOS validation must parse `AppShare.xcodeproj`.
