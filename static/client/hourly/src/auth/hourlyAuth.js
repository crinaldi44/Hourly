import { useEffect, useState, useRef } from "react"
import Authentication from './authentication'


/**
 * The useAuth hook may be used to fetch the active user's credentials synchronously in
 * an active scenario. At any and every point in time, the user credentials are monitored
 * for instantaneous changes such as those in which the expiration of the JWT has changed.
 * 
 * The hook returns a JSON-based payload obtained from the JWT that stores the credentials,
 * in the following format: 
 * 
 * {employee_id, department_id, name, exp}
 * 
 * @param {JSON} credentials the credentials to pass
 */
export default function useAuth() {

    /**
     * Represents a ref for the active employee.
     */
    const didMount = useRef(false)


    /**
     * Return the active employee's credentials. If the token has expired, returns a message
     * stating that the employee credentials are invalid.
     */
    const [authCredentials, setAuthCredentials] = useState(Authentication.getActiveEmployee())

    /**
     * Simulates a componentDidUpdate. Whenever the useAuth should update, the value of the useRef
     * is updated and the user can obtain the credentials.
     */
    useEffect(async () => {
        if (didMount.current) {
            // On update, sets the auth credentials to the active employee's credentials.
            setAuthCredentials(Authentication.getActiveEmployee())
        } else {
            setAuthCredentials(Authentication.getActiveEmployee())
            didMount.current = true
        }
    }, [])

    return authCredentials
}