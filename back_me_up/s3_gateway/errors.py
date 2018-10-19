class BaseException(Exception):
    def __init__(self, args):
        super().__init__(args)
        self.args = args


class UploadFileError(BaseException):
    pass


class GetMetadataError(BaseException):
    pass
