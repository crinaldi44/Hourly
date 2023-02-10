# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.add_response import AddResponse  # noqa: E501
from openapi_server.models.error_list_response import ErrorListResponse  # noqa: E501
from openapi_server.models.package import Package  # noqa: E501
from openapi_server.models.package_list_response import PackageListResponse  # noqa: E501
from openapi_server.models.patch_document import PatchDocument  # noqa: E501
from openapi_server.test import BaseTestCase


class TestPackagesController(BaseTestCase):
    """PackagesController integration test stubs"""

    def test_add_package(self):
        """Test case for add_package

        Add Package
        """
        package = "{'name': 'Example', 'description': 'Example description', 'img_url': 'url', 'price': '15.00', 'companyId': 1, 'questions': [{'title': 'Example', 'value': '', 'values': ['Test'], 'data_type': 'multiselect'}] }"
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/packages',
            method='POST',
            headers=headers,
            data=json.dumps(package),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_package(self):
        """Test case for delete_package

        Delete Package
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/packages/{id}'.format(id='id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_package(self):
        """Test case for get_package

        Get Package
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/packages/{id}'.format(id='id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_packages(self):
        """Test case for list_packages

        List Packages
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
            '/api/v0/packages',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_patch_package(self):
        """Test case for patch_package

        Patch Package
        """
        patch_document = "{\n    \"op\": \"replace\",\n    \"path\": \"/name\",\n    \"value\": \"Sample3\"\n}"
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/packages/{id}'.format(id='id_example'),
            method='PATCH',
            headers=headers,
            data=json.dumps(patch_document),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
