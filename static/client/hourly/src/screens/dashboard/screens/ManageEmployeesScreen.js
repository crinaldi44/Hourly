import React, {useState, useEffect} from 'react';
import useAuth from '../../../auth/hourlyAuth'
import axios from 'axios';
import DataTable from "../components/DataTable";

const ManageEmployeesScreen = () => {

  /**
   * Get the active credentials.
   */
  let creds = useAuth()


  /**
   * Fetches data from the database, sets the dataSet state
   * variable to the promisified data.
   */
  const fetchData = () => {
    axios.get('/employees').then(data => setDataSet(data))
  }

  /**
   * Represents the data set for the employee's respective department.
   */
  const [dataSet, setDataSet] = useState([])


  /**
   * On render, we will fetch information about the employees as well
   * as their respective department and payroll info.
   */
  useEffect(() => {
    fetchData()
  }, []);
  

  return (
    <>
      <h1 style={{textAlign: 'left', margin: '30px', color: 'var(--primary-dark)'}}>Viewing Department: {creds['department_name']}</h1>
      <DataTable data={dataSet} headerAutoGenerate />
    </>
  )
};

export default ManageEmployeesScreen;
