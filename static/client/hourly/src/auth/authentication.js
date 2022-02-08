import axios from 'axios'

/**
 * Represents the authentication state of the client side. Stores
 * and manages authentication methods. 
 *  
 * In order to make use of the useAuthenticator hook, first you
 * must implement a <ProtectedRoute>. Pass in the form data as props.
 * The client will then read the props, access the authenticator, and
 * set the state of authentication to true if a valid JWT is obtained.
 * @author Chris Rinaldi
 * @see ProtectedRoute
 */
class Authentication {

    /**
     * Constructs a new Authentication object. By default,
     * the authentication state is declared as false. If we
     * have a valid un-expired JWT stored in session cookies 
     * OR local storage, authentication state will return true.
     */
    constructor() {
        this.authenticated = false;
    }

    /**
     * Authenticates the user. First, an async request is made to
     * the authentication service via POST request. A JWT is provided
     * by the auth service and returned. The response is passed into
     * the callback function.
     * @param id represents the id to pass
     * @param password represents the password to send
     * @param callback represents the callback to pass
     */
    async authenticate(id, password) {
        let options = {
            headers: {
                'Content-Type': 'application/json'
            },
            data: {
                'id': id,
                'password': password
            }
        }
        let result = await axios.post('/login', options) // Initiate the request to the server.
        localStorage.setItem('employee', result.data['token'])
        return result // Return the JWT
    }

    /**
     * De-authenticates the user. Sets the value of
     * the authentication state to false.
     */
    deAuthenticate() {
        localStorage.removeItem('employee')
    }

    /**
     * 
     * @returns {boolean} the authentication state.
     */
    isAuthenticated() {
        // This should 1) check to verify 'employee' is in local storage and
        // 2), verify that the 'exp' field in the JWT payload has not expired.
        return localStorage.getItem('employee') || false
    }

    /**
     * 
     * @returns {JSON} a representation of the active employee
     */
    getActiveEmployee() {
        return JSON.parse(localStorage.getItem('employee'))
    }

}

export default new Authentication()