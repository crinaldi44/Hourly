import React, {useState, useEffect} from 'react'
import {
    ListItem, 
    Divider, 
    ListItemText, 
    List, 
    TextField, 
    Typography, 
    Stack,
    InputAdornment,
    InputLabel,
    FormControl,
    OutlinedInput,
    Box,
    Select,
    MenuItem,
} from '@mui/material';
import FullscreenDialog from '../../../components/FullscreenDialog'
import EmployeeService from '../../../services/EmployeeService'

/**
 * Adds an employee to the database.
 * @property open represents the state variable containing the 'open' state
 * @property handleClose represents the functionality on regular close
 * @property onConfirm represents what to do on confirm
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
        'department_id': 1,
        'pay_rate': 0.0,
        'covid_status': 'Healthy'
      })

    const resetEmployee = () => {
        setResponseObject({
            'name': '',
            'email': '',
            'password': '',
            'title': '',
            'department_id': 1,
            'pay_rate': 0.0,
            'covid_status': 'Healthy'
          })
    }

    /**
     * Represents all departments.
     */
    const [departments, setDepartments] = useState([])


    /**
     * Adds the employee to the DB.
     */
    const addEmployee = () => {
        EmployeeService.buildEmployee(responseObject).then(res => {
            props.onConfirm(res)
            if (res.status === 201) props.handleClose()
        })
        resetEmployee()
    }

    /**
     * Handles logic that takes place when a field changes.
     * @param e represents the default event
     * @param {String} property represents the property to change.
     */
    const handleChange = (e, property) => {
      setResponseObject({
          ...responseObject,
          [property]: e.target.value
      })
    }

    /**
     * On render, fetch all departments from the listing.
     */
    useEffect(() => {
        retrieveData()
    }, [])


    /**
     * Retrieves the data from the employee service.
     */
    async function retrieveData() {

        try {
            const data = await EmployeeService.getAllDepartments()
            setDepartments(data)
        } catch (err) {
            console.error(err)
        }
    }

    /**
     * Represents a mapping of department objects to a corresponding MenuItem
     * component.
     */
    const departmentMenuItems = (
        departments.map(department => (
            <MenuItem value={department.department_id}>{department.department_name}</MenuItem>
        ))
    )
    

  return (
        <FullscreenDialog open={props.open} title="Add Employee" handleClose={props.handleClose} handleConfirm={addEmployee}>
        <List>
        <Box sx={{width: '90%', ml: 'auto', mr: 'auto', mt: '1%'}}>
          <ListItem>
            <Typography>Employee information:</Typography>
          </ListItem>
          <Stack direction={'row'}>
            <ListItem sx={{width: '1fr'}}>
                <TextField  onChange={e => {handleChange(e, 'name')}} sx={{width: '100%'}} placeholder="Full name"/>
            </ListItem>
            <ListItem sx={{width: '1fr'}}>
                <TextField onChange={e => {handleChange(e, 'email')}} sx={{width: '100%'}} placeholder="Email address"/>
            </ListItem>
          </Stack>
            <Stack direction='row'>
                <ListItem>
                    <TextField sx={{width: '100%'}} placeholder="Title" onChange={e => {handleChange(e, 'title')}}/>
                </ListItem>
                <ListItem>
                    <TextField sx={{width: '100%'}} placeholder="Password" type='password' onChange={e => {handleChange(e, 'password')}}/>
                </ListItem>
            </Stack>
            <Stack direction='row'>
                <ListItem sx={{width: '1fr'}}>
                    <FormControl sx={{minWidth: '100%'}}>
                        <InputLabel>Department</InputLabel>
                        <Select
                        label="Department"
                        onChange={e => {handleChange(e, 'department_id')}}
                        value={responseObject.department_id}
                        >
                        {departmentMenuItems}
                        </Select>
                    </FormControl>
                </ListItem>
            <ListItem sx={{width: '1fr'}}>
                <FormControl fullWidth sx={{minWidth: 300}}>
                    <InputLabel htmlFor="outlined-adornment-amount">Pay Rate</InputLabel>
                    <OutlinedInput
                        id="outlined-adornment-amount"
                        onChange={e => {handleChange(e, 'pay_rate')}}
                        startAdornment={<InputAdornment position="start">$</InputAdornment>}
                        label="Amount"
                        placeholder='0.00'
                        type="number"
                        step="0.01"
                    />
                </FormControl>
            </ListItem>
          </Stack>
        </Box>
        </List>
      </FullscreenDialog>
  )
}

/**
 * 
 * 
 * */
export default AddEmployeesDialog