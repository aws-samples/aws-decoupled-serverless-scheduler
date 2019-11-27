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
Get job handler
"""

import json
import boto3

SQS = boto3.client("sqs")

def handler(event, _):
    """
    Lambda handler
    """

    queue_url = SQS.get_queue_url(QueueName=event["input"]["sqs_name"])
    print("Queue:", queue_url['QueueUrl'])

    response = SQS.receive_message(
        QueueUrl=queue_url["QueueUrl"],

        AttributeNames=[
            "SentTimestamp"
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            "All"
        ],
        VisibilityTimeout=5,
        WaitTimeSeconds=0,
    )
    print("Response:", json.dumps(response))

    try:
        message = response["Messages"][0]
    except (KeyError, IndexError) as err:
        print("Invalid response:", response)
        raise err

    print("Message:", message)
    return message
