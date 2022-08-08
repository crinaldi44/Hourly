"""
    Stores error codes in a unified format. When you need to raise application
    specific errors, simply raise an HourlyException with the error code as the
    parameter.

    Example:
        @app.get('/test')
        def test_error():
            raise HourlyException('err.hourly.NoClockinsFound')
"""


err_codes = {

        "err.hourly.InvalidNumberFormatting": {
            "status": 400,
            "message": "Invalid number formatting provided.",
            "title": "InvalidNumberFormatting",
            "suggestion": "Please check your spelling and try again."
        },

        "err.hourly.RequestTooLarge": {
            "status": 400,
            "message": "The content type must be provided as JSON or the request was too large.",
            "title": "RequestTooLarge",
            "suggestion": "Please re-attempt your query with a smaller request."
        },

        "err.hourly.NoClockinsFound": {
            "status": 404,
            "message": "No clockins were found for this employee!",
            "title": "NoClockinsFound",
            "suggestion": "Please check the ID of the employee and re-attempt your query."
        },

        "err.hourly.ClockinNotFound": {
            "status": 404,
            "message": "No clockin was found by this ID!",
            "title": "ClockinNotFound",
            "suggestion": "Please check the ID of the clockin and re-attempt your query."
        },

        "err.hourly.UserNotFound": {
            "status": 404,
            "message": "No user was found with that ID.",
            "title": "UserNotFound",
            "suggestion": "Please check the ID of the user and re-attempt your query."
        },

        'err.hourly.UserExists': {
            "status": 409,
            "message": "This email address is taken.",
            "title": "UserExists",
            "suggestion": "Please provide an alternate email address and re-attempt."
        },

        "err.hourly.InvalidUserDelete": {
            "status": 400,
            "message": "Invalid user deletion.",
            "title": "InvalidUserDelete",
            "suggestion": "Please check the user and re-attempt your deletion request."
        },

        "err.hourly.InvalidUserPayRate": {
            "status": 404,
            "message": "The format of the user pay rate is invalid!",
            "title": "InvalidUserPayRate",
            "suggestion": "Please ensure that the user pay rate is a valid number."
        },

        "err.hourly.InvalidCredentials": {
            "status": 403,
            "message": "Invalid email or password provided.",
            "title": "InvalidCredentials",
            "suggestion": "Please check your credentials and re-attempt your login."
        },

        "err.hourly.UnauthorizedRequest": {
            "status": 403,
            "message": "You are not authorized to make this request.",
            "title": "UnauthorizedRequest",
            "suggestion": "Please double-check the request and try again."
        },

        "err.hourly.BadUsernameOrPassword": {
            "status": 422,
            "message": "Invalid email or password provided.",
            "title": "BadUsernameOrPassword",
            "suggestion": "Please ensure your password contains at least one special character and that your email is of valid formatting."
        },

        "err.hourly.DepartmentNotFound": {
            "status": 404,
            "message": "No department was found with that ID.",
            "title": "DepartmentNotFound",
            "suggestion": "Please check the ID of the department and re-attempt your query."
        },

        "err.hourly.InvalidDepartmentDelete": {
            "status": 400,
            "message": "Invalid department deletion.",
            "title": "InvalidDepartmentDelete",
            "suggestion": "Please check the department and re-attempt your deletion request."
        },

        "err.hourly.BadDepartmentFormatting": {
            "status": 422,
            "message": "Invalid department formatting specified.",
            "title": "InvalidDepartmentDelete",
            "suggestion": "Please verify all fields have been included and re-attempt your request."
        },

        "err.hourly.DepartmentExists": {
            "status": 409,
            "message": "A department already exists by that name!",
            "title": "DepartmentExists",
            "suggestion": "Please modify and re-attempt your request."
        },

        "err.hourly.BadUserFormatting": {
            "status": 422,
            "message": "Invalid user formatting specified.",
            "title": "BadUserFormatting",
            "suggestion": "Please verify all fields have been included and re-attempt your request."
        },

        "err.hourly.BadRoleFormatting": {
            "status": 422,
            "message": "Invalid role formatting specified.",
            "title": "BadRoleFormatting",
            "suggestion": "Please verify all fields have been included and re-attempt your request."
        },

        "err.hourly.RoleNotFound": {
            "status": 404,
            "message": "No role was found by that ID.",
            "title": "RoleNotFound",
            "suggestion": "Please check the ID of the role and re-attempt your query."
        },

        "err.hourly.PackageNotFound": {
            "status": 404,
            "message": "No package was found by that ID.",
            "title": "PackageNotFound",
            "suggestion": "Please check the ID of the package and re-attempt your query."
        },

        "err.hourly.BadPackageFormatting": {
            "status": 422,
            "message": "Invalid package formatting specified.",
            "title": "BadPackageFormatting",
            "suggestion": "Please verify all fields have been included and re-attempt your request."
        },

        "err.hourly.PackageExists": {
            "status": 409,
            "message": "A package already exists by that name!",
            "title": "PackageExists",
            "suggestion": "Please modify and re-attempt your request."
        },

        "err.hourly.CompanyNotFound": {
            "status": 404,
            "message": "No company was found by that ID.",
            "title": "CompanyNotFound",
            "suggestion": "Please check the ID of the company and re-attempt your query."
        },

        "err.hourly.BadCompanyFormatting": {
            "status": 422,
            "message": "Invalid company formatting specified.",
            "title": "BadCompanyFormatting",
            "suggestion": "Please verify all fields have been included and re-attempt your request."
        },

        "err.hourly.CompanyExists": {
            "status": 409,
            "message": "A company already exists by that name!",
            "title": "CompanyExists",
            "suggestion": "Please modify and re-attempt your request."
        },

        "err.hourly.InvalidCompanyDelete": {
            "status": 400,
            "message": "Invalid company deletion.",
            "title": "InvalidCompanyDelete",
            "suggestion": "Please check the company and re-attempt your deletion request."
        },

}