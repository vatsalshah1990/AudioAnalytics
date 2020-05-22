"""
Submit audio files to Comprehend
"""
import boto3
from botocore.exceptions import ClientError
import os
import logging

logger = logging.getLogger()
level = logging.getLevelName(os.getenv('LOG_LEVEL', 'DEBUG'))
logger.setLevel(level)

def lambda_handler(event, context):
    logger.info("Starting transcribe job")
    logger.debug(event)
    client = boto3.client('transcribe')
    bucket_name = event["detail"]["requestParameters"]["bucketName"]
    object_key = event["detail"]["requestParameters"]["key"]
    transcription_job_name = bucket_name + "_" + object_key.split(".", 1)[0]
    media_file_uri = "s3://{bucket_name}/{object_key}".format(bucket_name=bucket_name, object_key=object_key)
    logger.debug(media_file_uri)
    output_bucket_name = os.environ["OUTPUT_BUCKET_NAME"]
    vocabulary_name = os.environ["TRANSCRIBE_CUSTOM_VOCABULARY"]
    transcribe_data_access_role = os.environ["TRANSCRIBE_DATA_ACCESS_ROLE_ARN"]
    transcribe_deferred_execution = os.environ["TRANSCRIBE_DEFERRED_EXECUTION"]
    logger.info("Deferred execution: {}".format(transcribe_deferred_execution))
    args = {
        "TranscriptionJobName": transcription_job_name,
        "LanguageCode": 'hi-IN',
        "MediaFormat": 'wav',
        "Media": {
            'MediaFileUri': media_file_uri
        },
        "OutputBucketName": output_bucket_name,
        "Settings": {
            'VocabularyName': vocabulary_name,
            'ChannelIdentification': True,
            'ShowAlternatives': False
        }
    }
    if transcribe_deferred_execution == "True":
        logger.debug("Adding deferred execution settings on transcribe")
        args["JobExecutionSettings"] = {
            'AllowDeferredExecution': True,
            'DataAccessRoleArn': transcribe_data_access_role
        }
    response = client.start_transcription_job(**args)
    logger.debug(response)
    logger.info("Created transcribe job")