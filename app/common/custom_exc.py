from setting import settings


class TokenAuthError(Exception):
    def __init__(self, err_desc: str = "User Authentication Failed"):
        self.err_desc = err_desc


class TokenExpired(Exception):
    def __init__(self, err_desc: str = "Token has expired"):
        self.err_desc = err_desc


class AuthenticationError(Exception):
    def __init__(self, err_desc: str = "Permission denied"):
        self.err_desc = err_desc


class LocalEpisodeNameError(Exception):
    def __init__(self, err_desc: str = "Local episode name is not number."):
        self.err_desc = err_desc


class LocalVideoTitleError(Exception):
    def __init__(self, err_desc: str = "Local video title doesn't has %s." % settings.VIDEO_NAME_SEPARATOR):
        self.err_desc = err_desc
