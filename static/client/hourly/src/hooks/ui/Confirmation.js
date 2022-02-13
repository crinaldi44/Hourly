import { React, useState } from "react"
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogContentText,
    DialogActions,
    Button
} from '@mui/material'

/**
 * The useConfirmationDialog hook represents a confirmation to allow
 * us to display a confirmation message to the user. Generally, these
 * types of messages are of the form 'are you sure you wish to [...]?'
 * or similar.
 * 
 * It is generally wiser to only use this hook for 'quicker' situations
 * where a quick confirmation response is needed.
 * @param {Function} onConfirmCallback represents the callback to invoke after confirmation
 * @author Chris Rinaldi
 * @see https://mui.com/components/dialogs/
 */
const useConfirmationDialog = (onConfirmCallback) => {

    /**
     * Stores the open/close state of the modal.
     */
    const [open, setOpen] = useState(false);

    /**
     * Represents the message displayed within the dialog
     * modal.
     */
    const [message, setMessage] = useState("");

    /**
     * Represents the title of the dialog.
     */
    const [title, setTitle] = useState("Confirm Action");

    /**
     * Handles action taken when the dialog modal should
     * close.
     */
    const handleClose = () => {
        setOpen(false)
    }

    /**
     * Handles action taken on confirm.
     */
    const handleConfirm = () => {
        if (onConfirmCallback) {
            onConfirmCallback();
        }
        handleClose();
    }

    /**
     * Represents the alert element.
     */
    const ConfirmationDialog = 
    ( <Dialog open={open} onClose={handleClose} aria-labelledby="alert-dialog-title" aria-describedby="alert-dialog-description">
                <DialogTitle id="alert-dialog-title">
                {title}
                </DialogTitle>
                <DialogContent>
                <DialogContentText id="alert-dialog-description">
                    {message}
                </DialogContentText>
                </DialogContent>
                <DialogActions>
                <Button onClick={handleClose}>Cancel</Button>
                <Button onClick={handleConfirm} autoFocus>
                    Confirm
                </Button>
                </DialogActions>
            </Dialog>
    )

    return [setOpen, setTitle, setMessage, ConfirmationDialog]

}

export default useConfirmationDialog;