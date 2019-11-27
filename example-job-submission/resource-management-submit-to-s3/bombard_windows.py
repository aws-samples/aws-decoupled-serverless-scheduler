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
import datetime

s3_r = boto3.resource('s3')
now = datetime.datetime.now().strftime("%y-%m-%d")

#This script sends new jobs to scheduler by uploading the job input files and executable file to s3 bucket
#A unique S3 directory should be used for each job to specify what files need to be copied to working directory on EC2 instance store
#An S3 event will need to exist to trigger S3Trigger.py Lambda on executable file suffix, in this case ".bat".
#Output files from jobs will be copied back to this directory from the EC2 working directory

bucket = 'my-resource-management-drop-job-files' #enter name of your s3 bucket for jobs

for i in range(0, 1000, 1): #The number of loops defines how many test jobs to send
    
    jobid = 'jobId_' + str(i)
    key = 'jobs/' + now + '/' + jobid + '/' + jobid + '.input'

    #send input file to s3 YOU CAN USE ANY FILE HERE AS EXECUTABLE WILL JUST RENAME IT, SEE EXECUATBLE BELOW
    s3_r.meta.client.upload_file(Filename='./example-job-submission/resource-management-submit-to-s3/example_file.input', Bucket=bucket, Key=key) 

    #S3 Trigger should be set to ".bat" to trigger from executable file key below
    key = 'jobs/' + now + '/' + jobid + '/' + jobid + '.bat' ####### .bat
    #Here I specify what to put in executable .bat file and create it dynamically in code but i could reference an existing static executable file
    content = "copy C:\ProgramData\Amazon\SSM\{}.input C:\ProgramData\Amazon\SSM\{}.output".format(jobid, jobid)
    #send executable file to s3 triggering a new job, results will end up back in this S3 directory, monitor progress in DynamoDB
    s3_r.Object(bucket, key).put(Body=content)
    print(key+ '   -----   ' + content)
    
