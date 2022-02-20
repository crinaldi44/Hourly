import React, {useEffect} from "react";
import {useNavigate} from 'react-router-dom'
import Authentication from '../../hooks/auth/authentication'
import LoginForm from "./components/LoginForm";
import './LoginScreen.css'
import {Link} from 'react-router-dom'

/**
 * Represents the Login Screen.
 * @constructor
 */
const LoginScreen = () => {

    const navigate = useNavigate()

    // If the user is logged in, push nav to dashboard, otherwise
    // simply revoke the auth token.
    useEffect(() => {
      if (Authentication.isAuthenticated()) {
          navigate('/dashboard')
      } else {
          Authentication.deAuthenticate()
      }
    }, [])
    

    return (
        <div className='login-screen_container'>
            <LoginForm/>
            <p className='login-back-prompt'><Link to='/'>Click here</Link> to return to clock-in screen.</p>
        </div>
    )

}

export default LoginScreen;