# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.add_response import AddResponse  # noqa: E501
from openapi_server.models.error_list_response import ErrorListResponse  # noqa: E501
from openapi_server.models.patch_document import PatchDocument  # noqa: E501
from openapi_server.models.role import Role  # noqa: E501
from openapi_server.models.role_list_response import RoleListResponse  # noqa: E501
from openapi_server.test import BaseTestCase


class TestRolesController(BaseTestCase):
    """RolesController integration test stubs"""

    def test_add_role(self):
        """Test case for add_role

        Add Role
        """
        role = "{\n    \"name\": \"Role1\",\n    \"description\": \"Role1 description\"\n}"
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/roles',
            method='POST',
            headers=headers,
            data=json.dumps(role),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_role(self):
        """Test case for delete_role

        Delete a role
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/roles/{id}'.format(id='id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_roles(self):
        """Test case for list_roles

        List the set of permissions a user may retain.
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
            '/api/v0/roles',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_patch_role(self):
        """Test case for patch_role

        Patch a role
        """
        patch_document = "{\n    \"op\": \"replace\",\n    \"path\": \"/name\",\n    \"value\": \"Sample3\"\n}"
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/roles/{id}'.format(id='id_example'),
            method='PATCH',
            headers=headers,
            data=json.dumps(patch_document),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
