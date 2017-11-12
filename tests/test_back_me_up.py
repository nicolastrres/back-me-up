import os
import tempfile
from unittest import mock

import pytest
from hamcrest import assert_that, equal_to

from back_me_up import back_me_up
from back_me_up.exceptions import InaccessibleFileException


def test_should_return_empty_list_when_no_files():
    with tempfile.TemporaryDirectory() as directory:
        actual_files = back_me_up.list_files(directory)

    assert_that([], equal_to(actual_files))


def test_should_return_all_files():
    with tempfile.TemporaryDirectory() as directory:
        with tempfile.NamedTemporaryFile(dir=directory) as file:
            expected_file_name = os.path.basename(file.name)
            actual_files = back_me_up.list_files(directory)

    assert_that([expected_file_name], equal_to(actual_files))


@mock.patch('os.path.getmtime')
def test_should_return_last_modified_date(getmtime_mocked):
    expected_last_modification_date = 1510431915.0
    getmtime_mocked.return_value = expected_last_modification_date

    with tempfile.NamedTemporaryFile() as file:
        last_modified_date = back_me_up.get_last_modification_date(file.name)

    assert_that(expected_last_modification_date, equal_to(last_modified_date))


def test_should_raise_inaccessible_file_when_file_does_not_exist():
    with pytest.raises(InaccessibleFileException) as excinfo:
        back_me_up.get_last_modification_date('non-existent-file.txt')

    assert_that(
        "File non-existent-file.txt does not exist or "
        "is inaccessible at the moment. Error raised: [Errno 2] No "
        "such file or directory: 'non-existent-file.txt'",
        equal_to(str(excinfo.value))
    )
