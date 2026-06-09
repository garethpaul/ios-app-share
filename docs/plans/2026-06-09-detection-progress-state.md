# AppShare Detection Progress State

status: completed

## Context

Installed-app detection is user-triggered and guarded against duplicate scans,
but the button kept its initial title while disabled. Users should see that the
local detection action is running.

## Objectives

- Set an explicit disabled title while detection is in progress.
- Preserve the completed and retry button states.
- Keep detection local-only and user-triggered.
- Extend `scripts/check-baseline.py` so the in-progress UI state remains
  covered without Xcode locally.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
