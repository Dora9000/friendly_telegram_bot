class NoCaptionException(BaseException):
    detail = "No caption was found. Generation will not start."


class TooManyRequestsException(BaseException):
    detail = "You have done too many requests. Please wait until some generation will be finished."
