#!/usr/bin/env python3
from pathlib import Path
import plistlib
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BASELINE_PLAN = ROOT / "docs/plans/2026-06-08-ios-app-detection-baseline.md"
MAKE_GATES_PLAN = ROOT / "docs/plans/2026-06-09-make-gate-aliases.md"
EXPLICIT_DETECTION_PLAN = ROOT / "docs/plans/2026-06-08-explicit-detection.md"
CALLBACK_UI_PLAN = ROOT / "docs/plans/2026-06-08-callback-ui-main-queue.md"
PROGRESS_PLAN = ROOT / "docs/plans/2026-06-09-detection-progress-state.md"
COMPLETED_STATE_PLAN = ROOT / "docs/plans/2026-06-09-detection-completed-state.md"
ACCESSIBILITY_PLAN = ROOT / "docs/plans/2026-06-09-detection-accessibility-affordance.md"
ACCESSIBILITY_STATE_PLAN = ROOT / "docs/plans/2026-06-09-detection-accessibility-state.md"
DETECTOR_LIFETIME_PLAN = ROOT / "docs/plans/2026-06-09-detector-lifetime-guard.md"
ACCESSIBILITY_ANNOUNCEMENT_PLAN = ROOT / "docs/plans/2026-06-09-detection-accessibility-announcements.md"
CALLBACK_RETAIN_CYCLE_PLAN = ROOT / "docs/plans/2026-06-10-detector-callback-retain-cycle.md"
CI_BASELINE_PLAN = ROOT / "docs/plans/2026-06-10-ci-baseline.md"
HOSTED_VALIDATION_PLAN = ROOT / "docs/plans/2026-06-10-hosted-project-validation.md"
STALE_CALLBACK_PLAN = ROOT / "docs/plans/2026-06-12-stale-detector-callback-guard.md"
RELATIVE_BRIDGE_PLAN = ROOT / "docs/plans/2026-06-13-relative-bridging-header.md"
DETECTOR_CONSTRUCTION_PLAN = ROOT / "docs/plans/2026-06-13-detector-construction-failure.md"
LOCATION_INDEPENDENT_MAKE_PLAN = ROOT / "docs/plans/2026-06-13-location-independent-make.md"
ALL_PUSH_CHECKS_PLAN = ROOT / "docs/plans/2026-06-17-all-push-checks.md"
DETECTOR_TIMEOUT_PLAN = ROOT / "docs/plans/2026-06-18-001-fix-detector-timeout-plan.md"
INACTIVE_DETECTION_PLAN = ROOT / "docs/plans/2026-06-25-release-detection-on-inactive.md"
HIDDEN_VIEW_DETECTION_PLAN = ROOT / "docs/plans/2026-06-26-release-detection-on-view-hide.md"
MEMORY_WARNING_DETECTION_PLAN = ROOT / "docs/plans/2026-06-26-release-detection-on-memory-warning.md"
ROADMAP_RECONCILIATION_PLAN = ROOT / "docs/plans/2026-06-26-platform-callback-roadmap-reconciliation.md"


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def strip_swift_comments(text):
    result = []
    index = 0
    block_depth = 0
    in_string = False
    escaped = False

    while index < len(text):
        character = text[index]
        next_character = text[index + 1] if index + 1 < len(text) else ""

        if block_depth:
            if character == "/" and next_character == "*":
                block_depth += 1
                index += 2
                continue
            if character == "*" and next_character == "/":
                block_depth -= 1
                index += 2
                continue
            if character == "\n":
                result.append(character)
            index += 1
            continue

        if in_string:
            result.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            index += 1
            continue

        if character == '"':
            in_string = True
            result.append(character)
            index += 1
            continue
        if character == "/" and next_character == "/":
            newline = text.find("\n", index + 2)
            if newline == -1:
                break
            result.append("\n")
            index = newline + 1
            continue
        if character == "/" and next_character == "*":
            block_depth = 1
            index += 2
            continue

        result.append(character)
        index += 1

    return "".join(result)


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
        ".github/workflows/check.yml",
        ".github/CODEOWNERS",
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
        "docs/plans/2026-06-09-make-gate-aliases.md",
        "docs/plans/2026-06-08-explicit-detection.md",
        "docs/plans/2026-06-08-callback-ui-main-queue.md",
        "docs/plans/2026-06-09-detection-progress-state.md",
        "docs/plans/2026-06-09-detection-completed-state.md",
        "docs/plans/2026-06-09-detection-accessibility-affordance.md",
        "docs/plans/2026-06-09-detection-accessibility-state.md",
        "docs/plans/2026-06-09-detector-lifetime-guard.md",
        "docs/plans/2026-06-09-detection-accessibility-announcements.md",
        "docs/plans/2026-06-10-detector-callback-retain-cycle.md",
        "docs/plans/2026-06-10-ci-baseline.md",
        "docs/plans/2026-06-10-hosted-project-validation.md",
        "docs/plans/2026-06-12-stale-detector-callback-guard.md",
        "docs/plans/2026-06-13-relative-bridging-header.md",
        "docs/plans/2026-06-13-detector-construction-failure.md",
        "docs/plans/2026-06-13-location-independent-make.md",
        "docs/plans/2026-06-17-all-push-checks.md",
        "docs/plans/2026-06-18-001-fix-detector-timeout-plan.md",
        "docs/plans/2026-06-25-release-detection-on-inactive.md",
        "docs/plans/2026-06-26-release-detection-on-view-hide.md",
        "docs/plans/2026-06-26-release-detection-on-memory-warning.md",
        "docs/plans/2026-06-26-platform-callback-roadmap-reconciliation.md",
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
    app_delegate = read("AppShare/AppDelegate.swift")
    active_app_delegate = strip_swift_comments(app_delegate)
    view_controller = read("AppShare/ViewController.swift")
    active_view_controller = strip_swift_comments(view_controller)
    readme = read("README.md")
    vision = read("VISION.md")
    security = read("SECURITY.md")
    changes = read("CHANGES.md")
    gitignore = read(".gitignore")
    makefile = read("Makefile")
    baseline_plan = BASELINE_PLAN.read_text(encoding="utf-8") if BASELINE_PLAN.exists() else ""
    make_gates_plan = MAKE_GATES_PLAN.read_text(encoding="utf-8") if MAKE_GATES_PLAN.exists() else ""
    explicit_detection_plan = EXPLICIT_DETECTION_PLAN.read_text(encoding="utf-8") if EXPLICIT_DETECTION_PLAN.exists() else ""
    callback_ui_plan = CALLBACK_UI_PLAN.read_text(encoding="utf-8") if CALLBACK_UI_PLAN.exists() else ""
    progress_plan = PROGRESS_PLAN.read_text(encoding="utf-8") if PROGRESS_PLAN.exists() else ""
    completed_state_plan = COMPLETED_STATE_PLAN.read_text(encoding="utf-8") if COMPLETED_STATE_PLAN.exists() else ""
    accessibility_plan = ACCESSIBILITY_PLAN.read_text(encoding="utf-8") if ACCESSIBILITY_PLAN.exists() else ""
    accessibility_state_plan = ACCESSIBILITY_STATE_PLAN.read_text(encoding="utf-8") if ACCESSIBILITY_STATE_PLAN.exists() else ""
    detector_lifetime_plan = DETECTOR_LIFETIME_PLAN.read_text(encoding="utf-8") if DETECTOR_LIFETIME_PLAN.exists() else ""
    accessibility_announcement_plan = ACCESSIBILITY_ANNOUNCEMENT_PLAN.read_text(encoding="utf-8") if ACCESSIBILITY_ANNOUNCEMENT_PLAN.exists() else ""
    callback_retain_cycle_plan = CALLBACK_RETAIN_CYCLE_PLAN.read_text(encoding="utf-8") if CALLBACK_RETAIN_CYCLE_PLAN.exists() else ""
    ci_baseline_plan = CI_BASELINE_PLAN.read_text(encoding="utf-8") if CI_BASELINE_PLAN.exists() else ""
    hosted_validation_plan = HOSTED_VALIDATION_PLAN.read_text(encoding="utf-8") if HOSTED_VALIDATION_PLAN.exists() else ""
    stale_callback_plan = STALE_CALLBACK_PLAN.read_text(encoding="utf-8") if STALE_CALLBACK_PLAN.exists() else ""
    relative_bridge_plan = RELATIVE_BRIDGE_PLAN.read_text(encoding="utf-8") if RELATIVE_BRIDGE_PLAN.exists() else ""
    detector_construction_plan = DETECTOR_CONSTRUCTION_PLAN.read_text(encoding="utf-8") if DETECTOR_CONSTRUCTION_PLAN.exists() else ""
    location_independent_make_plan = LOCATION_INDEPENDENT_MAKE_PLAN.read_text(encoding="utf-8") if LOCATION_INDEPENDENT_MAKE_PLAN.exists() else ""
    all_push_checks_plan = ALL_PUSH_CHECKS_PLAN.read_text(encoding="utf-8") if ALL_PUSH_CHECKS_PLAN.exists() else ""
    detector_timeout_plan = DETECTOR_TIMEOUT_PLAN.read_text(encoding="utf-8") if DETECTOR_TIMEOUT_PLAN.exists() else ""
    inactive_detection_plan = INACTIVE_DETECTION_PLAN.read_text(encoding="utf-8") if INACTIVE_DETECTION_PLAN.exists() else ""
    hidden_view_detection_plan = HIDDEN_VIEW_DETECTION_PLAN.read_text(encoding="utf-8") if HIDDEN_VIEW_DETECTION_PLAN.exists() else ""
    memory_warning_detection_plan = MEMORY_WARNING_DETECTION_PLAN.read_text(encoding="utf-8") if MEMORY_WARNING_DETECTION_PLAN.exists() else ""
    roadmap_reconciliation_plan = ROADMAP_RECONCILIATION_PLAN.read_text(encoding="utf-8") if ROADMAP_RECONCILIATION_PLAN.exists() else ""
    workflow = read(".github/workflows/check.yml")
    view_did_load = swift_function_body(active_view_controller, "override func viewDidLoad")
    view_will_disappear = swift_function_body(active_view_controller, "override func viewWillDisappear")
    memory_warning = swift_function_body(active_view_controller, "override func didReceiveMemoryWarning")
    detection_action = swift_function_body(active_view_controller, "func detectInstalledApps")
    terminal_state = swift_function_body(active_view_controller, "private func finishDetection")
    inactive_cancellation = swift_function_body(active_view_controller, "func cancelDetectionForInactiveApp")
    will_resign_active = swift_function_body(active_app_delegate, "func applicationWillResignActive")
    timeout_scheduler = swift_function_body(active_view_controller, "private func scheduleDetectionTimeout")
    timeout_handler = swift_function_body(active_view_controller, "func detectionTimedOut")
    deinit_body = swift_function_body(active_view_controller, "deinit")

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
    require(project.count("SWIFT_OBJC_BRIDGING_HEADER = AppShare/Bridge-Header.h;") == 2 and
            re.search(r"SWIFT_OBJC_BRIDGING_HEADER\s*=\s*\"?/", project) is None,
            "Debug and Release must use the repository-relative AppShare bridging header",
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
    require('self.updateDetectButtonAccessibility(\n            "Detect Installed Apps"' in active_view_controller and
            "Runs local installed-app detection without sending results" in active_view_controller and
            "without sending results" in active_view_controller,
            "ViewController must describe the local-only detection action for accessibility",
            failures)
    require("private func updateDetectButtonAccessibility" in active_view_controller and
            "UIAccessibilityPostNotification(UIAccessibilityAnnouncementNotification, label)" in active_view_controller,
            "ViewController must announce detection state changes to assistive technologies",
            failures)
    require(active_view_controller.count("announce: true") >= 1 and
            active_view_controller.count("announce: announce") == 2 and
            "announce: false" in active_view_controller,
            "ViewController must announce running, completed, and retry detection states only after user-triggered changes",
            failures)
    for accessibility_text in [
        "Detecting Installed Apps",
        "Detection is running locally without sending results",
        "Installed App Detection Complete",
        "Detection completed locally and the button is disabled",
        "Try App Detection Again",
        "Previous local detection failed; double tap to retry",
    ]:
        require(accessibility_text in active_view_controller,
                f"ViewController must keep state-specific accessibility text: {accessibility_text}",
                failures)
    require("private var detectionInProgress = false" in active_view_controller and
            "private var detectionCompleted = false" in active_view_controller and
            "self.detectionInProgress || self.detectionCompleted" in detection_action,
            "ViewController must guard duplicate detection runs",
            failures)
    require("private var appDetector: iHasApp?" in active_view_controller and
            "self.appDetector = detect" in detection_action and
            "self.appDetector = nil" in terminal_state,
            "ViewController must retain the app detector during asynchronous detection and release it after callbacks",
            failures)
    require("private let detectionTimeoutInterval: NSTimeInterval = 30.0" in active_view_controller and
            "private var detectionTimeoutTimer: NSTimer?" in active_view_controller,
            "ViewController must keep a named, retained completion timeout",
            failures)
    detector_new_index = detection_action.find("let detect = iHasApp.new()")
    detector_nil_index = detection_action.find("if detect == nil")
    detector_failure_index = detection_action.find(
        "self.finishDetection(detectionGeneration, succeeded: false)")
    detector_retain_index = detection_action.find("self.appDetector = detect")
    detector_timeout_index = detection_action.find(
        "self.scheduleDetectionTimeout(detectionGeneration)")
    detector_callback_index = detection_action.find(
        "detect.detectAppDictionariesWithIncremental")
    require(-1 not in [detector_new_index, detector_nil_index,
                       detector_failure_index, detector_retain_index,
                       detector_timeout_index, detector_callback_index] and
            detector_new_index < detector_nil_index < detector_failure_index <
            detector_retain_index < detector_timeout_index < detector_callback_index,
            "Detector construction failure must precede retention, timeout scheduling, and callbacks",
            failures)
    require("NSTimer.scheduledTimerWithTimeInterval" in timeout_scheduler and
            "self.detectionTimeoutInterval" in timeout_scheduler and
            "target: self.detectionTimeoutTarget" in timeout_scheduler and
            'selector: "timerFired:"' in timeout_scheduler and
            "userInfo: NSNumber(integer: generation)" in timeout_scheduler and
            "repeats: false" in timeout_scheduler,
            "Each successful detector construction must schedule one generation-owned timeout",
            failures)
    require("private final class WeakTimerTarget: NSObject" in active_view_controller and
            "private weak var viewController: ViewController?" in active_view_controller and
            "self.viewController?.detectionTimedOut(timer)" in active_view_controller and
            "private lazy var detectionTimeoutTarget" in active_view_controller and
            "target: self," not in timeout_scheduler,
            "Detector timeout timer must use a weak target instead of retaining the view controller",
            failures)
    require("timer.userInfo as? NSNumber" in timeout_handler and
            "self.finishDetection(generation.integerValue, succeeded: false)" in timeout_handler,
            "Timeout delivery must reuse generation-scoped failure state",
            failures)
    require("self.detectionTimeoutTimer?.invalidate()" in deinit_body,
            "ViewController teardown must invalidate any active detector timeout",
            failures)
    timeout_invalidate_index = terminal_state.find("self.detectionTimeoutTimer?.invalidate()")
    timeout_clear_index = terminal_state.find("self.detectionTimeoutTimer = nil")
    detector_clear_index = terminal_state.find("self.appDetector = nil")
    require(-1 not in [timeout_invalidate_index, timeout_clear_index, detector_clear_index] and
            timeout_invalidate_index < timeout_clear_index < detector_clear_index,
            "Accepted terminal state must invalidate and clear the timeout before releasing the detector",
            failures)
    require("detectButton.enabled = false" in active_view_controller and
            "detectButton.enabled = true" in terminal_state and
            "detectionCompleted = true" in terminal_state,
            "ViewController must disable detection while running and re-enable it on failure",
            failures)
    require(active_view_controller.count("detectButton.enabled = false") >= 2,
            "ViewController must keep the detection button disabled after completed success",
            failures)
    require('self.detectButton.setTitle("Detecting...", forState: UIControlState.Disabled)' in detection_action,
            "ViewController must show an in-progress title while detection is running",
            failures)
    require(detection_action.count("dispatch_async(dispatch_get_main_queue())") >= 2,
            "ViewController must update detection button state on the main queue from callbacks",
            failures)
    require(detection_action.count("[weak self]") >= 4 and
            detection_action.count("if let strongSelf = self") >= 2,
            "Terminal detector and main-queue callbacks must not retain the view controller",
            failures)
    require("private var detectionGeneration = 0" in active_view_controller and
            "self.detectionGeneration += 1" in detection_action and
            "let detectionGeneration = self.detectionGeneration" in detection_action and
            detection_action.count("finishDetection(detectionGeneration") == 3,
            "Each scan must capture a generation for construction failure and both terminal callbacks",
            failures)
    require("generation != self.detectionGeneration" in terminal_state and
            "!self.detectionInProgress" in terminal_state and
            "return" in terminal_state,
            "Terminal callbacks must ignore stale generations and duplicate results",
            failures)
    require("announce: Bool = true" in active_view_controller and
            terminal_state.count("announce: announce") == 2 and
            inactive_cancellation.count("self.finishDetection(self.detectionGeneration, succeeded: false, announce: false)") == 1 and
            "self.window?.rootViewController as? ViewController" in will_resign_active and
            "viewController.cancelDetectionForInactiveApp()" in will_resign_active,
            "App deactivation must release active detector state through the generation-guarded retry path without announcing off-screen",
            failures)
    require("super.viewWillDisappear(animated)" in view_will_disappear and
            "self.cancelDetectionForInactiveApp()" in view_will_disappear and
            view_will_disappear.find("super.viewWillDisappear(animated)") <
            view_will_disappear.find("self.cancelDetectionForInactiveApp()"),
            "View disappearance must release active detector state silently after calling super",
            failures)
    require("super.didReceiveMemoryWarning()" in memory_warning and
            "self.cancelDetectionForInactiveApp()" in memory_warning and
            memory_warning.find("super.didReceiveMemoryWarning()") <
            memory_warning.find("self.cancelDetectionForInactiveApp()"),
            "Memory warnings must release active detector state silently after calling super",
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
    require(".PHONY: build check lint test" in makefile and "lint test build: check" in makefile,
            "Makefile must expose lint, test, and build aliases for the local baseline",
            failures)
    require("override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))" in makefile and '@python3 "$(ROOT)/scripts/check-baseline.py"' in makefile,
            "Makefile must invoke the checker through the loaded checkout root", failures)
    require("absolute Makefile path" in readme and "any working directory" in readme,
            "README must document location-independent verification", failures)
    require("Make verification target derive the checkout root" in changes and "external directories" in changes,
            "CHANGES must record location-independent verification", failures)
    require("make lint" in readme and "make test" in readme and "make build" in readme and "make check" in readme and "GitHub Actions" in readme and "AppShare.xcworkspace" in readme and "iHasApp" in readme,
            "README must document static verification, workspace usage, and iHasApp",
            failures)
    require("repository-relative bridging header" in readme.lower(),
            "README must document the portable bridging-header setting",
            failures)
    require("detector construction failure" in readme.lower(),
            "README must document nil detector construction recovery",
            failures)
    require("completion timeout" in readme.lower() and "late callback" in readme.lower(),
            "README must document bounded detector recovery and late-callback rejection",
            failures)
    normalized_readme = " ".join(readme.split())
    roadmap_evidence = (
        "Historical Platform And Callback Evidence",
        "iOS 8.3 deployment target and Swift 1-era source",
        "broad `canOpenURL:` probing is not viable on current iOS",
        "cleartext `http://itunes.apple.com/lookup` request",
        "success and failure callbacks return to the main queue",
        "stale and duplicate terminal callbacks",
        "does not compile the Swift application or execute XCTest",
    )
    require(all(item in normalized_readme for item in roadmap_evidence),
            "README must preserve historical platform and callback verification evidence",
            failures)
    require("local-only" in readme.lower() and "installed-app" in readme.lower() and "button" in readme.lower() and "main queue" in readme.lower() and "in-progress" in readme.lower() and "completed state" in readme.lower() and "state-specific accessibility" in readme.lower() and "accessibility announcements" in readme.lower() and "detector lifetime" in readme.lower() and "retain cycle" in readme.lower() and "stale callback" in readme.lower(),
            "README must document local-only, user-triggered installed-app detection",
            failures)
    require("scripts/check-baseline.py" in vision and "make lint" in vision and "make test" in vision and "make build" in vision and "pinned macos ci" in vision.lower() and "local-only" in vision.lower() and "main queue" in vision.lower() and "in-progress" in vision.lower() and "completed state" in vision.lower() and "state-specific accessibility" in vision.lower() and "accessibility announcements" in vision.lower() and "detector lifetime" in vision.lower() and "retain cycle" in vision.lower() and "stale callback" in vision.lower(),
            "VISION must describe the current static privacy baseline",
            failures)
    require("repository-relative bridging header" in vision.lower(),
            "VISION must preserve checkout-independent bridge configuration",
            failures)
    require("detector construction failure" in vision.lower(),
            "VISION must preserve detector construction recovery",
            failures)
    require("completion timeout" in vision.lower() and "late callback" in vision.lower(),
            "VISION must preserve bounded detector recovery",
            failures)
    next_priorities_match = re.search(
        r"Next priorities:\n\n(?P<body>.*?)(?:\n\nContribution rules:)",
        vision,
        re.DOTALL,
    )
    next_priorities = next_priorities_match.group("body") if next_priorities_match else ""
    require(next_priorities_match is not None and
            "Modernize Swift and dependency usage in a dedicated pass" in next_priorities and
            "Document iOS version limitations around installed-app detection" not in next_priorities and
            "Add tests or manual checks around success and failure callbacks" not in next_priorities,
            "VISION must retire completed platform and callback roadmap items while retaining modernization",
            failures)
    require("installed-app" in security.lower() and "make check" in security and "github actions" in security.lower() and "completed state" in security.lower() and "state-specific accessibility" in security.lower() and "accessibility announcements" in security.lower() and "retain cycle" in security.lower() and "stale callback" in security.lower(),
            "SECURITY must document installed-app privacy and the static baseline",
            failures)
    require("repository-relative bridging header" in security.lower(),
            "SECURITY must reject machine-local bridge configuration",
            failures)
    require("detector construction failure" in security.lower(),
            "SECURITY must document detector construction recovery",
            failures)
    require("completion timeout" in security.lower() and "late callback" in security.lower(),
            "SECURITY must document timeout cleanup and stale-result protection",
            failures)
    require("debug logging" in changes and "github actions" in changes.lower() and "make check" in changes and "make lint" in changes and "make test" in changes and "make build" in changes and "user-triggered" in changes and "main queue" in changes.lower() and "in-progress" in changes and "completed state" in changes.lower() and "state-specific accessibility" in changes.lower() and "accessibility announcements" in changes.lower() and "detector lifetime" in changes.lower() and "retain cycle" in changes.lower() and "stale callback" in changes.lower(),
            "CHANGES must record the logging cleanup, user-triggered detection, and baseline",
            failures)
    require("repository-relative bridging header" in changes.lower(),
            "CHANGES must record portable bridge configuration",
            failures)
    require("detector construction failure" in changes.lower(),
            "CHANGES must record detector construction recovery",
            failures)
    require("completion timeout" in changes.lower() and "late callback" in changes.lower(),
            "CHANGES must record bounded detector recovery",
            failures)
    require("Reconciled completed platform-limit and callback-verification roadmap items" in changes,
            "CHANGES must record platform and callback roadmap reconciliation",
            failures)
    require("status: completed" in baseline_plan and "status: completed" in explicit_detection_plan and "status: completed" in callback_ui_plan,
            "plans must be marked completed",
            failures)
    require("status: completed" in make_gates_plan,
            "make gate aliases plan must be marked completed",
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
    require("status: completed" in detector_lifetime_plan,
            "detector lifetime plan must be marked completed",
            failures)
    require("status: completed" in accessibility_announcement_plan,
            "detection accessibility announcements plan must be marked completed",
            failures)
    require("status: completed" in callback_retain_cycle_plan,
            "detector callback retain-cycle plan must be marked completed",
            failures)
    require("status: completed" in ci_baseline_plan and "GitHub Actions" in ci_baseline_plan and "make check" in ci_baseline_plan,
            "CI baseline plan must record hosted make check verification",
            failures)
    require("status: completed" in hosted_validation_plan and "make check" in hosted_validation_plan,
            "hosted project validation plan must be completed and document make check",
            failures)
    require("status: completed" in relative_bridge_plan and
            "All four Make gates" in relative_bridge_plan and
            "hostile mutations" in relative_bridge_plan.lower(),
            "relative bridging header plan must record completed status and actual verification",
            failures)
    detector_construction_statuses = re.findall(
        r"^status: .+$", detector_construction_plan, flags=re.MULTILINE
    )
    detector_construction_sections = detector_construction_plan.split(
        "## Verification Completed\n", 1
    )
    detector_construction_verification = (
        detector_construction_sections[1]
        if len(detector_construction_sections) == 2 else ""
    )
    detector_construction_required_evidence = (
        "All four Make gates",
        "`xcodebuild` was",
        "python3 -m py_compile scripts/check-baseline.py",
        "python3 -c",
        "ruby -c Podfile",
        "git diff --check",
        "Five isolated hostile mutations",
    )
    require(detector_construction_statuses == ["status: completed"]
            and all(item in detector_construction_verification
                    for item in detector_construction_required_evidence)
            and re.search(r"\b(?:pending|todo|tbd|not run)\b",
                          detector_construction_verification,
                          re.IGNORECASE) is None,
            "detector construction failure plan must record completed status and actual local verification",
            failures)
    location_statuses = re.findall(r"^status: .+$", location_independent_make_plan, flags=re.MULTILINE)
    location_sections = location_independent_make_plan.split("## Verification Completed\n", 1)
    location_verification = location_sections[1] if len(location_sections) == 2 else ""
    location_required = ("Root and external-directory Make gates passed", "root-derivation mutation failed", "checker-invocation mutation failed", "plan-status mutation failed", "plan-evidence mutation failed", "documentation mutation failed")
    require(location_statuses == ["status: completed"] and all(item in location_verification for item in location_required) and re.search(r"\b(?:pending|todo|tbd|not run)\b", location_verification, re.IGNORECASE) is None,
            "location-independent Make plan must record completed verification", failures)
    all_push_statuses = re.findall(r"^status: .+$", all_push_checks_plan, flags=re.MULTILINE)
    all_push_sections = all_push_checks_plan.split("## Verification Completed\n", 1)
    all_push_verification = all_push_sections[1] if len(all_push_sections) == 2 else ""
    all_push_required = ("All four Make gates", "external-directory Make gate", "Six isolated trigger", "plan-evidence mutations were rejected")
    require(all_push_statuses == ["status: completed"] and all(item in all_push_verification for item in all_push_required) and re.search(r"\b(?:pending|todo|tbd|not run)\b", all_push_verification, re.IGNORECASE) is None,
            "all-push hosted checks plan must record completed verification", failures)
    detector_timeout_statuses = re.findall(r"^status: .+$", detector_timeout_plan, flags=re.MULTILINE)
    detector_timeout_sections = detector_timeout_plan.split("## Verification Completed\n", 1)
    detector_timeout_verification = detector_timeout_sections[1] if len(detector_timeout_sections) == 2 else ""
    detector_timeout_required = (
        "All four Make gates",
        "external-directory Make gate",
        "Seven isolated timeout",
        "direct controller timer targeting",
        "teardown invalidation",
        "plan-evidence mutation",
    )
    require(detector_timeout_statuses == ["status: completed"] and
            all(item in detector_timeout_verification for item in detector_timeout_required) and
            re.search(r"\b(?:pending|todo|tbd|not run)\b", detector_timeout_verification, re.IGNORECASE) is None,
            "detector completion timeout plan must record completed verification",
            failures)
    require("status: completed" in inactive_detection_plan and
            "applicationWillResignActive" in inactive_detection_plan and
            "cancelDetectionForInactiveApp" in inactive_detection_plan and
            "hostile mutations" in inactive_detection_plan.lower(),
            "inactive-app detector cleanup plan must record completed lifecycle verification",
            failures)
    require("status: completed" in hidden_view_detection_plan and
            "viewWillDisappear" in hidden_view_detection_plan and
            "cancelDetectionForInactiveApp" in hidden_view_detection_plan and
            "hostile mutations" in hidden_view_detection_plan.lower(),
            "hidden-view detector cleanup plan must record completed lifecycle verification",
            failures)
    require("status: completed" in memory_warning_detection_plan and
            "didReceiveMemoryWarning" in memory_warning_detection_plan and
            "cancelDetectionForInactiveApp" in memory_warning_detection_plan and
            "hostile mutations" in memory_warning_detection_plan.lower(),
            "memory-warning detector cleanup plan must record completed lifecycle verification",
            failures)
    require("status: completed" in roadmap_reconciliation_plan and
            "Historical Platform And Callback Evidence" in roadmap_reconciliation_plan and
            "hostile documentation mutations" in roadmap_reconciliation_plan.lower() and
            "external working directory" in roadmap_reconciliation_plan,
            "platform and callback roadmap reconciliation plan must record completed verification",
            failures)
    stale_callback_statuses = re.findall(
        r"^status: .+$", stale_callback_plan, flags=re.MULTILINE
    )
    stale_callback_sections = stale_callback_plan.split("## Verification Completed\n", 1)
    stale_callback_verification = (
        stale_callback_sections[1] if len(stale_callback_sections) == 2 else ""
    )
    stale_callback_required_evidence = (
        "All four Make gates",
        "Pull-request run `27394392145`",
        "push run `27394408704`",
        "CodeQL setup run `27402322743`",
        "Mutations removing either the generation comparison",
    )
    require(stale_callback_statuses == ["status: completed"]
            and all(item in stale_callback_verification for item in stale_callback_required_evidence)
            and re.search(r"\b(?:pending|todo|tbd|not run)\b", stale_callback_verification, re.IGNORECASE) is None,
            "stale detector callback plan must record completed status and actual verification",
            failures)
    require("permissions:\n  contents: read" in workflow and
            "cancel-in-progress: true" in workflow and
            "runs-on: macos-15" in workflow and
            "timeout-minutes: 10" in workflow and
            "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10" in workflow and
            "persist-credentials: false" in workflow and
            "run: make check" in workflow,
            "GitHub Actions must keep the bounded, least-privilege macOS project check",
            failures)
    require("on:\n  push:\n  pull_request:" in workflow and
            "branches:" not in workflow,
            "GitHub Actions must run the canonical check for every push and pull request",
            failures)
    require("2026-06-17-all-push-checks.md" in readme and
            "every branch push and pull request" in readme,
            "README must document all-push and pull-request hosted validation",
            failures)
    action_uses = re.findall(r"^\s*uses:\s*(\S+)\s*$", workflow, re.MULTILINE)
    require(action_uses == ["actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10"],
            "GitHub Actions must use only the reviewed pinned checkout action",
            failures)
    require("pull_request_target" not in workflow and not re.search(r"permissions:\s*[\s\S]*?\bwrite\b", workflow),
            "GitHub Actions must not gain privileged pull-request execution or write permissions",
            failures)

    if shutil.which("xcodebuild"):
        result = subprocess.run(
            ["xcodebuild", "-list", "-project", "AppShare.xcodeproj"],
            cwd=str(ROOT),
            stdout=subprocess.DEVNULL,
            check=False,
        )
        require(result.returncode == 0,
                "AppShare.xcodeproj must parse with installed Xcode",
                failures)
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
