# Hourly
Originally intended as in-class project for timesheet and payroll management, the Hourly cloud service
is an API that is intended to serve calculations and machine-learning based predictions to the user that
aim to provide data that benefits cost-optimization, scheduling, and increased workload productivity of small
businesses.

This is a Flask application wrapped in a library called Connexion, which will route requests based on an
OpenAPI spec.

The application achieves this by streamlining information that is commonly spread across 3-4 applications and 
combining it into one general portal.

# Getting Started

## Pre-requisites
To get this project up and running, you'll need to ensure the latest version of python3 and pip3 are up and running.

For the server side, a requirements.txt file has been included. By default, it is recommended to
install a python3 virtualenv folder in the home directory to avoid conflicts with other projects.
Once this has been completed, you can simply activate your virtual environment using:

source venv/bin/activate (MacOS)
OR
venv/Scripts/activate (Windows Powershell/GitBash)

And pip3 install each of the required dependencies.

## Structure of the Cloud
The cloud is based on Python's Flask library. The application leverages a domain-driven design for separation of
concerns. Each domain follows a routes/tests/utils/services pattern with the model for that particular route being
at the base level directory. The routes.py file within the routes folder serves to route the data to the service layer,
which provides automated deserialization and validation of the data. Additionally, unit tests are provided in the
tests folder and should be updated each time a new route has been added. You may run a script to validate all tests
at once. Unit tests should be batch-run by this method before each deployment.

There are 2 cloud servers which are hosted on IaaS platform Heroku which provides SSL certificates and a personalized
domain. They are located at:

  * hourly-cloud-dev
  * hourly-cloud-prod

## Security
You may protect routes that require a token with the @token_required wrapper, and the service will ensure that a token 
is passed and validated. The token will expire after the default expiration time OR when the service has been restarted,
as tokens are measured against their issued at time and compared with the system start time.

A rate limit of 100 requests per minute is imposed on the application as a whole to prevent flooding the backend with
requests. On endpoints that require heavier logic, joins or complex querying, it is suggested to use the default secure
rate limit of 50 requests per minute.

## The Data Layer
By default, this package uses SQLAlchemy's Object-Relational-Mapping library. In the server folder,
you will find the connection string in a module named database.py. Simply change the connection string
to your preferred dev/prod connection string.

The data tables will be created for you upon first run and any required tables will be inserted. Each
model contains a Validation (or "schema") layer which serves to deserialize the data and validate it. If
a validation error occurs, a response is sent back to the user with the error that occurred.

### Entities
Below is a list of each entity that exists within the Hourly cloud as well as a brief description of its
function:

* Clockins: A representation of a block of time that an employee has worked.
* Companies: Groups of users that hold data that is unique to that group.
* Departments: Subsections of companies that divide users into a function
* Employees: Users that exist within the database.
* Packages: Templates for event types
* Events: Instantiations of packages that contain unique metadata

## Security
This project is built with security in mind from the API level up. Routes at the API level are protected
using a JWT token with the secret API key found in the app.py file. To bolster this security feature
and due to the vulnerability nature of JWT tokens, it is recommended to rotate this security key periodically.

The scope of accessible data is limited on a role-and-company based premise. Users of any role up to and including
organization owner will only be able to access data from within their company. Conversely, users with the administrator
role will be able to access ANY data from any company. Query limits are capped at 100 to protect data.

To mitigate network traffic and prevent potential Denial-of-Service or other malicious attacks, rate limiting techniques are introduced
to throttle frequency of user requests within a short timeframe. Should the user exceed the rate limit multiple times, their IP will
be added to a blacklist.

# Cross-Cutting
This directory contains general-purpose functionality for use across each domain.

## Exception Handling
This project utilizes Flask's error handling capabilities to streamline the process of handling various errors
within the application. Any exception that occurs within the application is returned to the user in
the response as a streamlined dict for ease of error-handling within the frontend.

Within the exception directory, there is an HourlyException class that you may raise. The constructor
takes the error code as an argument. You will find the mapping of error codes to error code metadata 
within the exception directory.

# TODO
* Add routes for payroll reporting*
* Add calculations for employee hours
* Add machine learning model to predict cost and expenses of an employee based on number of events serviced within the past month and the price per event
* Add events route
* Add checks for request size get_data() > 1000 as well as request flooding
* Event Schema:
  * name
  * start_date
  * end_date
  * employee_id (assigned/created by)
  * package_id
  * company_id
  * department_id
* Validations with flask-marshmallow - add "validation/schema" layer
* Security
  * JWT blacklist once user logs out? or session invalidation
* Companies Schema
  * Only ones affected are company manager and Employee - only see info about company
  * Only company managers can see event package edit, departments, etc.
  * Departments should have a company ID associated
  * Admin and developer see anything - special forms eventually to add to ANY company or view
  * Company manager has access to change clockin method per company
  * Validate each model as well as user's company, role and department in JWT
* Data Visualization
  * Utilize DevExpress Reactive Charts for Data Visualization
  * For scheduling, utilize DevExpress Reactive Scheduler