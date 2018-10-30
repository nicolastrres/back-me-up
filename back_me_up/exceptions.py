class BaseException(Exception):
    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def __str__(self):
        if self.message:
            return self.message
        return self


class UploadFileError(BaseException):
    pass


class GetMetadataError(BaseException):
    pass


class GPGKeyNotFound(BaseException):
    def __init__(self, email):
        super().__init__(email)
        self.message = f'GPG key associated with email {email} was not found'
