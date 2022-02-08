import React from "react";
import LoginForm from "./components/LoginForm";
import './LoginScreen.css'
import {Link} from 'react-router-dom'

/**
 * Represents the Login Screen.
 * @constructor
 */
const LoginScreen = () => {

    return (
        <div className='login-screen_container'>
            <LoginForm/>
            <p className='login-back-prompt'><Link to='/'>Click here</Link> to return to clock-in screen.</p>
        </div>
    )

}

export default LoginScreen;