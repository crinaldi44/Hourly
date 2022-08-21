import sqlalchemy.exc
from flask import jsonify
import logging

from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest, UnprocessableEntity, InternalServerError, HTTPException, NotFound
from typing import Any as EndpointResult
from crosscutting.exception.hourly_exception import HourlyException

# Represents an instance of the logger.
logger = logging.getLogger()


# Generates a response dict to a user in a standardized format. If
# fields are not provided, defaults to the name of the error code as
# well as the status name and title.
def handle_validation_error(err: UnprocessableEntity) -> EndpointResult:
    messages = getattr(err, 'data', {}).get('messages')
    if messages:
        data = {
            'error_code': 'webargs_422',
            'messages': messages,
        }
    else:
        data = {
            'error_code': 'some_422',
        }
    return jsonify(data), err.code


def handle_marshmallow_validation_error(err: ValidationError):
    return jsonify({
        "error_code": "err.hourly.BadRequestFormatting",
        "status": 422,
        "detail": list(err.messages.values())[0],
        "suggestion": "Please double-check your spelling and re-attempt your request."
    }), 422


def handle_invalid_request(err: sqlalchemy.exc.InvalidRequestError):
    return jsonify({
        "error_code": "err.hourly.BadRequestFormatting",
        "status": 422,
        "detail": str(err) or "The server encountered an unexpected error. Please try again later.",
        "suggestion": "Please double-check your spelling and re-attempt your request."
    }), 422


def handle_hourly_exception(e: HourlyException) -> EndpointResult:
    return jsonify({
        "error_code": e.err_code,
        "status": e.status[0],
        "detail": e.message if e.message else "",
        "suggestion": e.suggestion or ""
    }), e.status[0]


def handle_notfound_exception(error: NotFound) -> EndpointResult:
    return jsonify({
        "error_code": "err.hourly.NotFound",
        "status": 404,
        "detail": 'The requested resource was not found on the server.',
        "suggestion": "Please re-adjust your request and re-attempt."
    }), 404


def handle_attribute_exception(error: AttributeError) -> EndpointResult:
    logger.exception('Attribute exception: ', exc_info=error)
    return jsonify({
        "error_code": "err.hourly.InternalServerError",
        "status": 500,
        "detail": str(error),
        "suggestion": "Please re-adjust your formatting and re-attempt your request."
    }), 500


def handle_unexpected_exception(error: Exception) -> EndpointResult:
    logger.exception('Unknown exception', exc_info=error)
    return jsonify({
        "error_code": "err.hourly.InternalServerError",
        "status": 500,
        "detail": "The server encountered an unexpected error. Please try again later.",
        "suggestion": "Wait 5 minutes before re-attempting your query and try again."
    }), 500
