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
Check job handler
"""

import boto3

SSM = boto3.client('ssm')

PENDING = 'pending'
SUCCESS = 'success'
FAILED = 'failed'

STATUS_MAP = {
    'Pending': PENDING,
    'InProgress': PENDING,
    'Delayed': PENDING,
    'Success': SUCCESS,
    'Cancelled': FAILED,
    'TimedOut': FAILED,
    'Failed': FAILED,
}

def handler(event, _):
    """
    Lambda handler
    """
    try:
        response = SSM.get_command_invocation(
            CommandId=event['CommandId'],
            InstanceId=event['ec2start']['instance_id']
        )

        return STATUS_MAP[str(response['Status'])], response
    except Exception:
        return 'success', 'null'
