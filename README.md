# sagemaker-defect-detection

A SAR application for batch processing images in Amazon S3 against an Amazon SageMaker model endpoint.


```bash
.
├── README.md                   <-- This instructions file
├── images_to_classify          <-- Sample dataset
├── jupyter-notebook            <-- Jupyter notebook for training and deploying model
├── test-images                 <-- Test images to run against the model
├── src                         <-- Source code for the lambda functions
│   ├── ClassifyImage.py        <-- Lambda function code
│   ├── GetImageInfo.py         <-- Lambda function code
├── template.yaml               <-- SAM Template
```
## Services Deployed

* Two AWS Lambda Functions (Described in the next section)
* An AWS Step function state machine
* An Amazon SQS Queue
* An Amazon SNS topic
* An Amazon SNS email subscription
* A DynamoDB table

## GetImageInfo

This function acts as an entry point to start the Step function state machine. The pre-made S3 bucket passed to this SAM app will need to be configured to notify the SQS queue created on deployment. Any image uploads can trigger the SQS queue which invokes this Lambda function. It extracts the bucket and key of the event and passes it into the start of the state machine.

## ClassifyImage

Receives a JSON message containing the bucket and key of the image to run against the Amazon SageMaker model endpoint. Returns an object containing the bucket, key, confidence score, detected class, and a message string. This gets passed on as input to the state machine in AWS Step Functions.


## Requirements

* AWS CLI already configured with Administrator permission
* [NodeJS 8.10+ installed](https://nodejs.org/en/download/)

## Installation Instructions

1. [Create an AWS account](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html) if you do not already have one and login.
1. Go to the app's page on the [Serverless Application Repository](https://serverlessrepo.aws.amazon.com/applications/) and click "Deploy"
1. Provide the required app parameters (see parameter details below) and click "Deploy"

## Parameter Details

* ModelEndpointName: (Required) Provide the name of the Amazon SageMaker model endpoint.
* EmailAddress: (Required) The email address to notify on detected defect.
* BucketName: The name of the bucket where your images will be added.

## Using this Application

* Create an Amazon SageMaker notebook instance.
* Prepare and upload an image dataset to an Amazon S3 bucket.
* Use the sample Jupyter notebook with the SageMaker notebook instance to train and deploy a custom image classification.
* Create an S3 bucket for processing images.
* Deploy this SAR application.
* Create an S3 bucket notification on the SQS queue.
* Upload a test image to S3 for classification.


==============================================

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
