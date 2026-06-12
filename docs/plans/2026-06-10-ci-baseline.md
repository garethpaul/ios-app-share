# iOS App Share CI Baseline

status: completed

## Context

The app-detection sample has an SDK-free `make check` baseline for source,
metadata, docs, and privacy guardrails. Full device verification still requires
macOS and the legacy Xcode/CocoaPods toolchain. The missing guard was hosted CI
for the static baseline.

## Changes

- Added `.github/workflows/check.yml` for GitHub Actions.
- Integrated the static baseline into the pinned, least-privilege macOS gate.
- Required current Xcode to parse `AppShare.xcodeproj` without selecting a
  simulator.
- Extended the checker and docs so the hosted gate remains visible.

## Verification

- `make check`
- `git diff --check`
