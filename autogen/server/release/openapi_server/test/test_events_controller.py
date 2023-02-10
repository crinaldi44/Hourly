# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.add_response import AddResponse  # noqa: E501
from openapi_server.models.error_list_response import ErrorListResponse  # noqa: E501
from openapi_server.models.event import Event  # noqa: E501
from openapi_server.models.event_list_response import EventListResponse  # noqa: E501
from openapi_server.models.event_search import EventSearch  # noqa: E501
from openapi_server.models.patch_document import PatchDocument  # noqa: E501
from openapi_server.test import BaseTestCase


class TestEventsController(BaseTestCase):
    """EventsController integration test stubs"""

    def test_add_event(self):
        """Test case for add_event

        Add Event
        """
        event = "{'name': 'Example', 'description': 'Example description', 'agreed_price': 'price', 'start_datetime': '203919174', 'end_datetime': '239829328', 'package_id': 1, 'employee_id': 1, 'questions': [{'title': 'Example', 'value': '', 'values': ['Test'], 'data_type': 'multiselect'}] }"
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/events',
            method='POST',
            headers=headers,
            data=json.dumps(event),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_event(self):
        """Test case for delete_event

        Delete Event
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/events/{id}'.format(id='id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_event(self):
        """Test case for get_event

        Get Event
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/events/{id}'.format(id='id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_events(self):
        """Test case for list_events

        List Events
        """
        query_string = [('q', 'q_example'),
                        ('include_totals', 'include_totals_example'),
                        ('page', 'page_example'),
                        ('fields', 'fields_example'),
                        ('sort', 'sort_example'),
                        ('offset', 56),
                        ('limit', 56),
                        ('lang', 'lang_example')]
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/events',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_patch_event(self):
        """Test case for patch_event

        Patch Event
        """
        patch_document = "{\n    \"op\": \"replace\",\n    \"path\": \"/name\",\n    \"value\": \"Sample3\"\n}"
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/events/{id}'.format(id='id_example'),
            method='PATCH',
            headers=headers,
            data=json.dumps(patch_document),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_events(self):
        """Test case for search_events

        Search Events
        """
        event_search = {"from_date":"01/01/2020","to_date":"02/20/2022","package_name":"dj"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/events/search',
            method='POST',
            headers=headers,
            data=json.dumps(event_search),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
