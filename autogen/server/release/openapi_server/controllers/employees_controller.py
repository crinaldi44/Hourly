import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.add_response import AddResponse  # noqa: E501
from openapi_server.models.error_list_response import ErrorListResponse  # noqa: E501
from openapi_server.models.patch_document import PatchDocument  # noqa: E501
from openapi_server.models.user import User  # noqa: E501
from openapi_server.models.user_credentials import UserCredentials  # noqa: E501
from openapi_server.models.user_list_response import UserListResponse  # noqa: E501
from openapi_server.models.user_login_response import UserLoginResponse  # noqa: E501
from openapi_server.models.user_profile_response import UserProfileResponse  # noqa: E501
from openapi_server.models.user_sign_up_request import UserSignUpRequest  # noqa: E501
from openapi_server.models.user_validation_list_response import UserValidationListResponse  # noqa: E501
from openapi_server import util


def add_employee(user=None):  # noqa: E501
    """Add Employee

     # noqa: E501

    :param user: 
    :type user: dict | bytes

    :rtype: Union[AddResponse, Tuple[AddResponse, int], Tuple[AddResponse, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def authenticate_user(user_credentials=None):  # noqa: E501
    """Login User

     # noqa: E501

    :param user_credentials: 
    :type user_credentials: dict | bytes

    :rtype: Union[UserLoginResponse, Tuple[UserLoginResponse, int], Tuple[UserLoginResponse, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        user_credentials = UserCredentials.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_employee(id):  # noqa: E501
    """Delete Employee

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_employee(id):  # noqa: E501
    """Get Employee

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_users_profile(id):  # noqa: E501
    """Get Employee Profile

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[UserProfileResponse, Tuple[UserProfileResponse, int], Tuple[UserProfileResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


def list_users(q=None, include_totals=None, page=None, fields=None, sort=None, offset=None, limit=None, lang=None):  # noqa: E501
    """List Employees

     # noqa: E501

    :param q: default query parameter
    :type q: str
    :param include_totals: include the total count in the response
    :type include_totals: str
    :param page: The page to query from. This will take precedence over a limit and offset.
    :type page: str
    :param fields: Fields to exclude {\&quot;measurements\&quot;: 0} or only include {\&quot;measurements\&quot;: 1}
    :type fields: str
    :param sort: comma-separated list of fields to define the sort order. To indicate sorting direction, may be prefixed with + (ascending) or - (descending), e.g. /sales-orders?sort&#x3D;+id
    :type sort: str
    :param offset: numeric offset of the first element on a page
    :type offset: int
    :param limit: client suggested limit to restrict the number of entries on a page
    :type limit: int
    :param lang: language code to prefer for document elements (en-US, fr ...) page
    :type lang: str

    :rtype: Union[UserListResponse, Tuple[UserListResponse, int], Tuple[UserListResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


def patch_employee(id, patch_document):  # noqa: E501
    """Patch Employee

     # noqa: E501

    :param id: 
    :type id: str
    :param patch_document: 
    :type patch_document: list | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        patch_document = [PatchDocument.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


def signup_user(user_sign_up_request=None):  # noqa: E501
    """Signup Employee

     # noqa: E501

    :param user_sign_up_request: 
    :type user_sign_up_request: dict | bytes

    :rtype: Union[AddResponse, Tuple[AddResponse, int], Tuple[AddResponse, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        user_sign_up_request = UserSignUpRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def validate_employees(user_validation_list_response=None):  # noqa: E501
    """Validate Employees

     # noqa: E501

    :param user_validation_list_response: 
    :type user_validation_list_response: dict | bytes

    :rtype: Union[UserValidationListResponse, Tuple[UserValidationListResponse, int], Tuple[UserValidationListResponse, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        user_validation_list_response = UserValidationListResponse.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
