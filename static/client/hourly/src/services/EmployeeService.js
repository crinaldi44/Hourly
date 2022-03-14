import axios from "axios"
import Authentication from '../hooks/auth/authentication'
import ApiResponseError from './ApiResponseError'

/**
 * The employee service manages communication with the API endpoints in a restful fashion.
 */
class EmployeeService {

    /**
     * Represents the success statuses.
     */
    successStatus = [
        200,
        201,
        202,
        203,
        204
    ]

    /**
     * Retrieves clockins for the specified department.
     * @param {number} department represents the department to obtain for.
     */
    async getClockinsForDepartment(department) {
        const options = {
            headers: {
                'x-access-tokens': Authentication.getToken()
            }
        }

        let result;

        try {
            result = await axios.get(`/departments/${department}/clockin`, options)
        } catch (error) {
            if (error.response) result = error.response
        }

        return result.data;
    }

    /**
     * Gets employee details.
     * @param {number} id represents the ID of the employee
     */
    async getEmployee(id) {
        let options = {
            headers: {
                'x-access-tokens': Authentication.getToken()
            }
        }

        let response;

        try {
            response = await axios.get(`/employees/${id}`, options)
        } catch (err) {
            if (err.response) { 
                response = err.response
            }
        }
        
        return response
    }

    /**
     * Builds an employee an sends to the database. Specifies the auth token
     * in the header.
     * @param {JSON} employee represents an employee in JSON form to send
     */
    async buildEmployee(employee) {

        let options = {
            headers: {
                'x-access-tokens': Authentication.getToken()
            }
        }

        let response;

        try {
            response = await axios.post('/employees', employee, options)
        } catch (err) {
            if (err.response) { 
                response = err.response
            }
        }
        
        return response
    }

    /**
     * Deletes an employee
     * @param {number} id
     * @returns response the response from the server
     */
    async deleteEmployee(id) {
        let options = {
            headers: {
                'x-access-tokens': Authentication.getToken()
            }
        }

        let response;

        try {
            response = await axios.delete(`/employees/${id}`, options)
        } catch (err) {
            if (err.response) {
                response = err.response
            }
        }

        return response;
    }

    /**
     * Updates the employee.
     * @param id the id
     * @param {JSON} employee the updated employee object
     */
    async updateEmployee(id, employee) {
        let options = {
            headers: {
                'x-access-tokens': Authentication.getToken()
            }
        }

        let response;

        try {
            response = await axios.patch(`/employees/${id}`, employee, options)
        } catch (err) {
            if (err.response) {
                response = err.response
            }
        }

        return response
    }

    /**
     * Retrieves all employees.
     * @returns response the response
     */
    async getAllEmployees() {

        let options = {
            method: 'GET',
            headers: {
                'x-access-tokens': Authentication.getToken()
            }
        }

        const response = await axios.get('/employees', options)

        if (!(this.successStatus.includes(response.status))) { 
            throw new ApiResponseError(response.status, response.data, `The server responded with error code ${response.status}`)
        }

        return response.data;
    }

    /**
     * Gets employees by the provided department id.
     * @param {number} id 
     * @returns 
     */
    async getEmployeesForDepartment(id) {
        let options = {
            headers: {
                'x-access-tokens': Authentication.getToken()
            }
        }
        
        let response
        
        try {
            response = await axios.get(`/employees?department=${id}`, options)
        } catch (error) {
            if (error.response) {
                response = error.response
            }
        }

        return response.data
    }

    /**
     * Retrieves all active departments.
     */
    async getAllDepartments() {

        let options = {
            method: 'GET',
            headers: {
                'x-access-tokens': Authentication.getToken()
            }
        }

        const response = await axios.get('/employees/departments', options)

        if (!(this.successStatus.includes(response.status))) {
            throw new ApiResponseError(response.status, response.data, `The server responded with error code ${response.status}`)
        }

        return response.data
    }

    /**
     * Adds the specified department to the database.
     * @param {JSON} department represents the department to add
     */
    async addDepartment(department) {

        if (!Object.keys(department).includes('department_name')) {
            throw new Error('Invalid department object specified.');
        }

        let options = {
            headers: {
                'x-access-tokens': Authentication.getToken()
            }
        }

        let response;
        
        try {
            response = await axios.post('/employees/departments', department, options)
        } catch (error) {
            if (error.response) response = error.response   
        }

        return response.data;

    }

    /**
     * Updates the specified department.
     */
    async updateDepartment(department) {
        let options = {
            headers: {
                'x-access-tokens': Authentication.getToken()
            }
        }

        let response
        
        try {
            response = await axios.patch(`/employees/departments/${department.department_id}`, department, options)
        } catch (err) {
            if (err.response) {
                response = err.response
            }
        }

        return response.data;
    }

    /**
     * Deletes the specified department.
     * @param {number} id represents id of department to delete
     */
    async deleteDepartment(id) {
        let options = {
            headers: {
                'x-access-tokens': Authentication.getToken()
            }
        }

        let response;
        try {
            response = await axios.delete(`/employees/departments/${id}`, options)   
        } catch (error) {
            if (error.response) {
                response = error.response
            }
        }

        return response.data
    }


    /**
     * Gets the payroll information for a specified department.
     * @param {number} id represents the id of the department
     */
    async getPayroll(id) {

        let options = {
            headers: {
                'x-access-tokens': Authentication.getToken()
            }
        }
        
        let route = id ? `/employees/payroll?department=${id}` : '/employees/payroll'

        let result;

        try {
            result = axios.get(route, options)
        } catch (error) {
            if (error.response) result = error.response
        }

        return result.data;

    }

    /**
     * Gets the hours information for a specified department.
     * @param {number} id represents the id of the department
     */
     async getDepartmentHours(id) {

        let options = {
            headers: {
                'x-access-tokens': Authentication.getToken()
            }
        }
        
        let route = id ? `/employees/hours?department=${id}` : '/employees/hours'

        let result;

        try {
            result = axios.get(route, options)
        } catch (error) {
            if (error.response) result = error.response
        }

        return result.data;

    }

    /**
     * Gets budget information for the specified department.
     * @param id {number} represents the id of the department
     * @return {Promise<void>}
     */
    async getBudget(id) {
        if (id) {
            let options = {
                headers: {
                    'x-access-tokens': Authentication.getToken()
                }
            }

            let result

            try {
                result = axios.get(`/employees/budget/${id}`, options)
            } catch (error) {
                if (error.response) result = error.response
            }

            return result.data
        }
    }


}

export default new EmployeeService()