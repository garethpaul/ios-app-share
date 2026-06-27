# AGENTS.md

## Repository purpose

`garethpaul/ios-app-share` is a legacy Swift iOS sample that demonstrates
user-triggered, local-only installed-app detection.

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `Podfile` - CocoaPods dependency definition
- `AppShare.xcodeproj` - Xcode project
- `AppShare.xcworkspace` - Xcode workspace
- `AppShare` - application source, storyboard, assets, and app metadata
- `AppShareTests` - XCTest target and test metadata

## Development commands

- Install dependencies: `pod install`
- Full baseline: `make check`
- Make gates support absolute checkout paths containing spaces; preserve the single-Makefile authority boundary and recursive regression.
- Local Apple development: `open AppShare.xcworkspace`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: Swift (3), C/C++ headers (1).
- Use the CocoaPods workspace when present; update `Podfile.lock` only with an intentional dependency change.
- Preserve legacy Xcode project settings and signing assumptions unless the change is explicitly about modernization.

## Testing guidance

- Test-related files detected: `AppShareTests/AppShareTests.swift`
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.
- Installed-app detection is sensitive device metadata. Keep the sample local-only and user-triggered, avoid debug logging of detection results or counts, and document any future data flow before adding storage or transmission.
- Keep the detection button accessibility text aligned with the local-only privacy boundary.
- Keep terminal state generation-guarded so stale callbacks cannot release a
  newer detector or overwrite its button state.
- Keep the detector completion timeout generation-owned, invalidate it before
  accepted terminal cleanup, and route timeout recovery through the existing
  failure state rather than duplicating button or accessibility mutations.
- Keep timeout delivery weak-targeted and invalidate any active timeout during
  view-controller teardown.
- Keep app deactivation routed through generation-guarded retry cleanup so the
  timeout and detector are released without posting an off-screen accessibility
  announcement.
- Keep view disappearance on the same silent cleanup path so installed-app
  detection ownership does not outlive the visible screen.
- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
