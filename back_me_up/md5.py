import hashlib


def calculate_md5(path):
    hash = ''
    with open(path, 'rb') as file:
        hash = hashlib.md5(file.read()).hexdigest()

    return hash
