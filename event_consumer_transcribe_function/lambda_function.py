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

def parse_arn(arn):
    # http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html
    elements = arn.split(':', 5)
    result = {
        'arn': elements[0],
        'partition': elements[1],
        'service': elements[2],
        'region': elements[3],
        'account': elements[4],
        'resource': elements[5],
        'resource_type': None
    }
    if '/' in result['resource']:
        result['resource_type'], result['resource'] = result['resource'].split('/',1)
    elif ':' in result['resource']:
        result['resource_type'], result['resource'] = result['resource'].split(':',1)
    return result

def lambda_handler(event, context):
    logger.info("Starting transcribe job")
    logger.debug(event)
    client = boto3.client('transcribe')
    for obj in event["detail"]["resources"]:
        if obj["type"] == "AWS::S3::Object":
            object_arn = obj["ARN"]
    logger.info(object_arn)
    parsed_arn = parse_arn(object_arn)
    logger.debug(parsed_arn)
    transcription_job_name = parsed_arn["resource_type"] + "_" + parsed_arn["resource"].split(".", 1)[0]
    media_file_uri = "s3://{bucket_name}/{object_key}".format(bucket_name=parsed_arn["resource_type"], object_key=parsed_arn["resource"])
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