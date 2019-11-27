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
Final terminate handler
"""

import boto3
from botocore.exceptions import ClientError

AS = boto3.client("autoscaling")
EC2 = boto3.client("ec2")

SUCCESS = "instance termination call was made"
FAILURE = "termination call not made"

def handler(event, _):
    """
    Lambda handler
    """

    instance_id = event["input"]["instance_id"]

    try:
        AS.terminate_instance_in_auto_scaling_group(
            InstanceId=instance_id,
            ShouldDecrementDesiredCapacity=True
        )
        return "asg instance termination call made"
    except ClientError:
        pass

    try:
        EC2.terminate_instances(
            InstanceIds=(instance_id,),
            DryRun=False
        )
        return SUCCESS
    except ClientError:
        return FAILURE
