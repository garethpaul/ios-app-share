#!/usr/bin/env python3
from pathlib import Path
import plistlib
import re
import shutil
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BASELINE_PLAN = ROOT / "docs/plans/2026-06-08-ios-app-detection-baseline.md"
EXPLICIT_DETECTION_PLAN = ROOT / "docs/plans/2026-06-08-explicit-detection.md"
CALLBACK_UI_PLAN = ROOT / "docs/plans/2026-06-08-callback-ui-main-queue.md"
PROGRESS_PLAN = ROOT / "docs/plans/2026-06-09-detection-progress-state.md"
COMPLETED_STATE_PLAN = ROOT / "docs/plans/2026-06-09-detection-completed-state.md"
ACCESSIBILITY_PLAN = ROOT / "docs/plans/2026-06-09-detection-accessibility-affordance.md"
ACCESSIBILITY_STATE_PLAN = ROOT / "docs/plans/2026-06-09-detection-accessibility-state.md"


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def strip_swift_line_comments(text):
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def swift_function_body(text, signature):
    start = text.find(signature)
    if start == -1:
        return ""

    body_start = text.find("{", start)
    if body_start == -1:
        return ""

    depth = 0
    for index in range(body_start, len(text)):
        character = text[index]
        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth == 0:
                return text[body_start + 1:index]
    return ""


def parse_xml(relative_path, failures):
    try:
        ET.parse(str(ROOT / relative_path))
    except ET.ParseError as error:
        failures.append(f"{relative_path} is not well-formed XML: {error}")


def parse_plist(relative_path, failures):
    try:
        with (ROOT / relative_path).open("rb") as file:
            return plistlib.load(file)
    except Exception as error:
        failures.append(f"{relative_path} is not a readable plist: {error}")
        return {}


