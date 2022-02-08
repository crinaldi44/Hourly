import useAuthenticator from '../hourlyAuth'
import {Route, Navigate} from 'react-router-dom'
import Authentication from '../authentication'

/**
 * Represents a route or chain of routes protected by the
 * authentication state.
 * @author Chris Rinaldi
 * @param {JSX.Element} element represents the inner component to render
 * @param {any} props represents the props to be passed
 */
const ProtectedRoute = ({element, ...props}) => {

    // Store the auth state. Pass in JWT as credentials.
    let isAuthorized = useAuthenticator({})

    // Conditionally, if the user is authenticated, display the
    // component. Otherwise, redirect to the login screen.
    return (
        isAuthorized ? element : <Navigate to={{
                                    pathname: '/login',
                                    state: {
                                        from: props.location
                                    }
                                }}/>
    )
}

export default ProtectedRoute