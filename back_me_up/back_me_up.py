import os

from back_me_up.exceptions import InaccessibleFileException


def list_files(folder):
    return os.listdir(folder)


def get_last_modification_date(file_path):
    try:
        return os.path.getmtime(file_path)
    except FileNotFoundError as e:
        raise InaccessibleFileException(file_path, e)


def store_file_last_modification_data(
        status_file_path,
        backup_file_name,
        last_modification_date
):
    with open(status_file_path, 'w') as status_file:
        status_file.write(
            '%s %s' % (backup_file_name, last_modification_date)
        )
