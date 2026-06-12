# Hosted Project Validation

status: completed

## Context

The repository had a deterministic local installed-app privacy baseline but no
hosted check enforced it for pushes or pull requests. Linux validation also
cannot confirm that current Xcode still parses the legacy project metadata.

## Completed Scope

- Added a read-only, concurrency-bounded macOS GitHub Actions workflow.
- Pinned the checkout action to a full commit SHA.
- Ran `make check` on pushes to `master` and on pull requests.
- Made the baseline parse `AppShare.xcodeproj` whenever Xcode is available.
- Kept iHasApp runtime behavior, signing, and device-only detection outside the
  hosted metadata boundary.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
