# iOS App Share Detection Baseline Plan

status: completed

## Context

`ios-app-share` is a legacy Swift iOS app-detection sample that uses `iHasApp` through CocoaPods. This Linux host does not provide Xcode, so local verification needs a static baseline while full app builds remain a macOS/Xcode responsibility.

## Objectives

- Keep installed-app detection local-only and remove debug logging of detection results.
- Add a local `make check` baseline for CocoaPods lockfiles, Xcode metadata, plist/storyboard XML, source inventory, and privacy guardrails.
- Document the legacy workspace, CocoaPods 0.36.1, `iHasApp`, and device-verification expectations.
- Avoid network, upload, or storage behavior for detected installed-app data.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
