import React from "react";
import NavigationBar from './components/NavigationBar'
import {Routes, Route, Navigate } from 'react-router-dom'
import DashboardHomeScreen from "./screens/DashboardHomeScreen";
import ManageEmployeesScreen from "./screens/ManageEmployeesScreen";
import ProtectedRoute from '../../hooks/auth/components/ProtectedRoute'
import DepartmentsScreen from "./screens/departments/DepartmentsScreen";
import AccountSettingsScreen from "./screens/settings/AccountSettingsScreen";

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
                        <Route path='/' exact element={<DashboardHomeScreen/>}/>
                        <Route path='/departments' exact element={<DepartmentsScreen/>}/>
                        <Route path='/manage' exact element={<ProtectedRoute element={<ManageEmployeesScreen/>}/>}/>
                        <Route path='/settings' exact element={<ProtectedRoute element={<AccountSettingsScreen/>}/>}/>
                    </Routes>
                </div>
        </div>
    )

}

export default Dashboard