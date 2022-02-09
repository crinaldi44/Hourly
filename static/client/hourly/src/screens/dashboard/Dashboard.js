import React from "react";
import NavigationBar from './components/NavigationBar'
import {Routes, Route, Navigate, useLocation} from 'react-router-dom'
import TimesheetsScreen from "./screens/TimesheetsScreen";
import ManageEmployeesScreen from "./screens/ManageEmployeesScreen";

/**
 * Represents the Dashboard Screen.
 * @constructor
 */
const Dashboard = (props) => {

    /**
     * Represents the default Route. Should the user attempt to route to
     * any route that is not specified, we will reroute them to the dashboard.
     */
    const defaultRoute = <Navigate to={{
        pathname: '/dashboard',
    }}/>

    return (
        <div style={{height: '100vh', display: 'flex', flexDirection: 'column'}}>
            <NavigationBar sx={{position: 'sticky'}}/>
                <div style={{flexGrow: 1, backgroundColor: 'var(--offwhite)'}}>
                    <Routes>
                        <Route path='/*' element={defaultRoute}/>
                        <Route path='/' exact element={<TimesheetsScreen/>}/>
                        <Route path='/manage' exact element={<ManageEmployeesScreen/>}/>
                    </Routes>
                </div>
        </div>
    )

}

export default Dashboard