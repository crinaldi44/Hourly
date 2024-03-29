# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Company(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, name='', about='', phone='', address_street='', city='', state='', zip_code='', img_url='', private=False):  # noqa: E501
        """Company - a model defined in OpenAPI

        :param id: The id of this Company.  # noqa: E501
        :type id: int
        :param name: The name of this Company.  # noqa: E501
        :type name: str
        :param about: The about of this Company.  # noqa: E501
        :type about: str
        :param phone: The phone of this Company.  # noqa: E501
        :type phone: str
        :param address_street: The address_street of this Company.  # noqa: E501
        :type address_street: str
        :param city: The city of this Company.  # noqa: E501
        :type city: str
        :param state: The state of this Company.  # noqa: E501
        :type state: str
        :param zip_code: The zip_code of this Company.  # noqa: E501
        :type zip_code: str
        :param img_url: The img_url of this Company.  # noqa: E501
        :type img_url: str
        :param private: The private of this Company.  # noqa: E501
        :type private: bool
        """
        self.openapi_types = {
            'id': int,
            'name': str,
            'about': str,
            'phone': str,
            'address_street': str,
            'city': str,
            'state': str,
            'zip_code': str,
            'img_url': str,
            'private': bool
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'about': 'about',
            'phone': 'phone',
            'address_street': 'address_street',
            'city': 'city',
            'state': 'state',
            'zip_code': 'zip_code',
            'img_url': 'img_url',
            'private': 'private'
        }

        self.id = id
        self.name = name
        self.about = about
        self.phone = phone
        self.address_street = address_street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.img_url = img_url
        self.private = private

    @classmethod
    def from_dict(cls, dikt) -> 'Company':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Company of this Company.  # noqa: E501
        :rtype: Company
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Company.

        Unique identifier  # noqa: E501

        :return: The id of this Company.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Company.

        Unique identifier  # noqa: E501

        :param id: The id of this Company.
        :type id: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Company.

        The name of the company.  # noqa: E501

        :return: The name of this Company.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Company.

        The name of the company.  # noqa: E501

        :param name: The name of this Company.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def about(self):
        """Gets the about of this Company.

        The company's about us.  # noqa: E501

        :return: The about of this Company.
        :rtype: str
        """
        return self._about

    @about.setter
    def about(self, about):
        """Sets the about of this Company.

        The company's about us.  # noqa: E501

        :param about: The about of this Company.
        :type about: str
        """

        self._about = about

    @property
    def phone(self):
        """Gets the phone of this Company.

        organization phone  # noqa: E501

        :return: The phone of this Company.
        :rtype: str
        """
        return self._phone

    @phone.setter
    def phone(self, phone):
        """Sets the phone of this Company.

        organization phone  # noqa: E501

        :param phone: The phone of this Company.
        :type phone: str
        """

        self._phone = phone

    @property
    def address_street(self):
        """Gets the address_street of this Company.

        The street address of the company.  # noqa: E501

        :return: The address_street of this Company.
        :rtype: str
        """
        return self._address_street

    @address_street.setter
    def address_street(self, address_street):
        """Sets the address_street of this Company.

        The street address of the company.  # noqa: E501

        :param address_street: The address_street of this Company.
        :type address_street: str
        """

        self._address_street = address_street

    @property
    def city(self):
        """Gets the city of this Company.

        The city in which the company is located.  # noqa: E501

        :return: The city of this Company.
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city):
        """Sets the city of this Company.

        The city in which the company is located.  # noqa: E501

        :param city: The city of this Company.
        :type city: str
        """

        self._city = city

    @property
    def state(self):
        """Gets the state of this Company.

        state  # noqa: E501

        :return: The state of this Company.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this Company.

        state  # noqa: E501

        :param state: The state of this Company.
        :type state: str
        """

        self._state = state

    @property
    def zip_code(self):
        """Gets the zip_code of this Company.

        zipCode  # noqa: E501

        :return: The zip_code of this Company.
        :rtype: str
        """
        return self._zip_code

    @zip_code.setter
    def zip_code(self, zip_code):
        """Sets the zip_code of this Company.

        zipCode  # noqa: E501

        :param zip_code: The zip_code of this Company.
        :type zip_code: str
        """

        self._zip_code = zip_code

    @property
    def img_url(self):
        """Gets the img_url of this Company.

        Represents the url of the company's image.  # noqa: E501

        :return: The img_url of this Company.
        :rtype: str
        """
        return self._img_url

    @img_url.setter
    def img_url(self, img_url):
        """Sets the img_url of this Company.

        Represents the url of the company's image.  # noqa: E501

        :param img_url: The img_url of this Company.
        :type img_url: str
        """

        self._img_url = img_url

    @property
    def private(self):
        """Gets the private of this Company.

        Whether the company's events are queryable.   # noqa: E501

        :return: The private of this Company.
        :rtype: bool
        """
        return self._private

    @private.setter
    def private(self, private):
        """Sets the private of this Company.

        Whether the company's events are queryable.   # noqa: E501

        :param private: The private of this Company.
        :type private: bool
        """

        self._private = private
