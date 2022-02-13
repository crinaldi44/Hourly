import {React, useState} from 'react'
import ToastAlert from "../../components/ToastAlert"

/**
 * A hook that allows us to write a declare-once Toast-style alert and 
 * provides mutator methods for the open, message, and severity states as
 * well as the corresponding JSX element.
 * @param {Function} onCloseCallback You can specify any cleanup or 'on close' functionality that must be performed
 * @returns {Array} [message, setMessage, setOpen, Toast] an array of four reusable components.
 * @author Chris Rinaldi
 * @see <ToastAlert>
 */
const useToast = (onCloseCallback) => {

    /**
     * Represents whether the Toast is open.
     */
    const [open, setOpen] = useState(false)

    /**
     * Represents the message.
     */
    const [message, setMessage] = useState("")

    /**
     * Represents the severity of the Toast. By default,
     * displays with 'info' severity level.
     */
    const [severity, setSeverity] = useState("info")

    /**
     * Represents a function that handles the close functionality. Invokes
     * the on close callback specified in the params, then sets the Toast
     * to closed.
     */
     const handleClose = (event, reason) => {
         if (reason === 'clickaway') {
             return;
         }
         if (onCloseCallback) onCloseCallback();
         setOpen(false);
    }

    /**
     * Stores a ToastAlert JSX component.
     */
    const Toast = (
        <ToastAlert open={open} severity={severity} onClose={handleClose} message={message}/>
    )

    /**
     * Return the components.
     */
    return [setMessage, setOpen, setSeverity, Toast]
}

export default useToast