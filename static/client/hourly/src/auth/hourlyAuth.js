import { useEffect, useState } from "react"
import Authentication from './authentication'


/**
 * Represents a hook that may be used to authenticate a user.
 * @param {JSON} credentials the credentials to pass
 */
export default function useAuthenticator(credentials) {

    /**
     * Represents the authentication status.
    */
    const [isAuthenticated, setAuthenticated] = useState(false)

    /**
     * Represents the instantiated result.
     */
    let result;

    /**
     * When the component mounts, authenticate a user.
     */
    useEffect(async () => {

        // Store the result.
        result = await Authentication.authenticate(credentials)

        // If success, set authenticated to true. We will need to store
        // the JWT in local storage.
        if (result.status === 200) setAuthenticated(true)
    }, [])

    return isAuthenticated
}