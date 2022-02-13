import React, { useState } from 'react';
import {
    Tab,
    Box,
    Typography,
} from '@mui/material'
import TabContext from '@mui/lab/TabContext';
import TabList from '@mui/lab/TabList';
import TabPanel from '@mui/lab/TabPanel';
import PropTypes from 'prop-types'

/**
 * A TabView presents children in a tabbable interface. Supports
 * an arbitrary number of tabs by mapping each wrapped child to
 * both a respective Tab and TabPanel.
 * 
 * In order to ensure that a child receives a proper label, simply
 * specify "label" as a prop in your child component containing a 
 * string denoting the tab's name.
 * @param {*} props represents the props passed
 * @property sx This component accepts a JSON-based stylesheet prop
 * @returns {JSX.Element}
 * @see https://mui.com/components/tabs/
 */
const TabView = (props) => {

    /**
     * Handles action taken when the tab should change.
     * @param {*} event 
     * @param {*} newValue 
     */
    const handleChange = (event, newValue) => {
        setCurrentTab(newValue);
    };

    /**
     * Represents the currently selected tab.
     */
    const [currentTab, setCurrentTab] = useState(0);

    /**
     * Represents the tabs corresponding to a child.
     */
    const tabs = props.children.map(child => (
        <Tab label={child.props.label || "Tab"} value={props.children.indexOf(child)}/>
    ));

    /**
     * Represents the panels.
     */
    const panels = props.children.map(child => (
        <TabPanel value={props.children.indexOf(child)}>{child}</TabPanel>
    ));

    return (
        <Box sx={{ width: '100%', typography: 'body1', borderRadius: '2px', backgroundColor: 'white', ...props.sx }}>
        <TabContext value={currentTab}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <TabList onChange={handleChange} aria-label="lab API tabs example">
                {tabs}
            </TabList>
            </Box>
            {panels}
        </TabContext>
        </Box>
    );
};

/**
 * A TabView presents children in a tabbable interface.
 * @returns {JSX.Element}
 */
export default TabView;
