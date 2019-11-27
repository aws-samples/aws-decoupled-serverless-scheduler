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
import os

sqs = boto3.resource('sqs')
s3 = boto3.client('s3')

def handler(event, _):
    
    for record in event['Records']:
        #read bucket and key of input file and get job_id
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        key_prefix, job_id = os.path.split(key)

        #get parameter store values for default job configuration///////////////////////////////using env varibales atm
        command_type = os.getenv('COMMANDTYPE')   #\\\\\\\\\\\\\\ PowerShell or ShellScript
        retry = os.getenv('RETRY')     # \\\\\\\\\\\\\\\\\\\\\\\\\\ default 1
        job_success_string = os.getenv('JOBSUCCESSSTRING')     # \\\\\\\\\\\\\\\\\\\\\\\\\\ expected name or file type of result file or ''. For linux default 'upload:', for windows default 'files(s) copied' s3 write output'
        ec2_work_directory = os.getenv('EC2WORKINGDIRECTORY')     # \\\\\\\\\\\\\\\\\\\\\\\\\\ for windows needs to use '\\', default that works with user rights on windows - 'C:\\ProgramData\\Amazon\\SSM'

        #prepare the commands to be run on the instance by ssm run command, sync s3 to working directory,run executable, then write results folder back to s3 location
        if 'PowerShell' in command_type:
            ssm_document = 'AWS-RunPowerShellScript'
            command0 = 'cd {}'.format(ec2_work_directory)
            command1 = 'Copy-S3object -Bucket {} -KeyPrefix {} -LocalFolder .\\'.format(bucket, key_prefix)
            command2 = ec2_work_directory + '\\' + job_id
            command3 = 'Remove-Item -Path {} -Force'.format(command2)
            command4 = 'Write-S3object -Bucket {} -KeyPrefix {} -Folder .\\'.format(bucket, key_prefix)
            command5 = 'Remove-Item -Path {}{} -Force'.format(ec2_work_directory, '\\*.*')
            commands =[command0, command1, command2, command3, command4, command5]
        elif 'ShellScript' in command_type:
            ssm_document = 'AWS-RunShellScript'
            command0 = 'mkdir {}; cd {}'.format(ec2_work_directory, ec2_work_directory)
            command1 = 'sudo aws s3 sync s3://{}/{}/ ./'.format(bucket, key_prefix)
            command2 = 'sudo chmod +x ' + ec2_work_directory + '/' + job_id
            command3 = 'sudo ' + ec2_work_directory + '/' + job_id
            command4 = 'sudo aws s3 sync ./ s3://{}/{}/'.format(bucket, key_prefix)
            command5 = 'sudo rm {}{}'.format(ec2_work_directory, '/*.*')
            commands =[command0, command1, command2, command3, command4, command5]
        else:
            return 'unknown document type'

            chmod +x /home/user/bash/backupscript.sh

        #create message for job that goes to SQS
        message = json.dumps({ 'job_id': key, 'retry': retry, 'job_success_string': job_success_string, 'ssm_document': ssm_document, 'commands': commands})
        print(message)

        # Get the queue
        sqs_name = os.getenv('SQSINPUTNAME')
        queue = sqs.get_queue_by_name(QueueName=sqs_name)

        # Send a new job message
        response = queue.send_message(MessageBody=message)
        
    return response
