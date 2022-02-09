import React, {useState, useEffect} from 'react';
import useAuth from '../../../auth/hourlyAuth'
import axios from 'axios';

const ManageEmployeesScreen = () => {

  /**
   * Get the active credentials.
   */
  let creds = useAuth()


  /**
   * Fetches data from the database.
   */
  const fetchData = async () => {
    let result = await axios.get('/employees/')
  }


  /**
   * On render, we will fetch information about the employees as well
   * as their respective department and payroll info.
   */
  useEffect(() => {
  
    return () => {
      // Cleanup
    };
  }, []);
  

  return <div>Active employee: {creds['name']}</div>;
};

export default ManageEmployeesScreen;
