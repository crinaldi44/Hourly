import axios from "axios"
import Authentication from '../auth/authentication'

/**
 * The employee service manages communication with the API endpoints in a restful fashion.
 */
class EmployeeService {

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
        
        const response = await axios.post('/employees', options)


    }

    /**
     * Deletes an employee
     * @param {number} id
     */
    deleteEmployee(id) {

    }

    /**
     * Updates the employee.
     * @param {JSON} employee 
     */
    updateEmployee(employee) {

    }

    /**
     * Retrieves all employees.
     */
    getAllEmployees() {

    }


}

export default new EmployeeService()