# iOS App Share CI Baseline

status: completed

## Context

The app-detection sample has an SDK-free `make check` baseline for source,
metadata, docs, and privacy guardrails. Full device verification still requires
macOS and the legacy Xcode/CocoaPods toolchain. The missing guard was hosted CI
for the static baseline.

## Changes

- Added `.github/workflows/check.yml` for GitHub Actions.
- Ran the Python static baseline on Ubuntu with Python 3.12.
- Kept full Xcode verification documented as a macOS legacy-toolchain task.
- Extended the checker and docs so the hosted gate remains visible.

## Verification

- `make check`
- `git diff --check`
