import React, { useState, useEffect } from 'react';
import Header from "../components/Header";
import {
  Paper,
  Grid,
  Typography,
  Box,
} from '@mui/material'
import TabView from '../components/TabView'
import Authentication from '../../../hooks/auth/authentication'
import EmployeeService from '../../../services/EmployeeService';

/**
 * Represents the Dashboard Home Screen.
 * @returns {JSX.Element}
 */
const DashboardHomeScreen = () => {

  const dashPaper = {
    height: 200,
    width: '1fr',
    borderWidth: '2px'
  }

  /**
   * Represents the payroll API object in dollars. The object
   * contains keys 'goal' and 'actual'.
   */
  const [payrollDollars, setPayrollDollars] = useState(0)

  /**
   * Represents the payroll API object in hours. The object
   * contains keys 'goal' and 'actual'.
   */
  const [payrollHours, setPayrollHours] = useState(0);

  /**
   * Fetches necessary data from the database.
   */
  const fetchData = async () => {

    // Retrieve the actual amount from the API.
    let payroll = await EmployeeService.getDepartmentHours(Authentication.getActiveEmployee().department_id)
    
    if (payroll) {
        setPayrollHours({
        ...payrollHours,
        actual: payroll
      })
    } else {
      setPayrollHours({
        ...payrollHours,
        actual: '0'
      })
    }

    // Retrieve the goal from the API.
    let budgetObj = await EmployeeService.getBudget(Authentication.getActiveEmployee().department_id)

    // If the budget goal exists, set it, else set to '*'.
    if (budgetObj) {
      setPayrollHours({
        ...payrollHours,
        goal: budgetObj
      })
    } else {
      setPayrollHours({
        ...payrollHours,
        goal: '*'
      })
    }
  }

  useEffect(() => {
    fetchData();
  }, [])
  


  return (<>
      <Grid container direction='column' pt={5} height={'100%'}>
        <Grid item>
          <Grid container width='97%' columnGap={2} margin="auto" direction='row'>
            <Grid item xs>
              <Paper sx={{borderRadius: 0.3, pl: 2, pt: 2, pr: 2}}>
                <Typography fontWeight={600} textAlign='left'>Pay Period Overview</Typography>
                <Grid container direction="row" justifyContent='space-between' p={2}>
                  <Grid item>
                    <Typography>Budget Amount</Typography>
                    <Typography>$2,450/$3,500</Typography>
                  </Grid>
                  <Grid item>
                    <Typography>Hourly Amount</Typography>
                    <Typography>{`${payrollHours.actual || '0'}/${payrollHours.goal}`}</Typography>
                  </Grid>
                  <Grid item>
                    <Typography>Shifts Remaining</Typography>
                  </Grid>
                </Grid>
              </Paper>
            </Grid>
            <Grid item xs={5}>
              <Paper sx={{borderRadius: 0.3}}>
                <Typography color="var(--primary-dark)" fontWeight={600} textAlign='left'>Employee Timesheets</Typography>
              </Paper>
            </Grid>
          </Grid>
        </Grid>
        <Grid item>
          <Paper sx={{width: '97%', m: 'auto'}}>
              <TabView>
                <Box label="Payroll"></Box>
                <Box label="Timesheets"></Box>
              </TabView>
          </Paper>
        </Grid>
      </Grid>
    </>);

};

export default DashboardHomeScreen;
