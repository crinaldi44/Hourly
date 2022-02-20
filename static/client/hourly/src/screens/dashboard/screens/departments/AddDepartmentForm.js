import React from 'react'

/**
 *  The AddDepartmentForm represents a component that
 *  allows a user to add a new department. 
 **/
const AddDepartmentForm = (props) => {

    /**
     * An object that represents the text to be inserted.
     */
    const [departmentBuilder, setDepartmentBuilder] = useState({
        department_name: '',
        manager_id: null,
    })

    /**
     * Handles changes in the value of any of the form fields.
     * @param {*} e represents the attached event
     */
    const handleChange = (e, ) => {
        
        e.preventDefault()
        
    }

    /**
     * Represents the JSX for the add department form.
     */
    const form = (
        <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Add Department</DialogTitle>
        <DialogContent>
          <DialogContentText>
            To add a new department, specify the name of the department and
            additionally, optionally specify the department's manager.
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
          <Button onClick={props.handleClose}>Submit</Button>
        </DialogActions>
      </Dialog>
    )

    return 
    (
        <div>{form}</div>
    )
}

/**
 *  The AddDepartmentForm represents a component that
 *  allows a user to add a new department. 
 **/
export default AddDepartmentForm