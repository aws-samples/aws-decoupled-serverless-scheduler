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
DynamoDB Handler
"""

import boto3

DDB = boto3.client("dynamodb")

def handler(event, _):
    """
    Lambda handler
    """

    event_input = event["input"]
    job_details = event["job_details"]

    try:
        job_output = str(event["jobstatus"][1]["StandardOutputContent"])
    except (IndexError, KeyError):
        job_output = "null"

    return DDB.put_item(
        TableName=event_input["table"],
        Item={
            "job_id": {
                "S": job_details["job_id"],
            },
            "Status": {
                "S": event["status"],
            },
            "Retries": {
                "S": "{} of {}".format(job_details["re_run"], job_details["retry"]),
            },
            "SSM_Document": {
                "S": job_details["ssm_document"],
            },
            "Commands": {
                "S": str(job_details["commands"]),
            },
            "Output_Logs": {
                "S": job_output,
            },
            "instance_id": {
                "S": event_input["instance_id"],
            }
        }
    )
