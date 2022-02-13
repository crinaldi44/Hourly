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
     * Builds an employee an sends to the database. Specifies the auth token
     * in the header.
     * @param {JSON} employee represents an employee in JSON form to send
     */
    async buildEmployee(employee) {

        let response;

        try {
            response = await axios.post('/employees', employee)
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
            method: 'DELETE',
            header: {
                'x-access-tokens': Authentication.getActiveEmployee()
            }
        }

        const response = await axios.delete(`/employees/${id}`).catch(err => {
            throw new Error('An exception occurred during the response: ' + err)
        })

        if (!(this.successStatus.includes(response.status))) {
            throw new ApiResponseError(response.status, response.data, `The server responded with error code ${response.status}`)
        }

        return response.data;
    }

    /**
     * Updates the employee.
     * @param {JSON} employee 
     */
    updateEmployee(employee) {

    }

    /**
     * Retrieves all employees.
     * @returns response the response
     */
    async getAllEmployees() {

        let options = {
            method: 'GET',
            header: {
                'x-access-tokens': Authentication.getActiveEmployee()
            }
        }

        const response = await axios.get('/employees', options)

        if (!(this.successStatus.includes(response.status))) { 
            throw new ApiResponseError(response.status, response.data, `The server responded with error code ${response.status}`)
        }

        return response.data;
    }

    /**
     * Retrieves all active departments.
     */
    async getAllDepartments() {

        let options = {
            method: 'GET',
            header: {
                'x-access-token': Authentication.getActiveEmployee()
            }
        }

        const response = await axios.get('/employees/departments', options)

        if (!(this.successStatus.includes(response.status))) {
            throw new ApiResponseError(response.status, response.data, `The server responded with error code ${response.status}`)
        }

        return response.data
    }


}

export default new EmployeeService()