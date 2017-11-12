import os

from back_me_up.exceptions import InaccessibleFileException


def list_files(folder):
    return os.listdir(folder)


def get_last_modification_date(file_path):
    try:
        return os.path.getmtime(file_path)
    except FileNotFoundError as e:
        raise InaccessibleFileException(file_path, e)
