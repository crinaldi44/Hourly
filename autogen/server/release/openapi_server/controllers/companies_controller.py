import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.add_response import AddResponse  # noqa: E501
from openapi_server.models.company import Company  # noqa: E501
from openapi_server.models.company_list_response import CompanyListResponse  # noqa: E501
from openapi_server.models.error_list_response import ErrorListResponse  # noqa: E501
from openapi_server.models.patch_document import PatchDocument  # noqa: E501
from openapi_server import util


def add_company(company):  # noqa: E501
    """Add Company

     # noqa: E501

    :param company: Add Company
    :type company: dict | bytes

    :rtype: Union[AddResponse, Tuple[AddResponse, int], Tuple[AddResponse, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        company = Company.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_company(id):  # noqa: E501
    """Delete Company

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_company(id):  # noqa: E501
    """Delete Company

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def list_companies(q=None, include_totals=None, page=None, fields=None, sort=None, offset=None, limit=None, lang=None):  # noqa: E501
    """List Companies

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

    :rtype: Union[CompanyListResponse, Tuple[CompanyListResponse, int], Tuple[CompanyListResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


def patch_company(id, patch_document):  # noqa: E501
    """Patch Company

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
