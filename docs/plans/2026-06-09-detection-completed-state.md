# Detection Completed State

status: completed

## Context

The app-detection button is disabled before `iHasApp` scanning starts and is
re-enabled on failure for retry. The success callback also needs to make the
terminal completed state explicit so a late success after a retry failure cannot
leave the control visually or accessibility-wise enabled.

## Objectives

- Disable the detection button again when the success callback marks detection
  completed.
- Preserve the existing retry behavior on failure.
- Extend the static baseline to require the completed-state button guard.
- Document the completed state alongside the in-progress detection UI guard.

## Verification

- `make check`
- `git diff --check`
