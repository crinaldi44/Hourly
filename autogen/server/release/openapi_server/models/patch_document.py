# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class PatchDocument(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, op=None, path=None, value=None, from_path=None):  # noqa: E501
        """PatchDocument - a model defined in OpenAPI

        :param op: The op of this PatchDocument.  # noqa: E501
        :type op: str
        :param path: The path of this PatchDocument.  # noqa: E501
        :type path: str
        :param value: The value of this PatchDocument.  # noqa: E501
        :type value: str
        :param from_path: The from_path of this PatchDocument.  # noqa: E501
        :type from_path: str
        """
        self.openapi_types = {
            'op': str,
            'path': str,
            'value': str,
            'from_path': str
        }

        self.attribute_map = {
            'op': 'op',
            'path': 'path',
            'value': 'value',
            'from_path': 'fromPath'
        }

        self.op = op
        self.path = path
        self.value = value
        self.from_path = from_path

    @classmethod
    def from_dict(cls, dikt) -> 'PatchDocument':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PatchDocument of this PatchDocument.  # noqa: E501
        :rtype: PatchDocument
        """
        return util.deserialize_model(dikt, cls)

    @property
    def op(self):
        """Gets the op of this PatchDocument.

        The operation to be performed  # noqa: E501

        :return: The op of this PatchDocument.
        :rtype: str
        """
        return self._op

    @op.setter
    def op(self, op):
        """Sets the op of this PatchDocument.

        The operation to be performed  # noqa: E501

        :param op: The op of this PatchDocument.
        :type op: str
        """
        allowed_values = ["add", "remove", "replace", "move", "copy", "test"]  # noqa: E501
        if op not in allowed_values:
            raise ValueError(
                "Invalid value for `op` ({0}), must be one of {1}"
                .format(op, allowed_values)
            )

        self._op = op

    @property
    def path(self):
        """Gets the path of this PatchDocument.

        A JSON-Pointer  # noqa: E501

        :return: The path of this PatchDocument.
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this PatchDocument.

        A JSON-Pointer  # noqa: E501

        :param path: The path of this PatchDocument.
        :type path: str
        """
        if path is None:
            raise ValueError("Invalid value for `path`, must not be `None`")  # noqa: E501

        self._path = path

    @property
    def value(self):
        """Gets the value of this PatchDocument.

        The value to be used within the operations.  # noqa: E501

        :return: The value of this PatchDocument.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this PatchDocument.

        The value to be used within the operations.  # noqa: E501

        :param value: The value of this PatchDocument.
        :type value: str
        """

        self._value = value

    @property
    def from_path(self):
        """Gets the from_path of this PatchDocument.

        A string containing a JSON Pointer value.  # noqa: E501

        :return: The from_path of this PatchDocument.
        :rtype: str
        """
        return self._from_path

    @from_path.setter
    def from_path(self, from_path):
        """Sets the from_path of this PatchDocument.

        A string containing a JSON Pointer value.  # noqa: E501

        :param from_path: The from_path of this PatchDocument.
        :type from_path: str
        """

        self._from_path = from_path
