import React, {useState, useEffect } from 'react';
import axios from 'axios';
import { Button, IconButton } from '@mui/material';
import { DataGrid, GridToolbar, GridToolbarContainer } from '@mui/x-data-grid';
import './ManageEmployeeScreen.css'
import AddEmployeesDialog from '../components/AddEmployeesDialog';
import useToast from '../../../hooks/ui/Toast'
import EmployeeService from '../../../services/EmployeeService';
import useConfirmationDialog from '../../../hooks/ui/Confirmation';
import DeleteIcon from '@mui/icons-material/Delete';

/**
 * The ManageEmployesScreen is meant to display a table of all active employees
 * and allow to edit existing employees. It features an 'add employee' button which
 * presents a modal that allows the user to import a new employee.
 * 
 * @returns {JSX.Element}
 */
const ManageEmployeesScreen = () => {

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
   * Represents a listing of the currently selected employees,
   * obtained via onSelectionModelChanged.
   */
  const [selectedEmployees, setSelectedEmployees] = useState([])

  /**
   * Represents the toast.
   */
  const [setToastMessage, setToastOpen, setToastSeverity, Toast] = useToast()

  /**
   * Handles action taken when employees are selected and confirmed
   * for deletion.
   */
   const handleDeleteEmployees = async () => {
    setToastSeverity('info')
    let response = await Promise.all(selectedEmployees.map(employee => {
      return EmployeeService.deleteEmployee(employee)
    })).finally(() => {
        setSelectedEmployees([])
        setToastMessage('Action performed.')
        setToastOpen(true)
        setTimeout(() => {
          fetchData()
        }, 1500) // Refresh after 1500ms
      }
    )
  }

  /**
   * Represents the confirmation dialog.
   */
  const [setDialogOpen, setDialogTitle, setDialogMessage, ConfirmDialog] = useConfirmationDialog(handleDeleteEmployees)

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
   * Handles action taken when an employee is added.
   * @param response represents the response returned from building an employee
   */
  const handleAddEmployee = (response) => {
    if (response.status !== 201) {
      setToastSeverity('error')
    } else {
      setToastSeverity('success')
    }
    setToastMessage(response.data.message)
    setToastOpen(true)
    if (response.status === 201) {
      setTimeout(() => {
        fetchData()
      }, 1000)
    }
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

  const toolbar = () => {
    return ( <GridToolbarContainer>
        <GridToolbar/>
        { selectedEmployees.length > 0 ? <Button onClick={() => {
          setDialogMessage(`Are you sure you want to delete ${selectedEmployees.length} employees?`)
          setDialogOpen(true)
        }} startIcon={<DeleteIcon/>} variant="outlined" color='error'>
          Delete
        </Button> : null}
      </GridToolbarContainer>
    )
  } 

  return (
    <>
      <div className='manage-header'>
        <div className='manage-add'>
          <h1 style={{display: 'inline-block', textAlign: 'left', color: 'var(--primary-dark)'}}>Manage Employees</h1>
          <Button onClick={(handleOpenAdd)} variant="contained">+ Add Employee</Button>
        </div>

      </div>
      <div style={{ height: '70%', width: '95%', marginLeft: 'auto', marginRight: 'auto' }}>
      {!loaded ? <div></div> : <DataGrid rows={dataSet}
              columns={columns}
              pageSize={15}
              rowsPerPageOptions={[15]}
              checkboxSelection
              disableSelectionOnClick
              density='compact'
              sx={{backgroundColor: 'white'}}
              onSelectionModelChange={sel => {setSelectedEmployees(sel)}}
              components={{Toolbar: toolbar}} />}
      </div>
      <AddEmployeesDialog open={addOpen} handleClose={handleCloseAdd} onConfirm={res => {handleAddEmployee(res)}} />
      {Toast}
      {ConfirmDialog}
    </>
  )
};

export default ManageEmployeesScreen;
