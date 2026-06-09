# Detection Accessibility Affordance

status: completed

## Context

Installed-app detection is sensitive device metadata and is intentionally
behind an explicit button. The button title is visible, but assistive
technologies should also receive a clear label and hint that describe the
local-only detection action.

## Objectives

- Add accessibility text to the installed-app detection button.
- Preserve explicit, user-triggered detection behavior.
- Keep detection results local-only with no logging or upload behavior.
- Extend the static baseline so the accessibility affordance stays aligned
  with the privacy boundary.

## Verification

- `python3 scripts/check-baseline.py`
- `make check`
- `git diff --check`
