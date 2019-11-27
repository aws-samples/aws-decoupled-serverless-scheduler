#Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.

#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
#the Software, and to permit persons to whom the Software is furnished to do so.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
#FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
#IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


"""
Wait EC2 handler
"""

import boto3

EC2 = boto3.client("ec2")
EC2_R = boto3.resource("ec2")

def handler(event, _):
    """
    Lambda handler
    """

    instance_id = event["input"]["instance_id"]

    print("Waiting for ec2 instance to boot up...")
    EC2_R.Instance(instance_id).wait_until_running()

    print("Waiting ok status check")
    EC2.get_waiter("instance_status_ok").wait(
        InstanceIds=[instance_id],
        DryRun=False,
        IncludeAllInstances=True
    )

    print("Ready")

    return {
        "instance_id": instance_id,
        "request_id":"null"
    }
