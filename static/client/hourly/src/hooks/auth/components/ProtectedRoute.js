import useAuthenticator from '../hourlyAuth'
import { useNavigate } from 'react-router-dom'
import {Route, Navigate} from 'react-router-dom'
import Authentication from '../authentication'
import React, {useEffect} from 'react'

/**
 * Represents a route or chain of routes protected by the
 * authentication state.
 * @author Chris Rinaldi
 * @param {JSX.Element} element represents the inner component to render
 * @param {any} props represents the props to be passed
 */
const ProtectedRoute = (props) => {

    /**
     * Represents the navigation hook.
     */
    const navigate = useNavigate()

    /**
     * On render/re-render, verify to ensure the user authentication token is still valid.
     */
    useEffect(() => {
        if (!Authentication.isAuthenticated()) {
            Authentication.deAuthenticate()
            navigate('/login')
        }   
    })
    

    // Conditionally, if the user is authenticated, display the
    // component. Otherwise, redirect to the login screen.
    return Authentication.isAuthenticated() ? props.element : <Navigate to={{
                                        pathname: '/login',
                                        state: {
                                            from: props.location
                                        }
                                    }}/>
}

export default ProtectedRoute