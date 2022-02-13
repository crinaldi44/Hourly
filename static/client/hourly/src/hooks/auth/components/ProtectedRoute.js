import useAuthenticator from '../hourlyAuth'
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
class ProtectedRoute extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            authenticated: Authentication.isAuthenticated()
        }
    }

    /**
     * Represents action taken should the component update. Each
     * render, we do a 'pulse' check to ensure that our auth state
     * is still intact.
     */
    componentDidUpdate() {
        this.setState({
            ...this.state,
            authenticated: Authentication.isAuthenticated()
        })
    }
    

    // Conditionally, if the user is authenticated, display the
    // component. Otherwise, redirect to the login screen.
    render() {
        return this.state.authenticated ? this.props.element : <Navigate to={{
                                        pathname: '/login',
                                        state: {
                                            from: this.props.location
                                        }
                                    }}/>  
    }
}

export default ProtectedRoute