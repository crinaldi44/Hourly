# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class ErrorListResponse(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, errors=None):  # noqa: E501
        """ErrorListResponse - a model defined in OpenAPI

        :param errors: The errors of this ErrorListResponse.  # noqa: E501
        :type errors: List[object]
        """
        self.openapi_types = {
            'errors': List[object]
        }

        self.attribute_map = {
            'errors': 'errors'
        }

        self.errors = errors

    @classmethod
    def from_dict(cls, dikt) -> 'ErrorListResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ErrorListResponse of this ErrorListResponse.  # noqa: E501
        :rtype: ErrorListResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def errors(self):
        """Gets the errors of this ErrorListResponse.

        List of all error messages.  # noqa: E501

        :return: The errors of this ErrorListResponse.
        :rtype: List[object]
        """
        return self._errors

    @errors.setter
    def errors(self, errors):
        """Sets the errors of this ErrorListResponse.

        List of all error messages.  # noqa: E501

        :param errors: The errors of this ErrorListResponse.
        :type errors: List[object]
        """
        if errors is None:
            raise ValueError("Invalid value for `errors`, must not be `None`")  # noqa: E501

        self._errors = errors
