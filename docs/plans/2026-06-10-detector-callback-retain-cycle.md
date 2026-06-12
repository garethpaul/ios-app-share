# Detector Callback Retain-Cycle Guard

status: completed

## Context

The controller intentionally retained `iHasApp` while a scan was in progress,
and the detector retained its terminal callbacks. Those callbacks captured the
controller strongly, forming a controller-to-detector-to-callback retain cycle
until success or failure. A dependency that never completed could therefore
keep the controller alive indefinitely.

## Completed Scope

- Captured the controller weakly in both outer detector callbacks and their
  terminal main-queue UI updates.
- Bound the controller only while applying success or failure UI state.
- Preserved explicit detector retention for the duration of an active scan.
- Preserved main-queue state changes, accessibility announcements, retry
  behavior, and completed-state behavior.
- Extended the static baseline and documentation with the ownership guardrail.

## Verification

- `python3 scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
