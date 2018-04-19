from unittest.mock import Mock

import boto3

from back_me_up.s3_gateway.s3_gateway import S3Gateway


class TestS3Client:

    def test_upload_file(self):
        s3_client = Mock(spec=boto3.client('s3'))
        s3_gateway = S3Gateway(client=s3_client)

        s3_gateway.upload('MyBucket', 'some_file.txt')

        s3_client.upload_file.assert_called_once_with(
            'some_file.txt', 'MyBucket', 'some_file.txt'
        )
