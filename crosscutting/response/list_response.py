from __future__ import absolute_import
from flask import jsonify
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401


class ListResponse:
    """A model class that holds a list response and a total count. The purpose of
       the class is to unify the response returned to the user when querying to
       a particular domain.

        :cvar records: Represents the records held by the response.
        :type List[Any]

        :cvar total_count: The total count of records.
        :type int
    """

    def __init__(self, records=[], total_count=None):
        """ Initializes a new ListResponse.

        :param records: The records held by the response.
        :type List[Any]
        :param total_count: The total count of records.
        :type int
        """
        self._total_count = total_count
        if not len(records):
            self._records = []
        else:
            self._records = records

    @classmethod
    def from_dict(cls, dikt) -> 'ListResponse':
        """Converts this response to a dictionary format.

        :param dikt:
        :return: The dictionary form of the response.
        """
        return util.deserialize_model(dikt, cls)

    # Serves the actual response.
    def serve(self):
        """Serve the models back to the user.

        :return: A response containing the models, including counts.
        :rtype: dict
        """
        response = self.records if self.total_count is None else {
            "records": self.records,
            "total_records": self.total_count
        }

        headers = {} if self.total_count is None else {
            'X-Total-Count': self.total_count
        }

        return serve_response(message="Success.", status=200, data=response, headers=headers)

    @property
    def records(self):
        """Gets the records contained in the response..


        :return: The records held by this response.
        :rtype: List[Any]
        """
        return self._records

    @property
    def total_count(self):
        """Gets the total count contained in the response.

        :return: The total count.
        :rtype: int
        """
        return self._total_count

    @total_count.setter
    def total_count(self, total_count):
        """Sets the total count contained in the response.

        :return:
        """
        self._total_count = total_count

    @records.setter
    def records(self, data):
        """Sets the records of this response.


        :param data: The records of this response.
        :type data: List[Any]
        """
        if data is None:
            raise ValueError("Invalid value for `records`, must not be `None`")  # noqa: E501
        self._records = data


def serve_response(message, status, data=[], headers={}):
    """Sends the response back to the client.

         # noqa: E501

        :param message:
        :type str:

        :param status
        :type int

        :param data
        :type [Any]

        :param headers
        :type dict

        :rtype: None
        """
    response = jsonify({
        "message": message,
        "status": status,
        "data": data
    })
    for i in headers.keys():
        response.headers.set(i, headers[i])
    return response, status
