import React from "react";
import NavigationBar from './components/NavigationBar'
import {Routes, Route} from 'react-router-dom'
import TimesheetsScreen from "./screens/TimesheetsScreen";
import ManageEmployeesScreen from "./screens/ManageEmployeesScreen";

/**
 * Represents the Dashboard Screen.
 * @constructor
 */
const Dashboard = () => {

    return (
        <>
            <NavigationBar/>
            <Routes>
                <Route path='/dashboard/home' exact component={TimesheetsScreen}/>
                <Route path='/dashboard/manage' exact component={ManageEmployeesScreen}/>
            </Routes>
        </>
    )

}

export default Dashboard