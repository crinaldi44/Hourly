import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.add_response import AddResponse  # noqa: E501
from openapi_server.models.error_list_response import ErrorListResponse  # noqa: E501
from openapi_server.models.package import Package  # noqa: E501
from openapi_server.models.package_list_response import PackageListResponse  # noqa: E501
from openapi_server.models.patch_document import PatchDocument  # noqa: E501
from openapi_server import util


def add_package(package):  # noqa: E501
    """Add Package

     # noqa: E501

    :param package: Add Package
    :type package: dict | bytes

    :rtype: Union[AddResponse, Tuple[AddResponse, int], Tuple[AddResponse, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        package = Package.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_package(id):  # noqa: E501
    """Delete Package

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_package(id):  # noqa: E501
    """Get Package

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def list_packages(q=None, include_totals=None, page=None, fields=None, sort=None, offset=None, limit=None, lang=None):  # noqa: E501
    """List Packages

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

    :rtype: Union[PackageListResponse, Tuple[PackageListResponse, int], Tuple[PackageListResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


def patch_package(id, patch_document):  # noqa: E501
    """Patch Package

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
