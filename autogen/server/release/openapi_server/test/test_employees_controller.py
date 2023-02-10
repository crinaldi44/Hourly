# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.error_list_response import ErrorListResponse  # noqa: E501
from openapi_server.models.list_response import ListResponse  # noqa: E501
from openapi_server.models.patch_document import PatchDocument  # noqa: E501
from openapi_server.models.user import User  # noqa: E501
from openapi_server.models.user_list_response import UserListResponse  # noqa: E501
from openapi_server.models.user_login_request import UserLoginRequest  # noqa: E501
from openapi_server.models.user_login_response import UserLoginResponse  # noqa: E501
from openapi_server.models.user_sign_up_response import UserSignUpResponse  # noqa: E501
from openapi_server.models.user_validation_list import UserValidationList  # noqa: E501
from openapi_server.test import BaseTestCase


class TestEmployeesController(BaseTestCase):
    """EmployeesController integration test stubs"""

    def test_add_employee(self):
        """Test case for add_employee

        Add Employee
        """
        user = "{\n    \"name\": \"User1\",\n    \"description\": \"User1 description\"\n}"
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/employees',
            method='POST',
            headers=headers,
            data=json.dumps(user),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_authenticate_user(self):
        """Test case for authenticate_user

        Login User
        """
        user_login_request = {"email":"email","password":"password"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v0/employees/login',
            method='POST',
            headers=headers,
            data=json.dumps(user_login_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_employee(self):
        """Test case for delete_employee

        Delete Employee
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/employees/{id}'.format(id='id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_employee(self):
        """Test case for get_employee

        Get Employee
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/employees/{id}'.format(id='id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_users_profile(self):
        """Test case for get_users_profile

        Get Employee Profile
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/users/profile/{id}'.format(id='id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_users(self):
        """Test case for list_users

        List Employees
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
            '/api/v0/employees',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_patch_employee(self):
        """Test case for patch_employee

        Patch Employee
        """
        patch_document = "{\n    \"op\": \"replace\",\n    \"path\": \"/name\",\n    \"value\": \"Sample3\"\n}"
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/employees/{id}'.format(id='id_example'),
            method='PATCH',
            headers=headers,
            data=json.dumps(patch_document),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_signup_user(self):
        """Test case for signup_user

        Signup Employee
        """
        user = "{\n    \"name\": \"User1\",\n    \"description\": \"User1 description\"\n}"
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/user/signup',
            method='POST',
            headers=headers,
            data=json.dumps(user),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_validate_employees(self):
        """Test case for validate_employees

        Validate Employees
        """
        user_validation_list = {"message":"Success.","status":200,"data":[{"zipCode":"zipCode","phone":"phone","city":"city","name":"name","about":"about","addressStreet":"addressStreet","id":"id","state":"state"},{"zipCode":"zipCode","phone":"phone","city":"city","name":"name","about":"about","addressStreet":"addressStreet","id":"id","state":"state"}]}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v0/employees/validate',
            method='POST',
            headers=headers,
            data=json.dumps(user_validation_list),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
