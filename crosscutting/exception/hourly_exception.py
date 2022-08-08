from flask import jsonify
from .errors import err_codes

"""
    Error
        Author:
            chris r

        Description:
            The Error class is a general-purpose class that is intended to uniformly
            handle exceptions at the API level.
"""


class HourlyException(Exception):

    """
        Returns a dict that routes information to the client regarding
        the error that occurred as well as the status and a strategy to
        avoid the error.
    """

    def __init__(self, err_code, message=None, suggestion=None):
        super()
        self.err_code = err_code
        self.status = err_codes[err_code]['status'],
        self.message = message if message else err_codes[err_code]['message']
        self.title = err_codes[err_code]['title']
        self.suggestion = suggestion if suggestion else err_codes[err_code]['suggestion']
        return
