# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class AddResponse(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None):  # noqa: E501
        """AddResponse - a model defined in OpenAPI

        :param id: The id of this AddResponse.  # noqa: E501
        :type id: int
        """
        self.openapi_types = {
            'id': int
        }

        self.attribute_map = {
            'id': 'id'
        }

        self.id = id

    @classmethod
    def from_dict(cls, dikt) -> 'AddResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The AddResponse of this AddResponse.  # noqa: E501
        :rtype: AddResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this AddResponse.


        :return: The id of this AddResponse.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this AddResponse.


        :param id: The id of this AddResponse.
        :type id: int
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id