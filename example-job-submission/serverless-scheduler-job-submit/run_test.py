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

############## After sending jobs with these parameters you need to start EC2 instance with Windows AMI and add tag it correctly to start statemachine
############## USE THE stack-name-ssm-access-role for EC2 Worker which has the AmazonEC2RoleforSSM policy attached

sqs = boto3.resource('sqs')
ec2 = boto3.resource('ec2')

#Parameters for job sent to SQS
sqs_name = 'serverless-scheduler-job-queue' #job queue for scheduler
job_id = 'Job_Example' #defind job_id
job_success_string = 'Hello' #Define a string that needs to be present in CLI output on instance for job to be succesful
ssm_document = 'AWS-RunPowerShellScript' #defind ssm document type to be run by scheduler via SSM
commands = ['echo Hello World'] #prepare the commands to be run on the instance
retry = 3 #How many retries for the job

#Tagkey for EC2 instance to get state machine assigned
scheduler_cf_stack_name = 'v3-stack-scheduler'

        ###### REST IS AUTOMATED

#Job definition JSON that is sent to SQS job queue
message = json.dumps(
    {
        'job_id': job_id,
        'retry': retry,
        'job_success_string': job_success_string,
        'ssm_document': ssm_document,
        'commands': commands
    }
)
print(message)

# Send a new job to SQS
queue = sqs.get_queue_by_name(QueueName=sqs_name)
response = queue.send_message(MessageBody=message)
print('StatusCode: ' + str(response['ResponseMetadata']['HTTPStatusCode']))

######################################## NOW YOU NEED TO - Start EC2 and add tag it currectly to start statemachine




