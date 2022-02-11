import React, {useState, useEffect, useCallback} from 'react';
import useAuth from '../../../auth/hourlyAuth'
import axios from 'axios';
import { Button, Snackbar, ListItem, Divider, ListItemText, List, TextField } from '@mui/material';
import { DataGrid, GridToolbar } from '@mui/x-data-grid';
import './ManageEmployeeScreen.css'
import FullscreenDialog from '../components/FullscreenDialog';

/**
 * The ManageEmployesScreen is meant to display a table of all active employees
 * and allow to edit existing employees. It features an 'add employee' button which
 * presents a modal that allows the user to import a new employee.
 * 
 * @returns {JSX.Element}
 */
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
    axios.get('/employees').then(res => setDataSet(res.data)).finally(setLoaded(true))
  }

  /**
   * Represents the data set for the employee's respective department.
   */
  const [dataSet, setDataSet] = useState([])

  /**
   * Represents whether the data has been loaded into memory.
   */
  const [loaded, setLoaded] = useState(false)

  /**
   * Represents whether the add dialog is open.
   */
  const [addOpen, setAddOpen] = useState(false)

  /**
   * Handles action taken when the add modal closes.
   */
  const handleCloseAdd = () => {
    setAddOpen(false);
  }

  /**
   * Handles action taken when the modal opens.
   */
  const handleOpenAdd = () => {
    setAddOpen(true)
  }


  /**
   * On render, we will fetch information about the employees as well
   * as their respective department and payroll info.
   */
  useEffect(() => {
    fetchData()
  }, []);

  const columns = [
    { field: 'id', headerName: 'Id', width: 90 },
    {
        field: 'name',
        headerName: 'Name',
        width: 150,
        editable: true,
    },
    {
        field: 'title',
        headerName: 'Title',
        width: 300,
        editable: true,
    },
    {
      field: "department",
      headerName: 'Department',
      width: 150,
      editable: false,
      valueGetter: (params) =>
        `${params.row.department.department_name}`,
    },
    {
      field: 'reportsTo',
      headerName: 'Reports To',
      width: 150,
      editable: false,
      valueGetter: (params) =>
        `${params.row.department.manager_id}`
    },
    {
      field: 'pay_rate',
      headerName: 'Pay Rate',
      width: 150,
      editable: false,
    },
    {
      field: 'covid_status',
      headerName: 'COVID-19 Status',
      width: 150,
      editable: false,
    }
  ]

  return (
    <>
      <div className='manage-header'>
        <div className='manage-add'>
          <h1 style={{display: 'inline-block', textAlign: 'left', color: 'var(--primary-dark)'}}>Manage Employees</h1>
          <Button onClick={handleOpenAdd}>+ Add Employee</Button>
        </div>

      </div>
      <div style={{ height: '70%', width: '95%', marginLeft: 'auto', marginRight: 'auto' }}>
      {!loaded ? <div></div> : <DataGrid rows={dataSet}
              columns={columns}
              pageSize={15}
              rowsPerPageOptions={[5]}
              checkboxSelection
              disableSelectionOnClick
              components={{Toolbar: GridToolbar}} />}
      </div>
      <FullscreenDialog open={addOpen} title="Add Employee" handleClose={handleCloseAdd}>
        <List>
          <ListItem>
            <TextField sx={{width: '30%', ml: '30px'}} placeholder="Full name"/>
          </ListItem>
          <Divider />
          <ListItem>
            <TextField sx={{width: '90%', ml: 'auto', mr: 'auto'}} placeholder="Email address"/>
          </ListItem>
          <Divider />
          <ListItem>
            <TextField sx={{width: '90%', ml: 'auto', mr: 'auto'}} placeholder="Email address"/>
          </ListItem>
          <Divider />
          <ListItem>
            <TextField sx={{width: '90%', ml: 'auto', mr: 'auto'}} placeholder="Full name"/>
          </ListItem>
        </List>
      </FullscreenDialog>
    </>
  )
};

export default ManageEmployeesScreen;
