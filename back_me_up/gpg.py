class GPG:
    def __init__(self, gpg_lib, binary=None, homedir=None):
        self.gpg = gpg_lib.GPG(binary=binary, homedir=homedir)

    def encrypt_file(self, file_path, fingerprint):
        with open(file_path, 'rb') as file:
            data = file.read()
            self.gpg.encrypt(data, fingerprint, output=f'{file_path}.gpg')
