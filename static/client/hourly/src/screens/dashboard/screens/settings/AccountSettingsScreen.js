import { Button, Card, CardActionArea, CardActions, CardHeader, TextField, Typography, Grid, Box } from '@mui/material'
import React, { useState, useEffect } from 'react'
import Authentication from '../../../../hooks/auth/authentication'
import EmployeeService from '../../../../services/EmployeeService'
import Header from '../../components/Header'
import useConfirmationDialog from '../../../../hooks/ui/Confirmation'

/**
 * Represents the account settings screen.
 **/ 
const AccountSettingsScreen = () => {

    /**
     * Represents the active user.
     */
    const [user, setUser] = useState({})

    /**
     * Gets the active user.
     */
    const getActiveUser = () => {
        console.log(Authentication.getActiveEmployee());
    }

    useEffect(() => {
      getActiveUser();
    }, [])

    const [setOpen, setTitle, setMessage, ConfirmationDialog] = useConfirmationDialog(() => {console.log('test')});
    
    /**
     * Represents the styling for each component.
     */
    const styles = {
        mainSettings: {
            maxWidth: '95%',
            ml: 'auto',
            mr: 'auto',
            mt: '15px'
        },
        sectionHeader: {
            ml: 4,
            mt: '20px',
            textAlign: 'left',
            color: '#636363'
        },
        settingsDescription: {
            textAlign: 'left'
        }
    }

    /**
     * Handles action taken when save is clicked.
     */
    const handleSave = async () => {
        // TODO: Implement API call.
    }

    /**
     * Handles resetting.
     */
    const handleReset = () => {
        setTitle('Are you sure?')
        setMessage('These changes may not be immediately reversed. You can change your settings at any time using the account settings panel.')
        setOpen(true);
    }

  return (
      <>
        <Header action={<Button variant='contained' onClick={handleReset}>Reset to Defaults</Button>}>
            Settings
        </Header>
        <Typography sx={styles.sectionHeader}><strong>Account</strong></Typography>
        <Card sx={styles.mainSettings}>
                <CardHeader>
                    <Typography color="primary">My Profile</Typography>
                </CardHeader>
                <Grid container>
                    <Grid item sx={styles.settingsDescription}>
                        <Typography>
                            <strong>Password</strong>
                            <br/>
                            Edit
                        </Typography>
                    </Grid>
                </Grid>
                <Typography>Edit your profile, including your password, avatar, and more.</Typography>
                <TextField type="password" placeholder='Enter updated password'/>
                <CardActions>
                    <Button>Save</Button>
                </CardActions>
        </Card>
        <Typography sx={styles.sectionHeader}><strong>Appearance</strong></Typography>
        <Card sx={styles.mainSettings}>
            <CardActions>
                <Button>Save</Button>
            </CardActions>
        </Card>
        {ConfirmationDialog}
      </>
  )
}

/**
 * Represents the account settings screen.
 **/ 
export default AccountSettingsScreen