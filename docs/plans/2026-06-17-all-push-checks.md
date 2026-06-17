# All-Push Hosted Checks

status: completed

## Context

The hosted baseline runs for pull requests and pushes to `master`, but it does
not validate feature-branch pushes. That leaves a pushed commit without a
canonical push-event result until a pull request exists, and prevents exact-head
evidence from covering both normal GitHub event paths.

## Requirements

- R1. Run the existing Check workflow for pushes to every branch.
- R2. Preserve pull-request validation, read-only permissions, concurrency
  cancellation, the pinned checkout action, the macOS runner, and the bounded
  job timeout.
- R3. Keep `make check` as the single hosted validation command.
- R4. Add a static contract that rejects restoring a branch-restricted push
  trigger while accepting the explicit all-push form.
- R5. Document the hosted trigger behavior and completed verification
  truthfully.

## Scope Boundaries

- Do not change application behavior, project metadata, dependencies, signing,
  or installed-app data handling.
- Do not broaden workflow permissions or introduce secrets.
- Local Linux validation must remain truthful about unavailable `xcodebuild`.

## Verification

- Parse `.github/workflows/check.yml` as YAML.
- Run `python3 -m py_compile scripts/check-baseline.py`.
- Run `make lint`, `make test`, `make build`, and `make check` from the checkout.
- Run the absolute-path `Makefile` gate from an external directory.
- Run `git diff --check` and intended-file artifact and secret-pattern audits.
- Reject isolated mutations that restore a `master`-only push trigger, remove
  pull-request validation, weaken workflow safeguards, stale the plan status,
  or remove completed verification evidence.

## Work Completed

- Removed the default-branch filter from the existing push trigger so the same
  bounded, read-only job runs for every pushed branch and every pull request.
- Added a static trigger contract that rejects branch-restricted push coverage
  while preserving the workflow safeguards and canonical `make check` command.
- Documented the expanded hosted event coverage without changing app code,
  dependencies, project metadata, or signing.

## Verification Completed

- All four Make gates passed locally and truthfully reported that `xcodebuild`
  was unavailable on this Linux host, so only the static iOS baseline ran.
- The external-directory Make gate passed through the absolute checkout path.
- Workflow YAML parsing, Python bytecode compilation, and `git diff --check`
  passed.
- Six isolated trigger, safeguard, documentation, plan-status, and
  plan-evidence mutations were rejected by the canonical gate.
- Intended-file artifact and credential-pattern scans passed.
