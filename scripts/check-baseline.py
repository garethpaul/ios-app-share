#!/usr/bin/env python3
from pathlib import Path
import plistlib
import re
import shutil
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/plans/2026-06-08-ios-app-detection-baseline.md"


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def strip_swift_line_comments(text):
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


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
    plan = PLAN.read_text(encoding="utf-8") if PLAN.exists() else ""

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
    require("detectAppDictionariesWithIncremental" in active_view_controller,
            "ViewController must retain the app-detection sample flow",
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
    require("local-only" in readme.lower() and "installed-app" in readme.lower(),
            "README must document local-only installed-app detection",
            failures)
    require("scripts/check-baseline.py" in vision and "local-only" in vision.lower(),
            "VISION must describe the current static privacy baseline",
            failures)
    require("installed-app" in security.lower() and "make check" in security,
            "SECURITY must document installed-app privacy and the static baseline",
            failures)
    require("debug logging" in changes and "make check" in changes,
            "CHANGES must record the logging cleanup and baseline",
            failures)
    require("status: completed" in plan,
            "plan must be marked completed",
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
