import React, {useState, useEffect} from 'react'
import {ListItem, Divider, ListItemText, List, TextField, Typography } from '@mui/material';
import FullscreenDialog from '../../../components/FullscreenDialog'

/**
 * Adds an employee to the database.
 * @returns {JSX.Element}
 */
const AddEmployeesDialog = (props) => {


    /**
     * Builds a response.
     */
    const [responseBuilder, setResponseBuilder] = useState(null)

  return (
        <FullscreenDialog open={props.open} title="Add Employee" handleClose={props.handleClose}>
        <List>
          <ListItem>
            <Typography>Employee information:</Typography>
          </ListItem>
          <ListItem>
            <TextField sx={{width: '30%', ml: '30px', mb: '30px'}} placeholder="Full name"/>
          </ListItem>
          <ListItem>
            <TextField sx={{width: '30%', ml: '30px', mb: '30px'}} placeholder="Email address"/>
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