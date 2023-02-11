# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.company import Company
from openapi_server.models.role import Role
from openapi_server import util

from openapi_server.models.company import Company  # noqa: E501
from openapi_server.models.role import Role  # noqa: E501

class UserProfile(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, email=None, first_name=None, last_name=None, pay_rate=None, department_id=None, role_id=None, company=None, role=None):  # noqa: E501
        """UserProfile - a model defined in OpenAPI

        :param id: The id of this UserProfile.  # noqa: E501
        :type id: int
        :param email: The email of this UserProfile.  # noqa: E501
        :type email: str
        :param first_name: The first_name of this UserProfile.  # noqa: E501
        :type first_name: str
        :param last_name: The last_name of this UserProfile.  # noqa: E501
        :type last_name: str
        :param pay_rate: The pay_rate of this UserProfile.  # noqa: E501
        :type pay_rate: float
        :param department_id: The department_id of this UserProfile.  # noqa: E501
        :type department_id: int
        :param role_id: The role_id of this UserProfile.  # noqa: E501
        :type role_id: int
        :param company: The company of this UserProfile.  # noqa: E501
        :type company: Company
        :param role: The role of this UserProfile.  # noqa: E501
        :type role: Role
        """
        self.openapi_types = {
            'id': int,
            'email': str,
            'first_name': str,
            'last_name': str,
            'pay_rate': float,
            'department_id': int,
            'role_id': int,
            'company': Company,
            'role': Role
        }

        self.attribute_map = {
            'id': 'id',
            'email': 'email',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'pay_rate': 'pay_rate',
            'department_id': 'department_id',
            'role_id': 'role_id',
            'company': 'company',
            'role': 'role'
        }

        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.pay_rate = pay_rate
        self.department_id = department_id
        self.role_id = role_id
        self.company = company
        self.role = role

    @classmethod
    def from_dict(cls, dikt) -> 'UserProfile':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The UserProfile of this UserProfile.  # noqa: E501
        :rtype: UserProfile
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this UserProfile.


        :return: The id of this UserProfile.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this UserProfile.


        :param id: The id of this UserProfile.
        :type id: int
        """

        self._id = id

    @property
    def email(self):
        """Gets the email of this UserProfile.


        :return: The email of this UserProfile.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this UserProfile.


        :param email: The email of this UserProfile.
        :type email: str
        """

        self._email = email

    @property
    def first_name(self):
        """Gets the first_name of this UserProfile.


        :return: The first_name of this UserProfile.
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """Sets the first_name of this UserProfile.


        :param first_name: The first_name of this UserProfile.
        :type first_name: str
        """

        self._first_name = first_name

    @property
    def last_name(self):
        """Gets the last_name of this UserProfile.


        :return: The last_name of this UserProfile.
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """Sets the last_name of this UserProfile.


        :param last_name: The last_name of this UserProfile.
        :type last_name: str
        """

        self._last_name = last_name

    @property
    def pay_rate(self):
        """Gets the pay_rate of this UserProfile.


        :return: The pay_rate of this UserProfile.
        :rtype: float
        """
        return self._pay_rate

    @pay_rate.setter
    def pay_rate(self, pay_rate):
        """Sets the pay_rate of this UserProfile.


        :param pay_rate: The pay_rate of this UserProfile.
        :type pay_rate: float
        """

        self._pay_rate = pay_rate

    @property
    def department_id(self):
        """Gets the department_id of this UserProfile.


        :return: The department_id of this UserProfile.
        :rtype: int
        """
        return self._department_id

    @department_id.setter
    def department_id(self, department_id):
        """Sets the department_id of this UserProfile.


        :param department_id: The department_id of this UserProfile.
        :type department_id: int
        """

        self._department_id = department_id

    @property
    def role_id(self):
        """Gets the role_id of this UserProfile.


        :return: The role_id of this UserProfile.
        :rtype: int
        """
        return self._role_id

    @role_id.setter
    def role_id(self, role_id):
        """Sets the role_id of this UserProfile.


        :param role_id: The role_id of this UserProfile.
        :type role_id: int
        """

        self._role_id = role_id

    @property
    def company(self):
        """Gets the company of this UserProfile.


        :return: The company of this UserProfile.
        :rtype: Company
        """
        return self._company

    @company.setter
    def company(self, company):
        """Sets the company of this UserProfile.


        :param company: The company of this UserProfile.
        :type company: Company
        """

        self._company = company

    @property
    def role(self):
        """Gets the role of this UserProfile.


        :return: The role of this UserProfile.
        :rtype: Role
        """
        return self._role

    @role.setter
    def role(self, role):
        """Sets the role of this UserProfile.


        :param role: The role of this UserProfile.
        :type role: Role
        """

        self._role = role
