# Platform And Callback Roadmap Reconciliation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Retire completed platform-limit and callback-verification roadmap items while preserving their source-backed evidence and validation boundaries.

**Architecture:** Keep the historical Swift application and retired `iHasApp` dependency unchanged. Add a fail-closed documentation contract that binds the README to the maintained deployment, dependency, privacy, callback, and hosted-validation evidence; then remove only the roadmap entries already proven complete.

**Tech Stack:** Markdown, Python 3 static contracts, GNU Make, legacy Swift/iOS project metadata

---

status: completed

### Task 1: Add The Failing Documentation Contract

**Files:**
- Modify: `scripts/check-baseline.py`
- Test: `scripts/check-baseline.py`

**Step 1: Require maintained evidence**

Require a dedicated README section covering the iOS 8.3/Swift 1-era baseline,
current `canOpenURL:` limitations, cleartext lookup privacy boundary, success
and failure callback handling, static-versus-native verification boundary, and
the completed reconciliation plan.

**Step 2: Run the checker and confirm red**

Run: `python3 scripts/check-baseline.py`

Expected: FAIL because the dedicated evidence section is absent, VISION still
lists completed work as future priority, and this plan is not completed.

### Task 2: Reconcile Roadmap And Evidence

**Files:**
- Modify: `README.md`
- Modify: `VISION.md`
- Modify: `CHANGES.md`
- Modify: `docs/plans/2026-06-26-platform-callback-roadmap-reconciliation.md`

**Step 1: Add concise maintained guidance**

Document the exact historical platform boundary and the callback behaviors
covered by the portable checker. State explicitly that current Xcode only
parses the project and does not compile or execute the Swift application.

**Step 2: Retire only completed roadmap entries**

Remove the platform-limit documentation and callback-check priorities from
VISION. Retain the separate Swift/dependency modernization priority.

**Step 3: Record the cycle**

Add a newest-first `CHANGES.md` entry with scope, files, validation, findings,
blockers, and next action. Mark this plan completed only after validation.

### Task 3: Validate The Exact Change

**Files:**
- Verify: `Makefile`
- Verify: `scripts/check-baseline.py`

**Step 1: Run focused and full gates**

Run: `python3 scripts/check-baseline.py`

Run: `python3 -m py_compile scripts/check-baseline.py`

Run: `/usr/bin/make lint test build check`

Run from `/tmp`: `/usr/bin/make -f /absolute/path/to/Makefile lint test build check`

Expected: all portable gates pass; local Xcode absence is reported honestly.

**Step 2: Check patch hygiene**

Run: `git diff --check`

Expected: PASS.

### Task 4: Ship And Review

**Files:**
- Verify: all changed files

**Step 1: Push a focused pull request**

Commit the exact validated files, push the branch, and open a public PR.

**Step 2: Run exact-head review**

Invoke `$codex-review`, inspect hosted checks, and merge only the reviewed head
after all required checks pass. Skip authentication-only review failures as
directed, but perform a manual diff review before merge.

## Verification Completed

- The maintained README section is `Historical Platform And Callback Evidence`.
- The red-first checker rejected the missing evidence section, stale VISION
  priorities, absent change record, and incomplete plan.
- Eleven isolated hostile documentation mutations were rejected across the
  evidence heading, platform baseline, current-iOS limitation, cleartext lookup,
  callback threading, stale-result handling, native-validation boundary, both
  retired roadmap entries, change record, and plan status.
- `python3 scripts/check-baseline.py` passed.
- `python3 -m py_compile scripts/check-baseline.py` passed.
- `/usr/bin/make lint test build check` passed from the checkout.
- All four Make gates passed from an external working directory through the
  absolute Makefile path.
- `git diff --check` passed.
- Local `xcodebuild` was unavailable; hosted macOS project parsing remains the
  Apple-tooling authority and does not claim Swift compilation or XCTest.

## Scope Boundaries

- No Swift, Objective-C, dependency, project, workspace, plist, storyboard,
  build, signing, storage, logging, transmission, or runtime behavior changed.
- The retained modernization priority requires a separate design and compatible
  Apple toolchain rather than being implied by documentation cleanup.
