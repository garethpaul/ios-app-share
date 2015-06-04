//
//  ViewController.swift
//  AppShare
//
//  Created by Gareth Jones  on 6/4/15.
//  Copyright (c) 2015 gpj. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()

        let detect = iHasApp.new()
       // detect.detectAppDictionariesWithIncremental({ ([AnyObject]!) -> Void in
            // done
        //}
        detect.detectAppDictionariesWithIncremental({ (apps: [AnyObject]!) -> Void in
            //
            println(apps.count)

        }, withSuccess: { ([AnyObject]!) -> Void in
            // List of Apps

        }, withFailure: {(error: NSError!) -> Void in

        })

    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

