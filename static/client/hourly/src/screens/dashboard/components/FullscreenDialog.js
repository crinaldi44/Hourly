import React from 'react';
import {Dialog, Toolbar, AppBar, Button, IconButton, Typography} from '@mui/material'
import CloseIcon from '@mui/icons-material/Close';

/**
 * A FullscreenDialog is a component that presents a fullscreen interface
 * prompting the user either for some info or presents a form. Use as follows:
 * 
 * <FullscreenDialog>
 * ...elements
 * </FullscreenDialog>
 * 
 * The intention of this component is to direct the focus of attention, particularly
 * when modifying or changing otherwise sensitive data.
 * @property open represents the variable storing the 'open' state of the dialog
 * @property handleClose represents action taken when the dialog closes
 * @property title represents the title of the dialog
 * @returns {JSX.Element}
 */
const FullscreenDialog = (props) => {

    return <Dialog
        fullScreen
        open={props.open}
        onClose={props.handleClose}
      >
        <AppBar sx={{ position: 'relative', backgroundColor: 'var(--primary-dark)' }}>
          <Toolbar>
            <IconButton
              edge="start"
              color="inherit"
              onClick={props.handleClose}
              aria-label="close"
            >
                <CloseIcon />
            </IconButton>
            <Typography sx={{ ml: 2, flex: 1 }} variant="h6" component="div">
                {props.title}
            </Typography>
            <Button autoFocus color="inherit" onClick={props.handleClose}>
              Confirm
            </Button>
          </Toolbar>
        </AppBar>
          {props.children}
      </Dialog>
};

/**
 * A FullscreenDialog is a component that presents a fullscreen interface
 * prompting the user either for some info or presents a form.
 * 
 * The intention of this component is to direct the focus of attention, particularly
 * when modifying or changing otherwise sensitive data.
 * @returns {JSX.Element}
 */
export default FullscreenDialog;
