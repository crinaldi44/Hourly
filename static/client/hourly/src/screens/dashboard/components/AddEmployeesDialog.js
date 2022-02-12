import React, {useState, useEffect} from 'react'
import {ListItem, Divider, ListItemText, List, TextField, Typography } from '@mui/material';
import FullscreenDialog from '../../../components/FullscreenDialog'
import EmployeeService from '../../../api/EmployeeService'

/**
 * Adds an employee to the database.
 * @returns {JSX.Element}
 */
const AddEmployeesDialog = (props) => {


    /**
     * Builds a response.
     */
    const [responseObject, setResponseObject] = useState({
      'name': '',
      'email': '',
      'password': '',
      'title': '',
      'department': 0,
      'pay_rate': 0.0,
      'covid_status': 'Healthy'
    })

    /**
     * Adds the employee to the DB.
     */
    const addEmployee = () => {
        EmployeeService.buildEmployee(responseObject).catch(err => {
          // TODO: Perform some logic here.
        })

    }

    /**
     * Handles logic that takes place when a field changes.
     * @param e represents the default event
     * @param property represents the property to change.
     */
    const handleChange = (e, property) => {
      e.preventDefault()
      setResponseObject({
        ...responseObject,
        property: e.target.value()
      })
    }

  return (
        <FullscreenDialog open={props.open} title="Add Employee" handleClose={props.handleClose} handleConfirm={addEmployee}>
        <List>
          <ListItem>
            <Typography>Employee information:</Typography>
          </ListItem>
          <ListItem>
            <TextField onChange={e => {handleChange(e, 'name')}} sx={{width: '30%', ml: '30px', mb: '30px'}} placeholder="Full name"/>
          </ListItem>
          <ListItem>
            <TextField onChange={e => {handleChange(e, 'email')}} sx={{width: '30%', ml: '30px', mb: '30px'}} placeholder="Email address"/>
          </ListItem>
          <ListItem>
            <TextField sx={{width: '30%', ml: '30px', mb: '30px'}} placeholder="Email address"/>
          </ListItem>
          <ListItem>
            <TextField sx={{width: '30%', ml: '30px', mb: '30px'}} placeholder="Full name"/>
          </ListItem>
          <ListItem>

          </ListItem>
        </List>
      </FullscreenDialog>
  )
}

/**
 * 
 * 
 * */
export default AddEmployeesDialog