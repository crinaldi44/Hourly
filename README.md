# Hourly
 Originally intended as in-class project for timesheet and payroll management, the Hourly cloud service
is an API that is intended to provide calculations and machine-learning based predictions to the user on
top of Create-Read-Update-Delete functionality. 

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
concerns. Each domain follows a routes/tests/utils pattern with the model for that particular route being
at the base level directory. The routes.py file within the routes folder serves to route and manipulate the data,
with several helper functions being contained within the model files. Additionally, unit tests are provided in the
tests folder and should be updated each time a new route has been added. You may run a script to validate all tests
at once. Unit tests should be batch-run by this method before each deployment.

## Security
You may protect routes that require a token with the @token_required wrapper, and the service will ensure that a token 
is passed and validated. The token will expire after the default expiration time OR when the service has been restarted,
as tokens are measured against their issued at time and compared with the system start time.

## Running the application
The application hosts all build/start scripts from the client side. Simply run the following commands:

** npm start **
** npm start-api **

From the client directory.

## The Data Layer
By default, this package uses SQLAlchemy's Object-Relational-Mapping library. In the server folder,
you will find the connection string in a module named database.py. Simply change the connection string
to your preferred dev/prod connection string.

The data schema will be created for you upon first run and any required tables will be inserted. By
default, a row in the Departments table named 'Management' will be created and MUST be initialized as
the first department, as it is the primary department. An employee account named 'admin' under this
department will be inserted, which will give you access to add any required employees.


## Data Security
This project is built with security in mind from the API level up. Routes at the API level are protected
using a JWT token with the secret API key found in the app.py file. To bolster this security feature
and due to the vulnerability nature of JWT tokens, it is recommended to rotate this security key periodically.

Any user with a 'management' account who is NOT in the Management department will simply only be able to view
and edit data for THEIR respective department. Conversely, users with an account in 'management'
will be able to view and edit data - including payroll and employees - for ANY department. Data
is protected at the server API level with a security token to prevent employees from accessing
any restricted data.

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
* Add event types route
* Add events route
* Add checks for request size get_data() > 1000 as well as request flooding
* Event Schema:
  * name
  * date
  * employee_id
  * created_by
* Companies Schema
  * Each user associated with a company ID
  * Only ones affected are company manager and Employee - only see info about company
  * Only company managers can see event package edit, departments, etc.
  * Departments should have a company ID associated
  * Admin and developer see anything - special forms eventually to add to ANY company or view
  * Company manager has access to change clockin method per company
  * Validate each model as well as user's company, role and department in JWT
* Data Visualization
  * Utilize DevExpress Reactive Charts for Data Visualization
  * For scheduling, utilize DevExpress Reactive Scheduler