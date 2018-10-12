import boto3
from .errors import UploadFileError


class S3Gateway:
    def __init__(self, client):
        self.client = client

    def upload(self, bucket_name, file_path):
        try:
            self.client.upload_file(file_path, bucket_name, file_path)
        except Exception as error:
            raise UploadFileError(error.args)


def create():
    s3_client = boto3.client('s3')
    return S3Gateway(s3_client)
