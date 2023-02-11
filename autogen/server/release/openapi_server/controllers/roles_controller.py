import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.add_response import AddResponse  # noqa: E501
from openapi_server.models.error_list_response import ErrorListResponse  # noqa: E501
from openapi_server.models.patch_document import PatchDocument  # noqa: E501
from openapi_server.models.role import Role  # noqa: E501
from openapi_server.models.role_list_response import RoleListResponse  # noqa: E501
from openapi_server import util


def add_role(role):  # noqa: E501
    """Add Role

     # noqa: E501

    :param role: Add Role
    :type role: dict | bytes

    :rtype: Union[AddResponse, Tuple[AddResponse, int], Tuple[AddResponse, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        role = Role.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_role(id):  # noqa: E501
    """Delete a role

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def list_roles(q=None, include_totals=None, page=None, fields=None, sort=None, offset=None, limit=None, lang=None):  # noqa: E501
    """List Roles

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

    :rtype: Union[RoleListResponse, Tuple[RoleListResponse, int], Tuple[RoleListResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


def patch_role(id, patch_document):  # noqa: E501
    """Patch a role

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
