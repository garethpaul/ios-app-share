# Detector Construction Failure Guard

status: completed

## Context

The user-triggered action calls Objective-C `iHasApp.new()` and immediately
stores and invokes the imported implicitly unwrapped result. If detector
construction returns nil, the sample can dereference nil after disabling the
button and leave the local detection UI stuck in progress.

## Requirements

- R1. Detect a nil `iHasApp.new()` result before detector retention or callback
  registration.
- R2. Route construction failure through the existing generation-scoped retry
  state so the button, accessibility text, and announcement remain consistent.
- R3. Preserve local-only, user-triggered detection and weak callback capture.
- R4. Preserve the active-detector lifetime and stale-callback generation guard
  for successfully constructed detectors.
- R5. Keep compatibility with the Swift 1.2-era source and existing CocoaPods
  and Xcode metadata.

## Scope Boundaries

- Do not log, persist, expose, or transmit installed-app results or errors.
- Do not change dependency locks, project files, bridging headers, workflow
  policy, or accessibility wording.
- Local Linux validation must remain truthful about unavailable `xcodebuild`.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `python3 -m py_compile scripts/check-baseline.py`
- `python3 -c` plist and workflow YAML parsing
- `ruby -c Podfile`
- `git diff --check`
- Hostile mutations must reject removal or reordering of the nil guard, bypass
  of generation-scoped retry state, stale plan status, and missing verification
  evidence.

## Work Completed

- Checked the Objective-C detector construction result before retention or
  callback registration.
- Routed nil construction through the existing generation-scoped failure path,
  preserving retry button and accessibility behavior.
- Added source-ordering contracts so construction failure cannot bypass terminal
  state or occur after detector use.
- Documented the failure boundary without changing dependency, project,
  bridging-header, accessibility-copy, or workflow files.

## Verification Completed

- All four Make gates passed locally and reported that `xcodebuild` was
  unavailable, so only the static iOS baseline ran on this host.
- `python3 -m py_compile scripts/check-baseline.py`, `python3 -c` plist and
  workflow YAML parsing, `ruby -c Podfile`, and `git diff --check` passed.
- Five isolated hostile mutations were rejected: removed nil guard, detector
  retention before the guard, direct button mutation instead of terminal state,
  stale plan status, and missing verification evidence.
- Exact-base comparison confirmed dependencies, Xcode metadata, bridge headers,
  accessibility wording, and hosted workflow configuration remained unchanged.
- Intended-file generated-artifact and secret-pattern scans passed.
- Hosted macOS project parsing and code-scanning evidence is recorded separately
  after push; this plan claims only the completed local static verification.
