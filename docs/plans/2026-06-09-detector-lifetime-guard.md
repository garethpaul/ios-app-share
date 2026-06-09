# Detector Lifetime Guard

status: completed

## Context

Installed-app detection runs through `iHasApp` callbacks, but the detector was
created as a local variable in the button action. If the detector does not retain
itself for the full asynchronous scan, callbacks could be lost or detection
state could remain stuck in progress.

## Completed Scope

- Added a controller property to retain the active `iHasApp` detector.
- Stored the detector before starting local installed-app detection.
- Released the detector in both success and failure callback paths after UI
  state is updated on the main queue.
- Extended the static privacy baseline and docs to preserve detector lifetime
  handling.

## Verification

- `make check`
- `git diff --check`
