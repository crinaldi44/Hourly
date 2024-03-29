# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.clockin import Clockin
from openapi_server import util

from openapi_server.models.clockin import Clockin  # noqa: E501

class ClockinListResponse(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, clockins=None):  # noqa: E501
        """ClockinListResponse - a model defined in OpenAPI

        :param clockins: The clockins of this ClockinListResponse.  # noqa: E501
        :type clockins: List[Clockin]
        """
        self.openapi_types = {
            'clockins': List[Clockin]
        }

        self.attribute_map = {
            'clockins': 'clockins'
        }

        self.clockins = clockins

    @classmethod
    def from_dict(cls, dikt) -> 'ClockinListResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ClockinListResponse of this ClockinListResponse.  # noqa: E501
        :rtype: ClockinListResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def clockins(self):
        """Gets the clockins of this ClockinListResponse.


        :return: The clockins of this ClockinListResponse.
        :rtype: List[Clockin]
        """
        return self._clockins

    @clockins.setter
    def clockins(self, clockins):
        """Sets the clockins of this ClockinListResponse.


        :param clockins: The clockins of this ClockinListResponse.
        :type clockins: List[Clockin]
        """

        self._clockins = clockins
