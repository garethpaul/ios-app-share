# Relative Bridging Header Path

status: planned

## Context

Both AppShare target build configurations set `SWIFT_OBJC_BRIDGING_HEADER` to
an absolute path under the original developer's home directory. Xcode project
parsing does not prove that a later compilation can resolve that machine-local
path from another checkout.

The bridging header is already tracked at `AppShare/Bridge-Header.h`, so the
project should reference that repository-relative path in every AppShare target
configuration.

## Priority

The Objective-C bridge exposes the preserved `iHasApp` dependency to Swift. A
machine-local path makes a real build checkout-dependent and can prevent the
only application target from compiling before source validation begins.

## Requirements

- R1. Every AppShare target `SWIFT_OBJC_BRIDGING_HEADER` setting must equal
  `AppShare/Bridge-Header.h`.
- R2. The project must contain no `/Users/`-rooted bridging-header setting.
- R3. Debug and Release must remain aligned without changing the bridge header,
  dependency versions, deployment target, source code, signing, or schemes.
- R4. The canonical checker must enforce the exact relative setting count and
  reject absolute or divergent variants.
- R5. Maintenance, security, vision, and change documentation must record the
  portable project boundary.

## Implementation Units

### U1. Normalize project build settings

- **File:** `AppShare.xcodeproj/project.pbxproj`
- Replace both machine-local AppShare target bridging-header paths with the
  tracked repository-relative path.

### U2. Enforce project portability

- **File:** `scripts/check-baseline.py`
- Require exactly two relative bridge settings and reject absolute home paths.

### U3. Document the build boundary

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`
- Record that app-target configurations resolve the bridge from the checkout.

## Scope Boundaries

- Do not update Swift, CocoaPods, `iHasApp`, deployment targets, signing, or
  generated Pods support files.
- Do not claim full Swift 1.2 compilation when the compatible toolchain is not
  available.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `python3 -m py_compile scripts/check-baseline.py`
- Parse plist, storyboard, XIB, workspace, project, and workflow YAML files.
- `git diff --check`
- Hostile mutations restoring either absolute path, changing one configuration,
  weakening the exact count, or removing completion evidence must be rejected.
