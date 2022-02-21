# Hourly
 An in-class project for timesheet and payroll management.

# Getting Started

## Pre-requisites
This project is managed by the Node Package Manager (referred to as NPM). To get this project up
and running, you'll need to ensure that the latest version of NPM as well as the latest version
of python3 and pip3 are up and running.

For the client side, a package.json file has been provided. Simply cd into the client directory
and use npm install to install all client-side dependencies. 

For the server side, a requirements.txt file has been included. By default, it is recommended to
install a python3 virtualenv folder in the home directory to avoid conflicts with other projects.
Once this has been completed, you can simply activate your virtual environment using:

source venv/bin/activate (MacOS)
OR
venv/Scripts/activate (Windows Powershell/GitBash)

And pip3 install each of the required dependencies.

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

# TODO
Add routes for payroll reporting*
Add calculations for employee hours