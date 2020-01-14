  # Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
  # Permission is hereby granted, free of charge, to any person obtaining a copy of this
  # software and associated documentation files (the "Software"), to deal in the Software
  # without restriction, including without limitation the rights to use, copy, modify,
  # merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
  # permit persons to whom the Software is furnished to do so.
  # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
  # INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
  # PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  # HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
  # OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
  # SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import os
import io
import boto3
import json

ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime= boto3.client('runtime.sagemaker')
s3 = boto3.client('s3')

def lambda_handler(event, context):

    # Extract upload event key and bucket
    key = event['key']
    bucket = event['bucket']

    # Fetch image data from S3
    data = s3.get_object(Bucket= bucket, Key= key)
    imageData = data['Body'].read()

    # Invoke Amazon SageMaker model endpoint
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='application/x-image',
                                       Body=imageData)

    result = json.loads(response['Body'].read().decode())

    # Prepare state data
    detected_class = "defect_free" if result[0] > result[1] else "defective"
    score = result[0] if detected_class == "defect_free" else result[1]
    score = str(score)

    message = "File: " + bucket + "/" + key + "\nScore: " + score

    return {
        "score": score,
        "detected_class": detected_class,
        "key": key,
        "bucket": bucket,
        "message": message
    }
