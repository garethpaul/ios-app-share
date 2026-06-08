# Explicit Detection Plan

status: completed

## Context

`ios-app-share` demonstrates installed-app detection, which is sensitive device metadata. The existing baseline keeps results local-only, but the sample still starts detection from `viewDidLoad`.

## Objectives

- Require an explicit user action before installed-app detection runs.
- Prevent duplicate detection runs while a scan is in progress or after one completes.
- Re-enable the action after a detection failure without logging or transmitting error details.
- Extend the static baseline so detection cannot move back into `viewDidLoad`.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
