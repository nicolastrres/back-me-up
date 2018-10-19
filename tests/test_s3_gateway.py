import boto3
import botocore
import pytest

from unittest.mock import Mock
from hamcrest import assert_that, equal_to


from back_me_up.s3_gateway.s3_gateway import S3Gateway
from back_me_up.s3_gateway.errors import UploadFileError, GetMetadataError


class TestS3Client:

    def test_upload_file(self):
        s3_client = Mock(spec=boto3.client('s3'))
        s3_gateway = S3Gateway(client=s3_client)

        s3_gateway.upload('MyBucket', 'some_file.txt')

        s3_client.upload_file.assert_called_once_with(
            'some_file.txt', 'MyBucket', 'some_file.txt', ExtraArgs={'Metadata': {}}
        )

    def test_raise_error_when_exception(self):
        s3_client = Mock(spec=boto3.client('s3'))
        s3_client.upload_file.side_effect = boto3.exceptions.S3UploadFailedError('Some Error Message')
        s3_gateway = S3Gateway(client=s3_client)

        with pytest.raises(UploadFileError) as error_raised:
            s3_gateway.upload('MyBucket', 'some_file.txt')

        assert_that(error_raised.value.args, equal_to(('Some Error Message',)))

    def test_upload_file_should_pass_metadata(self):
        s3_client = Mock(spec=boto3.client('s3'))
        s3_gateway = S3Gateway(client=s3_client)

        s3_gateway.upload('MyBucket', 'some_file.txt', metadata={'some_arg': 'some-value'})

        s3_client.upload_file.assert_called_once_with(
            'some_file.txt', 'MyBucket', 'some_file.txt', ExtraArgs={'Metadata': {'some_arg': 'some-value'}}
        )

    def test_get_md5_metadata(self):
        s3_client = Mock(spec=boto3.client('s3'))
        s3_client.head_object.return_value = {'ResponseMetadata': {'HTTPHeaders': {'x-amz-meta-md5': 'some md5 hash'}}}

        s3_gateway = S3Gateway(client=s3_client)

        md5_hash = s3_gateway.get_md5_metadata('MyBucket', 'some_file.txt')

        assert_that(md5_hash, equal_to('some md5 hash'))

    def test_get_md5_metadata_should_return_raise_right_exception_when_error(self):
        s3_client = Mock(spec=boto3.client('s3'))
        s3_client.head_object.side_effect = botocore.exceptions.ClientError(
            {'Error': {'Code': 'ExpiredToken', 'Message': 'Some Error Happened.'}},
            'HeadObject'
        )

        s3_gateway = S3Gateway(client=s3_client)

        with pytest.raises(GetMetadataError) as error_raised:
            s3_gateway.get_md5_metadata('MyBucket', 'some_file.txt')

        assert_that(
            error_raised.value.args,
            equal_to(('An error occurred (ExpiredToken) when calling the '
                      'HeadObject operation: Some Error Happened.',))
        )
