import React, {useState} from 'react'
import {
  Dialog,
  DialogTitle,
  DialogContent,
  Button,
  DialogActions,
  TextField,
  DialogContentText
} from '@mui/material'
import EmployeeService from '../../../../services/EmployeeService'

/**
 *  The AddDepartmentForm represents a component that
 *  allows a user to add a new department. 
 **/
const AddDepartmentForm = (props) => {

    /**
     * An object that represents the text to be inserted.
     */
    const [departmentName, setDepartmentName] = useState('')

    /**
     * Handles changes in the value of any of the form fields.
     * @param {*} e represents the attached event
     * @param {string} field represents the field to change
     */
    const handleChange = (e) => {
        
        e.preventDefault()
        setDepartmentName(e.target.value)
        
    }

    const handleSubmit = async () => {
      await EmployeeService.addDepartment({'department_name': departmentName})
      props.handleClose();
    }

    /**
     * Represents the JSX for the add department form.
     */
    const form = (
        <Dialog open={props.open} onClose={props.handleClose}>
        <DialogTitle>Add Department</DialogTitle>
        <DialogContent>
          <DialogContentText>
            To add a new department, specify the name of the department. After,
            you may specify a manager after at least one employee has been added.
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            id="name"
            label="Department name"
            type="email"
            fullWidth
            variant="standard"
            onInput={e => {handleChange(e)}}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={props.handleClose}>Cancel</Button>
          <Button onClick={handleSubmit}>Submit</Button>
        </DialogActions>
      </Dialog>
    )

    return ( <>
              {form}
            </>
    )
}

/**
 *  The AddDepartmentForm represents a component that
 *  allows a user to add a new department. 
 **/
export default AddDepartmentForm