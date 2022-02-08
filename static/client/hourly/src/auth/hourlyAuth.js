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

    let result;

    /**
     * When the component mounts, authenticate a user.
     */
    useEffect(async () => {
        result = await Authentication.authenticate(credentials)
        setAuthenticated(result) // Set the auth state to the result.
    }, [])

    return isAuthenticated
}