import {
    Typography,
    Box,
    Button
} from '@mui/material';
import React from 'react';
import Header from '../../components/Header';
import TabView from '../../components/TabView';
import Departments from './Departments';

/**
 * Represents the departments screen.
 * @returns {JSX.Element}
 */
const DepartmentsScreen = () => {

  return <>
    <Header
        action={<Button variant='contained'>Add Department</Button>}
    >Manage Departments</Header>
    <TabView sx={{width: '95%', ml: 'auto', mr: 'auto'}}>
        <Box label='Departments'>
            <Departments/>
        </Box>
        <Typography label="Timesheets"></Typography>
    </TabView>
  </>;

};

/**
 * Represents the departments screen.
 * @returns {JSX.Element}
 */
export default DepartmentsScreen;
