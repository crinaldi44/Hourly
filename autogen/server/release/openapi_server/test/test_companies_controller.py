# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.add_response import AddResponse  # noqa: E501
from openapi_server.models.company import Company  # noqa: E501
from openapi_server.models.company_list_response import CompanyListResponse  # noqa: E501
from openapi_server.models.error_list_response import ErrorListResponse  # noqa: E501
from openapi_server.models.patch_document import PatchDocument  # noqa: E501
from openapi_server.test import BaseTestCase


class TestCompaniesController(BaseTestCase):
    """CompaniesController integration test stubs"""

    def test_add_company(self):
        """Test case for add_company

        Add Company
        """
        company = "{\n    \"zip_code\": \"zip_code\",\n    \"phone\": \"phone\",\n    \"city\": \"city\",\n    \"name\": \"name\",\n    \"about\": \"about\",\n    \"address_street\": \"address_street\",\n    \"id\": \"id\",\n    \"state\": \"state\"\n    \"img_url\": \"img_url\"\n}"
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/companies',
            method='POST',
            headers=headers,
            data=json.dumps(company),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_company(self):
        """Test case for delete_company

        Delete Company
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/companies/{id}'.format(id='id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_company(self):
        """Test case for get_company

        Delete Company
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/companies/{id}'.format(id='id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_companies(self):
        """Test case for list_companies

        List Companies
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
            '/api/v0/companies',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_patch_company(self):
        """Test case for patch_company

        Patch Company
        """
        patch_document = "{\n    \"op\": \"replace\",\n    \"path\": \"/name\",\n    \"value\": \"Sample3\"\n}"
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/companies/{id}'.format(id='id_example'),
            method='PATCH',
            headers=headers,
            data=json.dumps(patch_document),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
