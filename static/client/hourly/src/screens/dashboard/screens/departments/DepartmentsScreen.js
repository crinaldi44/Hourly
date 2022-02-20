import {
    Typography,
    Box,
    Button
} from '@mui/material';
import React, {useState} from 'react';
import Header from '../../components/Header';
import TabView from '../../components/TabView';
import AddDepartmentForm from './AddDepartmentForm';
import Departments from './Departments';

/**
 * Represents the departments screen.
 * @returns {JSX.Element}
 */
const DepartmentsScreen = () => {

  const [addDeptOpen, setAddDeptOpen] = useState(false);

  /**
   * Handles opening the add department modal.
   */
  const handleAddDeptOpen = () => {
    setAddDeptOpen(true)
  }

  const handleAddDeptClose = () => {
    setAddDeptOpen(false)
  }

  return <>
    <Header
        action={<Button variant='contained' onClick={handleAddDeptOpen}>Add Department</Button>}
    >Manage Departments</Header>
    <TabView sx={{width: '95%', ml: 'auto', mr: 'auto'}}>
        <Box label='Departments'>
            <Departments/>
        </Box>
        <Typography label="Timesheets"></Typography>
    </TabView>
    <AddDepartmentForm open={addDeptOpen} handleClose={handleAddDeptClose} />
  </>;

};

/**
 * Represents the departments screen.
 * @returns {JSX.Element}
 */
export default DepartmentsScreen;
