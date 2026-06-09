# Detection Accessibility State

status: completed

## Context

The detection button already describes the local-only installed-app detection
action before a scan starts. Once detection begins, succeeds, or fails, the
button title changes and assistive technologies should receive matching state
text.

## Objectives

- Preserve explicit, user-triggered installed-app detection.
- Add accessibility labels and hints for detecting, completed, and retry states.
- Keep detected app data local-only with no logging or upload behavior.
- Extend the static baseline so state-specific accessibility text remains in
  sync with button state.

## Verification

- `python3 scripts/check-baseline.py`
- `make check`
- `git diff --check`

Full Xcode verification still requires macOS with the legacy project toolchain.
