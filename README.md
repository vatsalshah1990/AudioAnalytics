# Audio Analytics Serverless Pipeline

## AWS Services Used
* EventBridge
* S3
* CloudTrail
* Lambda
* Transcribe
* Comprehend

## Pre-requisites
1. [Docker installation on the host](https://docs.docker.com/get-docker/)

## Quick Start
1. [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
2. [Install SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
3. Create a custom vocabulary from Transcribe console using S3 path for table file. This name should be later passed into the parameters in the next step.
4. Run the following commands to build and deploy your application
    ```
    sam build --use-container
    sam deploy --guided # Only first time
    sam deploy # Next time onwards
    ```
5. Run the above commands everytime you change any functions or template.yaml.
6. Start pushing audio files in .wav format to the audifiles bucket. Your results will be published to the transribe bucket.

Note: Bucket name & other parameters are defined during first deploy using the --guided flag on sam deploy. You can use the same command to redefine any parameters.

