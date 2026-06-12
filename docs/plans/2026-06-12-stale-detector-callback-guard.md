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

## Work Completed

- Assigned a monotonically increasing generation to user-triggered scans and
  required callbacks to match the active generation while detection remains
  in progress.
- Centralized terminal cleanup and button-state transitions while preserving
  weak capture, main-queue UI work, local-only handling, and retries.
- Added static contracts for both stale-generation and duplicate-terminal
  callback rejection.

## Verification Completed

- All four Make gates, checker compilation, and `git diff --check` passed
  locally; Xcode project parsing was truthfully skipped because Xcode is
  unavailable in the local environment.
- Pull-request run `27394392145` passed at commit
  `b7681f0f561c99e4fc90a4bafd288ca0ccec5f23`; the hosted macOS gate included
  the detection baseline and Xcode project parsing.
- Post-merge push run `27394408704` and CodeQL setup run `27402322743` passed
  at default-branch merge commit `d8b47077f87f6f5c8773168df12d7d08d4bff1e0`.
- Mutations removing either the generation comparison or in-progress guard
  were rejected by the baseline.
