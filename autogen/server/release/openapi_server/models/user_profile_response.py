# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.user_profile import UserProfile
from openapi_server import util

from openapi_server.models.user_profile import UserProfile  # noqa: E501

class UserProfileResponse(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, user_profile=None):  # noqa: E501
        """UserProfileResponse - a model defined in OpenAPI

        :param user_profile: The user_profile of this UserProfileResponse.  # noqa: E501
        :type user_profile: UserProfile
        """
        self.openapi_types = {
            'user_profile': UserProfile
        }

        self.attribute_map = {
            'user_profile': 'userProfile'
        }

        self.user_profile = user_profile

    @classmethod
    def from_dict(cls, dikt) -> 'UserProfileResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The UserProfileResponse of this UserProfileResponse.  # noqa: E501
        :rtype: UserProfileResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def user_profile(self):
        """Gets the user_profile of this UserProfileResponse.


        :return: The user_profile of this UserProfileResponse.
        :rtype: UserProfile
        """
        return self._user_profile

    @user_profile.setter
    def user_profile(self, user_profile):
        """Sets the user_profile of this UserProfileResponse.


        :param user_profile: The user_profile of this UserProfileResponse.
        :type user_profile: UserProfile
        """

        self._user_profile = user_profile