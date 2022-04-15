import React, { useState, useEffect } from 'react';
import Header from "../components/Header";
import {
  Grid,
  Typography,
  Card,
  CardContent,
  Container,
  CardActions,
  Button,
} from '@mui/material'
import TabView from '../components/TabView'
import Authentication from '../../../hooks/auth/authentication'
import EmployeeService from '../../../services/EmployeeService';
import { ChargingStation, LeaderboardTwoTone, RequestPage } from '@mui/icons-material';
import DiagramImage from '../../../assets/images/diagram.png'

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
    <Container maxWidth={'xl'}>
      <Grid container direction={'row'} spacing={2}>
        <Grid item xs={6}>
      <Card square sx={{textAlign: 'left', mt: 5, height: '90%'}}>
                <CardContent>
                  <LeaderboardTwoTone color='primary'/>
                  <Typography variant='h5'>
                    Overview
                  </Typography>
                  <Typography variant='body2' color='textSecondary'>Application Structure</Typography>
                  <br/>
                  <Typography maxWidth={800}>
                    This application is a "full-stack" web application. The frontend is a React application wrapped with a component library called Material-UI (Google theme). The backend is Python-based and is run on a library called Flask. The Flask backend uses a library called SQLAlchemy to connect to a MySQL database.
                  </Typography>
                  <br/>
                </CardContent>
                <CardActions>
                  <Button variant='outlined'>View Host</Button>
                </CardActions>
      </Card>
      </Grid>
      <Grid item xs={6}>
      <Card square sx={{textAlign: 'left', mt: 5, height: '90%'}}>
                <CardContent>
                  <RequestPage color='primary'/>
                  <Typography variant='h5'>
                    Walkthrough
                  </Typography>
                  <Typography variant='body2' color='textSecondary'>How does it work?</Typography>
                  <br/>
                  <Typography maxWidth={800}>
                    Like any web app, your browser will request the entire "front end" (React app) from the server, which will send it over to us. Then, whenever you interact with the application, we make a request to the server to either perform some business logic or interact with the database. The server will perform the request and send back a response, which is used to display the data.
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button variant='outlined'>See In Action</Button>
                </CardActions>
      </Card>
      </Grid>
      <Grid item xs={12}>
      <Card square sx={{textAlign: 'left'}}>
                <CardContent>
                  <ChargingStation color='primary'/>
                  <Typography variant='h5'>
                    Diagram
                  </Typography>
                  <Typography variant='body2' color='textSecondary'>View Below</Typography>
                  <br/>
                  <Typography maxWidth={800}>
                    Below is a diagram of the request-response cycle of the application:
                  </Typography>
                  <img src={DiagramImage} width={550} height={150}/>
                </CardContent>
      </Card>
      </Grid>
      </Grid>
      </Container>
    </>);

};

export default DashboardHomeScreen;
