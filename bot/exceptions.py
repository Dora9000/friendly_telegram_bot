class NoCaptionException(BaseException):
    detail = "No caption was found. Generation will not start."


class TooManyRequestsException(BaseException):
    detail = "You have done too many requests. Please wait until some generation will be finished."


class DownloadTimeoutException(BaseException):
    detail = "Image saving timeout."


class DownloadErrorException(BaseException):
    detail = "Image saving error."


class ParamFormatException(BaseException):
    detail = "Invalid parameter format."


class ParamValueException(BaseException):
    detail = "Invalid parameter value."
