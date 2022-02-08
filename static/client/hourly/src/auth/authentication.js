
/**
 * Represents the authentication state of the client side. Stores
 * and manages authentication methods.
 * @author Chris Rinaldi
 */
class Authentication {

    /**
     * Constructs a new Authentication object. By default,
     * the authentication state is declared as false. If we
     * have a JWT stored in session cookies OR local storage, 
     * authentication state will return true.
     */
    constructor() {
        this.authenticated = true;
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
    async authenticate(id, password, callback) {
        let options = {
            method: 'POST',
            data: {
                'id': id,
                'password': password
            }
        }
        let result = fetch('/login')
        callback() // Return the JSON web token in the callback.
    }

    /**
     * De-authenticates the user. Sets the value of
     * the authentication state to false.
     */
    deAuthenticate() {
        this.authenticated = false;
    }

    /**
     * 
     * @returns {boolean} the authentication state.
     */
    isAuthenticated() {
        return this.authenticated
    }

}

export default new Authentication()