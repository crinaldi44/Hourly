from crosscutting.response.list_response import serve_response, ListResponse
from crosscutting.auth.authentication import token_required
from crosscutting.exception.hourly_exception import HourlyException
from flask_cors import CORS
from flask import Blueprint, request

from domains.departments.services.department_service import Departments

# Represents the blueprint for this domain.
departments = Blueprint('departments', __name__, template_folder='templates', url_prefix='/api/v0')

# Enables Cross-Origin-Resource-Sharing across this domain.
CORS(departments)


