# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.package_question import PackageQuestion
from openapi_server import util

from openapi_server.models.package_question import PackageQuestion  # noqa: E501

class Event(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, name=None, description=None, agreed_price=None, start_datetime=None, end_datetime=None, package_id=None, company_id=None, employee_id=None, questions=None):  # noqa: E501
        """Event - a model defined in OpenAPI

        :param id: The id of this Event.  # noqa: E501
        :type id: int
        :param name: The name of this Event.  # noqa: E501
        :type name: str
        :param description: The description of this Event.  # noqa: E501
        :type description: str
        :param agreed_price: The agreed_price of this Event.  # noqa: E501
        :type agreed_price: float
        :param start_datetime: The start_datetime of this Event.  # noqa: E501
        :type start_datetime: str
        :param end_datetime: The end_datetime of this Event.  # noqa: E501
        :type end_datetime: str
        :param package_id: The package_id of this Event.  # noqa: E501
        :type package_id: int
        :param company_id: The company_id of this Event.  # noqa: E501
        :type company_id: int
        :param employee_id: The employee_id of this Event.  # noqa: E501
        :type employee_id: int
        :param questions: The questions of this Event.  # noqa: E501
        :type questions: List[PackageQuestion]
        """
        self.openapi_types = {
            'id': int,
            'name': str,
            'description': str,
            'agreed_price': float,
            'start_datetime': str,
            'end_datetime': str,
            'package_id': int,
            'company_id': int,
            'employee_id': int,
            'questions': List[PackageQuestion]
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'description': 'description',
            'agreed_price': 'agreed_price',
            'start_datetime': 'start_datetime',
            'end_datetime': 'end_datetime',
            'package_id': 'package_id',
            'company_id': 'company_id',
            'employee_id': 'employee_id',
            'questions': 'questions'
        }

        self.id = id
        self.name = name
        self.description = description
        self.agreed_price = agreed_price
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.package_id = package_id
        self.company_id = company_id
        self.employee_id = employee_id
        self.questions = questions

    @classmethod
    def from_dict(cls, dikt) -> 'Event':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Event of this Event.  # noqa: E501
        :rtype: Event
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Event.

        The identifier for the event.  # noqa: E501

        :return: The id of this Event.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Event.

        The identifier for the event.  # noqa: E501

        :param id: The id of this Event.
        :type id: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Event.

        name  # noqa: E501

        :return: The name of this Event.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Event.

        name  # noqa: E501

        :param name: The name of this Event.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this Event.

        Block of text describing the event.  # noqa: E501

        :return: The description of this Event.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Event.

        Block of text describing the event.  # noqa: E501

        :param description: The description of this Event.
        :type description: str
        """
        if description is None:
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501

        self._description = description

    @property
    def agreed_price(self):
        """Gets the agreed_price of this Event.

        The agreed upon price.  # noqa: E501

        :return: The agreed_price of this Event.
        :rtype: float
        """
        return self._agreed_price

    @agreed_price.setter
    def agreed_price(self, agreed_price):
        """Sets the agreed_price of this Event.

        The agreed upon price.  # noqa: E501

        :param agreed_price: The agreed_price of this Event.
        :type agreed_price: float
        """
        if agreed_price is None:
            raise ValueError("Invalid value for `agreed_price`, must not be `None`")  # noqa: E501

        self._agreed_price = agreed_price

    @property
    def start_datetime(self):
        """Gets the start_datetime of this Event.

        The start datetime.  # noqa: E501

        :return: The start_datetime of this Event.
        :rtype: str
        """
        return self._start_datetime

    @start_datetime.setter
    def start_datetime(self, start_datetime):
        """Sets the start_datetime of this Event.

        The start datetime.  # noqa: E501

        :param start_datetime: The start_datetime of this Event.
        :type start_datetime: str
        """
        if start_datetime is None:
            raise ValueError("Invalid value for `start_datetime`, must not be `None`")  # noqa: E501

        self._start_datetime = start_datetime

    @property
    def end_datetime(self):
        """Gets the end_datetime of this Event.

        The end datetime.  # noqa: E501

        :return: The end_datetime of this Event.
        :rtype: str
        """
        return self._end_datetime

    @end_datetime.setter
    def end_datetime(self, end_datetime):
        """Sets the end_datetime of this Event.

        The end datetime.  # noqa: E501

        :param end_datetime: The end_datetime of this Event.
        :type end_datetime: str
        """

        self._end_datetime = end_datetime

    @property
    def package_id(self):
        """Gets the package_id of this Event.

        The ID of the package associated with this event.  # noqa: E501

        :return: The package_id of this Event.
        :rtype: int
        """
        return self._package_id

    @package_id.setter
    def package_id(self, package_id):
        """Sets the package_id of this Event.

        The ID of the package associated with this event.  # noqa: E501

        :param package_id: The package_id of this Event.
        :type package_id: int
        """
        if package_id is None:
            raise ValueError("Invalid value for `package_id`, must not be `None`")  # noqa: E501

        self._package_id = package_id

    @property
    def company_id(self):
        """Gets the company_id of this Event.

        The ID of the company associated to the event.  # noqa: E501

        :return: The company_id of this Event.
        :rtype: int
        """
        return self._company_id

    @company_id.setter
    def company_id(self, company_id):
        """Sets the company_id of this Event.

        The ID of the company associated to the event.  # noqa: E501

        :param company_id: The company_id of this Event.
        :type company_id: int
        """

        self._company_id = company_id

    @property
    def employee_id(self):
        """Gets the employee_id of this Event.

        The ID of the employee servicing the event.  # noqa: E501

        :return: The employee_id of this Event.
        :rtype: int
        """
        return self._employee_id

    @employee_id.setter
    def employee_id(self, employee_id):
        """Sets the employee_id of this Event.

        The ID of the employee servicing the event.  # noqa: E501

        :param employee_id: The employee_id of this Event.
        :type employee_id: int
        """

        self._employee_id = employee_id

    @property
    def questions(self):
        """Gets the questions of this Event.

        The questions to include in the event form.  # noqa: E501

        :return: The questions of this Event.
        :rtype: List[PackageQuestion]
        """
        return self._questions

    @questions.setter
    def questions(self, questions):
        """Sets the questions of this Event.

        The questions to include in the event form.  # noqa: E501

        :param questions: The questions of this Event.
        :type questions: List[PackageQuestion]
        """
        if questions is None:
            raise ValueError("Invalid value for `questions`, must not be `None`")  # noqa: E501

        self._questions = questions
