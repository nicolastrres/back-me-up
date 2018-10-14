import boto3
import pytest

from unittest.mock import Mock
from hamcrest import assert_that, equal_to


from back_me_up.s3_gateway.s3_gateway import S3Gateway
from back_me_up.s3_gateway.errors import UploadFileError


class TestS3Client:

    def test_upload_file(self):
        s3_client = Mock(spec=boto3.client('s3'))
        s3_gateway = S3Gateway(client=s3_client)

        s3_gateway.upload('MyBucket', 'some_file.txt')

        s3_client.upload_file.assert_called_once_with(
            'some_file.txt', 'MyBucket', 'some_file.txt'
        )

    def test_raise_error_when_exception(self):
        s3_client = Mock(spec=boto3.client('s3'))
        s3_client.upload_file.side_effect = boto3.exceptions.S3UploadFailedError('Some Error Message')
        s3_gateway = S3Gateway(client=s3_client)

        with pytest.raises(UploadFileError) as error_raised:
            s3_gateway.upload('MyBucket', 'some_file.txt')

        assert_that(error_raised.value.args, equal_to(('Some Error Message',)))
