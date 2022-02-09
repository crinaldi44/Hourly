import React from "react";
import {Alert, AlertTitle, Snackbar} from "@mui/material";

/**
 * An ToastAlert is a brief informational message displayed bottom left
 * to provide feedback for a user action. If an error occurs, more info
 * is required, or some other arbitrary condition, an ToastAlert should be used.
 *
 * By default, the ToastAlert provides a 6-second (6000ms) time clock before it 'expires'.
 *
 * Requirements: The parent component should contain the state of 'openness' of the ToastAlert
 * component, passed as props.
 * @property open - represents the state of open of the ToastAlert - REQUIRED
 * @property onClose - represents what happens when closed - REQUIRED
 * @property message - represents the message displayed by the alert - REQUIRED
 * @property title - represents the title of the alert, by default none provided - OPTIONAL
 * @property severity - represents the severity of the alert, by default info - OPTIONAL
 * @property cleanup - a callback function provided when the alert closes - OPTIONAL
 * @author Chris Rinaldi
 * @see https://mui.com/components/alert/
 */
class ToastAlert extends React.Component {

    /**
     * Constructs a new ToastAlert.
     * @param props
     */
    constructor(props) {
        super(props);
    }

    /**
     * Renders the JSX as html.
     * @returns {JSX.Element}
     */
    render() {
        return (
            <Snackbar open={this.props.open} autoHideDuration={3000} onClose={this.props.onClose}>
                <Alert severity={this.props.severity ? this.props.severity : 'info'}>
                    {this.props.title ? (<AlertTitle sx={{mb: '0', textAlign: 'left'}}><b>{this.props.title}</b></AlertTitle>) : null}
                    {this.props.message}
                </Alert>
            </Snackbar>
        )
    }

}

export default ToastAlert