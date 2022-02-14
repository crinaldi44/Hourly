import {
    Typography,
    Box,
} from '@mui/material';
import {Accordion, AccordionSummary, AccordionDetails} from "../components/AccordionView";
import {ExpandMore} from "@mui/icons-material";
import React, {useEffect, useState} from 'react';
import Header from '../components/Header';
import TabView from '../components/TabView';

/**
 * Represents the departments screen.
 * @returns {JSX.Element}
 */
const DepartmentsScreen = () => {

    /**
     * Represents a variable that stores each department.
     */
    const [departments, setDepartments] = useState([])

    /**
     * Represents action taken on render.
     */
    useEffect(() => {

    }, [])

  return <>
    <Header>Manage Departments</Header>
    <TabView sx={{width: '95%', ml: 'auto', mr: 'auto'}}>
        <Box label='Departments'>
            <Accordion>
                <AccordionSummary
                    expandIcon={<ExpandMore />}>
                    <Typography>Management</Typography>
                </AccordionSummary>
                <AccordionDetails></AccordionDetails>
            </Accordion>
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
