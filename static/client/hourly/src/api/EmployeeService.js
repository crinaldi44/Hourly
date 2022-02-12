import axios from "axios"
import Authentication from '../auth/authentication'
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

        let options = {
            method: 'POST',
            header: {
                'x-access-tokens': Authentication.getActiveEmployee()
            },
            body: employee
        }
        
        const response = await axios.post('/employees', options).catch(err => {
            throw new Error('Exception during response: ' + err)
        })

        if (!(this.successStatus.includes(response.status))) { 
            throw new ApiResponseError(response.status, response.data, `The server responded with error code ${response.status}`);
        }

        return response;
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

        return response;
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

        return response;
    }


}

export default new EmployeeService()