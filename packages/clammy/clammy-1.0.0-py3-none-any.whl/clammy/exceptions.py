""" Exceptions and errors """


class ClamdError(Exception):
    """Generic Clamd error"""


class ClamdResponseError(ClamdError):
    """Reponse errror"""


class ClamdBufferTooLongError(ClamdResponseError):
    """Class for errors with clamd using INSTREAM with a buffer lenght > StreamMaxLength in /etc/clamav/clamd.conf"""


class ClamdConnectionError(ClamdError):
    """Class for errors communication with clamd"""
