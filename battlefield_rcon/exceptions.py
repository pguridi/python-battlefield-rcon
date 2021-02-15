class RCONException(Exception):
    pass


class RCONAuthException(RCONException):
    pass


class RCONLoginRequiredException(RCONException):
    pass
