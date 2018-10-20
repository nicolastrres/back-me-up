import boto3
from .errors import UploadFileError, GetMetadataError


class S3Gateway:
    def __init__(self, client):
        self.client = client

    def upload(self, bucket_name, file_path, metadata=None):
        metadata = metadata or {}
        try:
            self.client.upload_file(file_path, bucket_name, file_path, ExtraArgs={'Metadata': metadata})
        except Exception as error:
            raise UploadFileError(error.args)

    def get_md5_metadata(self, bucket_name, file_path):
        try:
            return self.client.head_object(
                Bucket=bucket_name,
                Key=file_path
            )['ResponseMetadata']['HTTPHeaders']['x-amz-meta-md5']
        except KeyError:
            return None
        except Exception as error:
            if error.response['Error']['Code'] == '404':
                return None
            raise GetMetadataError(error.args)


def create():
    s3_client = boto3.client('s3')
    return S3Gateway(s3_client)
