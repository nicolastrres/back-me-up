import os
from unittest.mock import Mock

import pytest
from hamcrest import assert_that, equal_to, has_length

from back_me_up.back_me_up import Directory, BackmeUp
from back_me_up.s3_gateway.s3_gateway import S3Gateway

@pytest.fixture
def directory_handler():
    return Mock(spec=os)


class TestDirectory:
    def test_should_return_empty_list_when_no_entries(
            self, directory_handler
    ):
        directory_handler.listdir.return_value = []

        directory = Directory('/', directory_handler)

        assert_that(directory.entries, equal_to([]))

    def test_should_return_all_entries(self, directory_handler):
        directory_handler.listdir.return_value = ['file1', 'file2']

        directory = Directory('/', directory_handler)

        assert_that(directory.entries, has_length(2))
        assert_that(directory.entries[0].path, equal_to('file1'))
        assert_that(directory.entries[1].path, equal_to('file2'))


class TestBackmeUp:
    def test_should_upload_file_to_bucket(self):
        s3_gateway = Mock(spec=S3Gateway)

        back_me_up = BackmeUp(s3_gateway)

        back_me_up.sync('my bucket', 'some file')

        s3_gateway.upload.assert_called_once_with('my bucket', 'some file')
