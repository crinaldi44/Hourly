import { Button, Card, CardActionArea, CardActions, CardHeader, TextField, Typography, Grid, Box, Switch } from '@mui/material'
import React, { useState, useEffect } from 'react'
import Authentication from '../../../../hooks/auth/authentication'
import EmployeeService from '../../../../services/EmployeeService'
import Header from '../../components/Header'
import useConfirmationDialog from '../../../../hooks/ui/Confirmation'
import UserPreferences from '../../../../services/settings/UserPreferences'
import ArrowForwardIosSharpIcon from '@mui/icons-material/ArrowForwardIosSharp';
import { styled } from '@mui/material'
import MuiAccordion from '@mui/material/Accordion';
import MuiAccordionSummary from '@mui/material/AccordionSummary';
import MuiAccordionDetails from '@mui/material/AccordionDetails';



/**
 * Represents the account settings screen.
 **/ 
const AccountSettingsScreen = () => {

    const Accordion = styled((props) => (
        <MuiAccordion disableGutters elevation={0} square {...props} />
      ))(({ theme }) => ({
        border: `1px solid ${theme.palette.divider}`,
        '&:not(:last-child)': {
          borderBottom: 0,
        },
        '&:before': {
          display: 'none',
        },
      }));
      
      const AccordionSummary = styled((props) => (
        <MuiAccordionSummary
          expandIcon={<ArrowForwardIosSharpIcon sx={{ fontSize: '0.9rem' }} />}
          {...props}
        />
      ))(({ theme }) => ({
        backgroundColor:
          theme.palette.mode === 'dark'
            ? 'rgba(255, 255, 255, .05)'
            : 'rgba(0, 0, 0, .03)',
        flexDirection: 'row-reverse',
        '& .MuiAccordionSummary-expandIconWrapper.Mui-expanded': {
          transform: 'rotate(90deg)',
        },
        '& .MuiAccordionSummary-content': {
          marginLeft: theme.spacing(1),
        },
      }));
      
      const AccordionDetails = styled(MuiAccordionDetails)(({ theme }) => ({
        padding: theme.spacing(2),
        borderTop: '1px solid rgba(0, 0, 0, .125)',
      }));

    /**
     * Represents the active user.
     */
    const [user, setUser] = useState({})

    /**
     * Represents whether the appbar switch is selected.
     */
    const [darkAppbar, setDarkAppbar] = useState(UserPreferences.get('appbarLight') || false)

    /**
     * Gets the active user.
     */
    const getActiveUser = async () => {
        let user = await EmployeeService.getEmployee(Authentication.getActiveEmployee().employee_id);
        setUser(user);
    }

    /**
     * Saves the employee to the database.
     */
    const save = async () => {
        let response = await EmployeeService.updateEmployee(user.employee_id, user);
    }

    // Represents action taken when the component re-renders.
    useEffect(() => {
      getActiveUser();
    }, [])

    /**
     * Creates and establishes a confirmation dialog.
     */
    const [setOpen, setTitle, setMessage, ConfirmationDialog] = useConfirmationDialog(() => {UserPreferences.reset();});
    
    
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
     * Handles action taken when settings are reset. Taps the local settings helper
     * class to reset all active settings.
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
                <Accordion>
                    <AccordionSummary>
                        <Typography sx={{mr: '1em', flexShrink: 0}}>Password</Typography>
                        <Typography sx={{color: 'text.secondary'}}>Enter a new password for your account.</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <TextField fullWidth variant='outlined' placeholder='Enter password...' type='password' />
                    </AccordionDetails>
                </Accordion>
                <Accordion>
                    <AccordionSummary>
                        <Typography sx={{mr: '1em', flexShrink: 0}}>Personal Info</Typography>
                        <Typography sx={{color: 'text.secondary'}}>Manage your personal information.</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <TextField fullWidth placeholder='Enter your name, first and last...'/>
                    </AccordionDetails>
                </Accordion>
                <CardActions>
                    <Button variant='contained'>Save</Button>
                </CardActions>
                </Card>
        <Typography sx={styles.sectionHeader}><strong>Appearance</strong></Typography>
        <Box sx={styles.mainSettings}>
            <Accordion expanded={true}>
                <AccordionSummary>
                    <Typography sx={{mr: '10em', flexShrink: 0}}>Use light appbar</Typography>
                    <Typography sx={{color: 'text.secondary'}}>Change to the light side.</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <Switch
                        checked={darkAppbar}
                        onChange={(event) => {
                            setDarkAppbar(event.target.checked)
                            UserPreferences.save('appbarLight', event.target.checked)
                        }}
                    />
                </AccordionDetails>
            </Accordion>
        </Box>
        {ConfirmationDialog}
      </>
  )
}

/**
 * Represents the account settings screen.
 **/ 
export default AccountSettingsScreen