def main():
    failures = []
    required_files = [
        ".gitignore",
        "CHANGES.md",
        "Makefile",
        "Podfile",
        "Podfile.lock",
        "README.md",
        "SECURITY.md",
        "VISION.md",
        "AppShare.xcworkspace/contents.xcworkspacedata",
        "AppShare.xcodeproj/project.pbxproj",
        "AppShare/Info.plist",
        "AppShare/AppDelegate.swift",
        "AppShare/Bridge-Header.h",
        "AppShare/ViewController.swift",
        "AppShareTests/AppShareTests.swift",
        "AppShareTests/Info.plist",
        "docs/plans/2026-06-08-ios-app-detection-baseline.md",
        "docs/plans/2026-06-08-explicit-detection.md",
        "docs/plans/2026-06-08-callback-ui-main-queue.md",
        "docs/plans/2026-06-09-detection-progress-state.md",
        "docs/plans/2026-06-09-detection-completed-state.md",
        "docs/plans/2026-06-09-detection-accessibility-affordance.md",
        "docs/plans/2026-06-09-detection-accessibility-state.md",
        "docs/readme-overview.svg",
    ]

    for relative_path in required_files:
        require((ROOT / relative_path).is_file(), f"Required file missing: {relative_path}", failures)

    for xml_file in [
        "AppShare.xcworkspace/contents.xcworkspacedata",
        "AppShare.xcodeproj/project.xcworkspace/contents.xcworkspacedata",
        "AppShare/Base.lproj/Main.storyboard",
        "AppShare/Base.lproj/LaunchScreen.xib",
        "docs/readme-overview.svg",
    ]:
        parse_xml(xml_file, failures)

    app_plist = parse_plist("AppShare/Info.plist", failures)
    test_plist = parse_plist("AppShareTests/Info.plist", failures)
    podfile = read("Podfile")
    podlock = read("Podfile.lock")
    workspace = read("AppShare.xcworkspace/contents.xcworkspacedata")
    project = read("AppShare.xcodeproj/project.pbxproj")
    bridge = read("AppShare/Bridge-Header.h")
    view_controller = read("AppShare/ViewController.swift")
    active_view_controller = strip_swift_line_comments(view_controller)
    readme = read("README.md")
    vision = read("VISION.md")
    security = read("SECURITY.md")
    changes = read("CHANGES.md")
    gitignore = read(".gitignore")
    baseline_plan = BASELINE_PLAN.read_text(encoding="utf-8") if BASELINE_PLAN.exists() else ""
    explicit_detection_plan = EXPLICIT_DETECTION_PLAN.read_text(encoding="utf-8") if EXPLICIT_DETECTION_PLAN.exists() else ""
    callback_ui_plan = CALLBACK_UI_PLAN.read_text(encoding="utf-8") if CALLBACK_UI_PLAN.exists() else ""
    progress_plan = PROGRESS_PLAN.read_text(encoding="utf-8") if PROGRESS_PLAN.exists() else ""
    completed_state_plan = COMPLETED_STATE_PLAN.read_text(encoding="utf-8") if COMPLETED_STATE_PLAN.exists() else ""
    accessibility_plan = ACCESSIBILITY_PLAN.read_text(encoding="utf-8") if ACCESSIBILITY_PLAN.exists() else ""
    accessibility_state_plan = ACCESSIBILITY_STATE_PLAN.read_text(encoding="utf-8") if ACCESSIBILITY_STATE_PLAN.exists() else ""
    view_did_load = swift_function_body(active_view_controller, "override func viewDidLoad")
    detection_action = swift_function_body(active_view_controller, "func detectInstalledApps")

    require("pod 'iHasApp'" in podfile,
            "Podfile must preserve the iHasApp dependency",
            failures)
    require("iHasApp (2.2.0)" in podlock and "COCOAPODS: 0.36.1" in podlock,
            "Podfile.lock must preserve the legacy iHasApp and CocoaPods versions",
            failures)
    require("AppShare.xcodeproj" in workspace and "Pods/Pods.xcodeproj" in workspace,
            "AppShare.xcworkspace must include the app project and Pods project",
            failures)
    require("Check Pods Manifest.lock" in project and "Pods-AppShare.debug.xcconfig" in project,
            "Xcode project must keep CocoaPods integration metadata",
            failures)
    require(app_plist.get("CFBundleIdentifier", "").startswith("com.gpj."),
            "AppShare Info.plist must keep the expected sample bundle identifier",
            failures)
    require(test_plist.get("CFBundlePackageType") == "BNDL",
            "AppShareTests Info.plist must remain a test bundle plist",
            failures)

    require('#import "iHasApp.h"' in bridge,
            "Bridge header must expose iHasApp to Swift",
            failures)
    require("detectAppDictionariesWithIncremental" in detection_action and
            active_view_controller.count("detectAppDictionariesWithIncremental") == 1,
            "ViewController must keep detection behind the explicit action only",
            failures)
    require("self.configureDetectButton()" in view_did_load and "detectAppDictionariesWithIncremental" not in view_did_load,
            "ViewController must not start installed-app detection from viewDidLoad",
            failures)
    require("private let detectButton" in active_view_controller and
            'addTarget(self, action: "detectInstalledApps:", forControlEvents: UIControlEvents.TouchUpInside)' in active_view_controller,
            "ViewController must expose an explicit user action for detection",
            failures)
    require('detectButton.accessibilityLabel = "Detect Installed Apps"' in active_view_controller and
            "detectButton.accessibilityHint" in active_view_controller and
            "without sending results" in active_view_controller,
            "ViewController must describe the local-only detection action for accessibility",
            failures)
    for accessibility_text in [
        "Detecting Installed Apps",
        "Detection is running locally without sending results",
        "Installed App Detection Complete",
        "Detection completed locally and the button is disabled",
        "Try App Detection Again",
        "Previous local detection failed; double tap to retry",
    ]:
        require(accessibility_text in detection_action,
                f"ViewController must keep state-specific accessibility text: {accessibility_text}",
                failures)
    require("private var detectionInProgress = false" in active_view_controller and
            "private var detectionCompleted = false" in active_view_controller and
            "self.detectionInProgress || self.detectionCompleted" in detection_action,
            "ViewController must guard duplicate detection runs",
            failures)
    require("self.detectButton.enabled = false" in detection_action and
            "self.detectButton.enabled = true" in detection_action and
            "self.detectionCompleted = true" in detection_action,
            "ViewController must disable detection while running and re-enable it on failure",
            failures)
    require(detection_action.count("self.detectButton.enabled = false") >= 2,
            "ViewController must keep the detection button disabled after completed success",
            failures)
    require('self.detectButton.setTitle("Detecting...", forState: UIControlState.Disabled)' in detection_action,
            "ViewController must show an in-progress title while detection is running",
            failures)
    require(detection_action.count("dispatch_async(dispatch_get_main_queue())") >= 2,
            "ViewController must update detection button state on the main queue from callbacks",
            failures)
    require(not re.search(r"\b(?:print|println|NSLog)\s*\(", active_view_controller),
            "Detection callback must not log installed-app data or counts",
            failures)
    for forbidden in ["NSURL", "URLSession", "NSURLConnection", "http://", "https://", "upload"]:
        require(forbidden not in active_view_controller,
                f"ViewController must not add network/upload behavior for detected app data: {forbidden}",
                failures)

    swift_files = sorted((ROOT / "AppShare").rglob("*.swift")) + sorted((ROOT / "AppShareTests").rglob("*.swift"))
    require(len(swift_files) >= 3,
            "expected Swift source/test inventory is missing",
            failures)
    require("Pods/" in gitignore and "*.local.xcconfig" in gitignore and ".env" in gitignore,
            ".gitignore must exclude Pods and local secret/config files",
            failures)
    require("make check" in readme and "AppShare.xcworkspace" in readme and "iHasApp" in readme,
            "README must document static verification, workspace usage, and iHasApp",
            failures)
    require("local-only" in readme.lower() and "installed-app" in readme.lower() and "button" in readme.lower() and "main queue" in readme.lower() and "in-progress" in readme.lower() and "completed state" in readme.lower() and "state-specific accessibility" in readme.lower(),
            "README must document local-only, user-triggered installed-app detection",
            failures)
    require("scripts/check-baseline.py" in vision and "local-only" in vision.lower() and "main queue" in vision.lower() and "in-progress" in vision.lower() and "completed state" in vision.lower() and "state-specific accessibility" in vision.lower(),
            "VISION must describe the current static privacy baseline",
            failures)
    require("installed-app" in security.lower() and "make check" in security and "completed state" in security.lower() and "state-specific accessibility" in security.lower(),
            "SECURITY must document installed-app privacy and the static baseline",
            failures)
    require("debug logging" in changes and "make check" in changes and "user-triggered" in changes and "main queue" in changes.lower() and "in-progress" in changes and "completed state" in changes.lower() and "state-specific accessibility" in changes.lower(),
            "CHANGES must record the logging cleanup, user-triggered detection, and baseline",
            failures)
    require("status: completed" in baseline_plan and "status: completed" in explicit_detection_plan and "status: completed" in callback_ui_plan,
            "plans must be marked completed",
            failures)
    require("status: completed" in progress_plan,
            "detection progress state plan must be marked completed",
            failures)
    require("status: completed" in completed_state_plan,
            "detection completed state plan must be marked completed",
            failures)
    require("status: completed" in accessibility_plan,
            "detection accessibility affordance plan must be marked completed",
            failures)
    require("status: completed" in accessibility_state_plan,
            "detection accessibility state plan must be marked completed",
            failures)

    if shutil.which("xcodebuild"):
        print("xcodebuild is available; run a scheme-specific Xcode test on macOS before release.")
    else:
        print("xcodebuild unavailable; static iOS baseline only.")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("ios-app-share app-detection baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
