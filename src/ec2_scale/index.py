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


from __future__ import print_function
import boto3
import json
from collections import OrderedDict 
import time

import os

sqs = boto3.client('sqs')
auto = boto3.client('autoscaling')
s3 = boto3.client('s3')

def new_capacity(autoscaling_group, answer):
    #set desiered capacity in autoscaling group to match messages in queue
    response = auto.set_desired_capacity(
    AutoScalingGroupName=autoscaling_group,
    DesiredCapacity=answer,
    HonorCooldown=False
    )
    return response

def handler(event, _):

    sqs_name = os.getenv('SQSINPUTNAME')
    autoscaling_group = os.getenv('AUTOSCALINGGROUP')
    
    #get number of messages in queue
    sqs_url = sqs.get_queue_url(QueueName=sqs_name)
    response = sqs.get_queue_attributes(
        QueueUrl=sqs_url['QueueUrl'],
        AttributeNames=[
           'ApproximateNumberOfMessages',
        ]
    )
    
    answer = int(response['Attributes']['ApproximateNumberOfMessages'])
    print(answer)
    
    if answer <= 0:
        response = new_capacity(autoscaling_group, answer)
        return response
    else:
        maxsize = auto.describe_auto_scaling_groups(
            AutoScalingGroupNames=[
            autoscaling_group],
            MaxRecords=1
            )
            
        maxsize = maxsize['AutoScalingGroups'][0]['MaxSize']
            
        if answer <= maxsize:
            response = new_capacity(autoscaling_group, answer)
            return response
        else:
            response = new_capacity(autoscaling_group, maxsize)
            return response

    return response