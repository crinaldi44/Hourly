import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.add_response import AddResponse  # noqa: E501
from openapi_server.models.error_list_response import ErrorListResponse  # noqa: E501
from openapi_server.models.event import Event  # noqa: E501
from openapi_server.models.event_list_response import EventListResponse  # noqa: E501
from openapi_server.models.event_search import EventSearch  # noqa: E501
from openapi_server.models.patch_document import PatchDocument  # noqa: E501
from openapi_server import util


def add_event(event):  # noqa: E501
    """Add Event

     # noqa: E501

    :param event: Add Event
    :type event: dict | bytes

    :rtype: Union[AddResponse, Tuple[AddResponse, int], Tuple[AddResponse, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        event = Event.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_event(id):  # noqa: E501
    """Delete Event

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_event(id):  # noqa: E501
    """Get Event

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def list_events(q=None, include_totals=None, page=None, fields=None, sort=None, offset=None, limit=None, lang=None):  # noqa: E501
    """List Events

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

    :rtype: Union[EventListResponse, Tuple[EventListResponse, int], Tuple[EventListResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


def patch_event(id, patch_document):  # noqa: E501
    """Patch Event

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


def search_events(event_search):  # noqa: E501
    """Search Events

    Searches events within the user&#39;s company. # noqa: E501

    :param event_search: Search Event
    :type event_search: dict | bytes

    :rtype: Union[AddResponse, Tuple[AddResponse, int], Tuple[AddResponse, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        event_search = EventSearch.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
