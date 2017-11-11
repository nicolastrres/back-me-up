import os


def list_files(folder):
    return os.listdir(folder)


def get_last_modification_date(file):
    return os.path.getmtime(file)
