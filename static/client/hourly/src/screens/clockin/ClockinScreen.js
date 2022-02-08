import React from "react";
import './ClockinScreen.css'
import Button from "../../components/Button";
import Clock from "./components/Clock";
import {Link} from "react-router-dom";
import ToastAlert from '../../components/ToastAlert'
import Logo from '../../assets/images/logo-light.png'
import axios from "axios";

/**
 * Represents the first screen displayed when the user navigates to the application.
 * @constructor
 */
class ClockinScreen extends React.Component {

    /**
     * Constructs a new ClockinScreen component.
     * @param props
     */
    constructor(props) {
        super(props);
        this.state = {
            alertActive: false,
            employeeId: '',
            alertMessage: '',
            alertSeverity: ''
        }
    }

    /**
     * Represents action taken when the alert is closed.
     */
    handleClose = (event, reason) => {

        // Ignore click-away events.
        if (reason === 'clickaway') return;

        // Invoke the cleanup callback function, if any.
        if (this.props.cleanup) {
         this.props.cleanup();
        }

        this.setState({
            ...this.state,
            alertActive: false
        })

    }

    /**
     * Opens the alert.
     */
    openAlert = () => {
        this.setState({
            ...this.state,
            alertActive: true
        })
    }

    /**
     * Logs a time clock for an employee.
     * @return {Promise<void>}
     */
    punchInOut = async () => {

        let result;

        try {
            result = await axios.post(`/employees/${this.state.employeeId}/clockin`)
        } catch (err) {
            if (err.response) result = err.response
            else {
                this.setState({
                    ...this.state,
                    alertMessage: 'An unknown error occurred! Please contact support for details.',
                    alertSeverity: 'error'
                })
                this.openAlert()
                return
            }
        }
        this.setState({
            ...this.state,
            alertMessage: result.data.message,
            alertSeverity: (result.status === 201 || result.status === 200) ? 'success' : 'error'
        })
        document.getElementById('clockin').value = "" // Clear the input field
        this.openAlert(); // Present the alert to the user.
    }

    /**
     * Handles action taken when the input should change. Tracks
     * the employeeId state variable for use with the clockin
     * system.
     * @param e
     */
    handleChange = (e) => {
        this.setState({
            ...this.state,
            employeeId: e.target.value
        })
    }


    /**
     * Renders JSX as HTML on the screen.
     * @returns {JSX.Element}
     */
    render() {
        return (
            <div className='clockin-container'>
                <img src={Logo} className='logo-clockin'/>
                <Clock/>
                <input id="clockin"
                       type="password"
                       className='employee_code-input'
                       placeholder='Enter your 6-digit employee ID.'
                       onChange={this.handleChange}/>
                <Button label='CLOCK IN / OUT' onClick={this.punchInOut}/>
                <p className='login_prompt'>Access your dashboard. <Link to='/login'>Click here</Link> to login.</p>
                <ToastAlert open={this.state.alertActive} onClose={this.handleClose} message={this.state.alertMessage} severity={this.state.alertSeverity}/>
            </div>
        )
    }

}

export default ClockinScreen