# Detection Accessibility Announcements

status: completed

## Context

The detection button already exposed state-specific accessibility labels and
hints for idle, running, completed, and retry states. Because the running,
completed, and retry states are changed from user-triggered asynchronous work,
assistive technologies should also receive announcements when those states
change.

## Completed Scope

- Centralized detection button accessibility label and hint updates.
- Preserved the initial local-only label and hint without announcing on view
  load.
- Posted accessibility announcements for detecting, completed, and retry states.
- Extended the static privacy baseline so state-change announcements remain
  covered.
- Updated README, VISION, SECURITY, and CHANGES with the announcement guardrail.

## Verification

- `python3 scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
