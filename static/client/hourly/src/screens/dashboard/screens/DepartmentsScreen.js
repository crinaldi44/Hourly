import { Typography, Box } from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import React from 'react';
import Header from '../components/Header';
import TabView from '../components/TabView';

/**
 * Represents the departments screen.
 * @returns {JSX.Element}
 */
const DepartmentsScreen = () => {

  return <>
    <Header>Manage Departments</Header>
    <TabView sx={{width: '95%', ml: 'auto', mr: 'auto'}}>
        <Typography label="Departments"></Typography>
        <Typography label="Timesheets"></Typography>
    </TabView>
  </>;

};

/**
 * Represents the departments screen.
 * @returns {JSX.Element}
 */
export default DepartmentsScreen;
