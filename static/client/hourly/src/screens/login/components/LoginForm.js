import React from "react";
import './LoginForm.css'
import Logo from '../../../assets/images/logo-clock.png'

/**
 * Represents the login screen.
 * @constructor
 * @see https://fontawesome.com/v5/cheatsheet
 */
const LoginForm = () => {

    return (
        <form method='POST' className='login-form'>
            <div className='form-logo-wrapper'>
                <img className='form-logo' src={Logo} alt='Logo'/>
                <h2>Log In</h2>
            </div>
            <div style={{marginTop: '15px'}}>
                <span className='input-wrapper' data-label='&#xf007;'>
                    <input id='employee' className='login-input' type='text' name='id' placeholder='Enter your 6-digit code.'/>
                </span>
                <span className='input-wrapper' data-label='&#xf023;'>
                    <input className='login-input' type='password' name='password' placeholder='Enter your password.'/>
                </span>
                <p className='form-header-text'>To request access to this portal, please contact Human Resources.</p>
            </div>
            <input className='login-input' type='submit' value={'LOG IN'}/>
        </form>
    )

}


export default LoginForm;