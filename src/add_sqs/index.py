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
Add SQS handler
"""

import json
import boto3

SQS = boto3.resource('sqs')

def handler(event, _):
    """
    Lambda handler
    """

    if int(event['job_details']['retry']) <= int(event['job_details']['re_run']):
        return 'NoRetries'

    event['job_details']['re_run'] = int(event['job_details']['re_run']) + 1

    #create message for job that goes to SQS
    message = json.dumps(event['job_details'])
    print("Message:", message)

    # Get the queue
    queue = SQS.get_queue_by_name(QueueName=event['input']['sqs_name'])
    print("Queue:", queue)

    # Create a new message
    response = queue.send_message(MessageBody=message)
    message_id = response['ResponseMetadata']['RequestId']
    print("Message ID:", message_id)

    return message_id
