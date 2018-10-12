import os
from unittest.mock import Mock

import pytest
from hamcrest import assert_that, equal_to, has_length

from back_me_up import Directory


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
