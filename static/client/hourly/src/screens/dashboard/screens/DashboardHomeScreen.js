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

/**
 * Represents the Timesheets Screen.
 * @returns {JSX.Element}
 */
const DashboardHomeScreen = () => {

  const dashPaper = {
    height: 200,
    width: '1fr',
    borderWidth: '2px'
  }

  /**
   * Fetches necessary data from the database.
   */
  const fetchData = () => {

  }

  useEffect(() => {
    // TODO: Data retrieval logic.
  }, [])
  


  return (<>
      <Grid container direction='column' mt={5} height={'100%'}>
        <Grid item>
          <Grid container width='97%' columnGap={2} margin="auto" direction='row'>
            <Grid item xs>
              <Paper sx={{borderRadius: 0.5}}>
                <Typography fontWeight={600} textAlign='left'>Department Overview</Typography>
              </Paper>
            </Grid>
            <Grid item xs={5}>
              <Paper sx={{borderRadius: 0.5}}>
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
