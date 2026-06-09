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

    override func viewDidLoad() {
        super.viewDidLoad()
        self.configureDetectButton()
    }

    private func configureDetectButton() {
        self.detectButton.setTitle("Detect Installed Apps", forState: UIControlState.Normal)
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

    @IBAction func detectInstalledApps(sender: AnyObject) {
        if self.detectionInProgress || self.detectionCompleted {
            return
        }

        self.detectionInProgress = true
        self.detectButton.enabled = false
        self.detectButton.setTitle("Detecting...", forState: UIControlState.Disabled)
        let detect = iHasApp.new()
        detect.detectAppDictionariesWithIncremental({ (_: [AnyObject]!) -> Void in
            // Detected app data stays local to this sample.
        }, withSuccess: { (_: [AnyObject]!) -> Void in
            dispatch_async(dispatch_get_main_queue()) {
                self.detectionInProgress = false
                self.detectionCompleted = true
                self.detectButton.enabled = false
                self.detectButton.setTitle("Detection Complete", forState: UIControlState.Disabled)
            }
        }, withFailure: {(_: NSError!) -> Void in
            dispatch_async(dispatch_get_main_queue()) {
                self.detectionInProgress = false
                self.detectButton.enabled = true
                self.detectButton.setTitle("Try Again", forState: UIControlState.Normal)
            }
        })

    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}
