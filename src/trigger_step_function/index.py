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


import boto3
import os
import sys
import json
from collections import OrderedDict 

sf_client = boto3.client('stepfunctions')
ec2_client = boto3.client('ec2')
ec2_r = boto3.resource('ec2')

def handler(event, context):
    print(event)
    instance_id = event['detail']['instance-id']
    print(instance_id)

    # When given an instance ID as str e.g. 'i-1234567', return the value for 'scheduler_queue'
    ec2instance = ec2_r.Instance(instance_id)
    queue_name = 'nothing'
    autoscaling_group = 'nothing'
    for tags in ec2instance.tags:
        print(tags)
        if os.getenv('TAGKEY') in tags["Key"]:
            queue_name = tags["Value"]
        if 'aws:autoscaling:groupName' in tags["Key"]:
            autoscaling_group = tags["Value"]
    
    if 'nothing' in queue_name:
        print('did not start sf')
        return "Not tagged for scheduler"
    
    print(queue_name)
    
    #Get config from json file in S3    
    timeout_Job = os.getenv('TIMEOUTJOB')
    region = os.getenv('REGION')
    state_machine_name = os.getenv('STATEMACHINENAME')
    state_machine_arn = os.getenv('STATEMACHINEARN')
    sqs_name = queue_name
    sqs_name_out = queue_name + '-finished'
    sqs_name_failed = queue_name + '-failed'
    table = os.getenv('TABLENAME')

    #json input parameter payload for step functions workflow
    input = {"input" : {"sqs_name": sqs_name,
    "sqs_name_out": sqs_name_out,
    "sqs_name_failed": sqs_name_failed,
    "region": region,
    "state_machine_arn": state_machine_arn,
    "state_machine_name": state_machine_name,
    "Timeout_Job": timeout_Job,
    "instance_id": instance_id,
    "autoscaling_group": autoscaling_group,
    "table": table
    }}
    
    #start step functions wrapped workflow for instance   
    response = sf_client.start_execution(
    stateMachineArn=state_machine_arn,
    input = json.dumps(input))
    print(response)

    