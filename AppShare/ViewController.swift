//
//  ViewController.swift
//  AppShare
//
//  Created by Gareth Jones  on 6/4/15.
//  Copyright (c) 2015 gpj. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    private let detectButton = UIButton(type: UIButtonType.System)
    private var detectionInProgress = false
    private var detectionCompleted = false
    private var detectionGeneration = 0
    private var appDetector: iHasApp?

    override func viewDidLoad() {
        super.viewDidLoad()
        self.configureDetectButton()
    }

    private func configureDetectButton() {
        self.detectButton.setTitle("Detect Installed Apps", forState: UIControlState.Normal)
        self.updateDetectButtonAccessibility(
            "Detect Installed Apps",
            hint: "Runs local installed-app detection without sending results",
            announce: false)
        self.detectButton.addTarget(self, action: "detectInstalledApps:", forControlEvents: UIControlEvents.TouchUpInside)
        self.detectButton.translatesAutoresizingMaskIntoConstraints = false
        self.view.addSubview(self.detectButton)

        self.view.addConstraint(NSLayoutConstraint(
            item: self.detectButton,
            attribute: NSLayoutAttribute.CenterX,
            relatedBy: NSLayoutRelation.Equal,
            toItem: self.view,
            attribute: NSLayoutAttribute.CenterX,
            multiplier: 1.0,
            constant: 0.0))
        self.view.addConstraint(NSLayoutConstraint(
            item: self.detectButton,
            attribute: NSLayoutAttribute.CenterY,
            relatedBy: NSLayoutRelation.Equal,
            toItem: self.view,
            attribute: NSLayoutAttribute.CenterY,
            multiplier: 1.0,
            constant: 0.0))
    }

    private func updateDetectButtonAccessibility(label: String, hint: String, announce: Bool) {
        self.detectButton.accessibilityLabel = label
        self.detectButton.accessibilityHint = hint

        if announce {
            UIAccessibilityPostNotification(UIAccessibilityAnnouncementNotification, label)
        }
    }

    private func finishDetection(generation: Int, succeeded: Bool) {
        if generation != self.detectionGeneration || !self.detectionInProgress {
            return
        }

        self.appDetector = nil
        self.detectionInProgress = false

        if succeeded {
            self.detectionCompleted = true
            self.detectButton.enabled = false
            self.detectButton.setTitle("Detection Complete", forState: UIControlState.Disabled)
            self.updateDetectButtonAccessibility(
                "Installed App Detection Complete",
                hint: "Detection completed locally and the button is disabled",
                announce: true)
        }
        else {
            self.detectionCompleted = false
            self.detectButton.enabled = true
            self.detectButton.setTitle("Try Again", forState: UIControlState.Normal)
            self.updateDetectButtonAccessibility(
                "Try App Detection Again",
                hint: "Previous local detection failed; double tap to retry",
                announce: true)
        }
    }

    @IBAction func detectInstalledApps(sender: AnyObject) {
        if self.detectionInProgress || self.detectionCompleted {
            return
        }

        self.detectionInProgress = true
        self.detectionGeneration += 1
        let detectionGeneration = self.detectionGeneration
        self.detectButton.enabled = false
        self.detectButton.setTitle("Detecting...", forState: UIControlState.Disabled)
        self.updateDetectButtonAccessibility(
            "Detecting Installed Apps",
            hint: "Detection is running locally without sending results",
            announce: true)
        let detect = iHasApp.new()
        self.appDetector = detect
        detect.detectAppDictionariesWithIncremental({ (_: [AnyObject]!) -> Void in
            // Detected app data stays local to this sample.
        }, withSuccess: { [weak self] (_: [AnyObject]!) -> Void in
            dispatch_async(dispatch_get_main_queue()) { [weak self] in
                if let strongSelf = self {
                    strongSelf.finishDetection(detectionGeneration, succeeded: true)
                }
            }
        }, withFailure: { [weak self] (_: NSError!) -> Void in
            dispatch_async(dispatch_get_main_queue()) { [weak self] in
                if let strongSelf = self {
                    strongSelf.finishDetection(detectionGeneration, succeeded: false)
                }
            }
        })

    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}
