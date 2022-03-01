import {
    MenuItem,
    Select,
    Button,
    Box,
    Typography,
    Chip,
} from '@mui/material'
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { DataGrid, GridToolbar, GridToolbarContainer } from '@mui/x-data-grid'
import React, { useState, useEffect } from 'react'
import useQuery from '../../../../hooks/navigation/query'
import EmployeeService from '../../../../services/EmployeeService'


/**
 * The timesheet table represents timesheet data in a user-friendly
 * manner. Timesheets are grabbed based upon the query parameter
 * 'department' being filled out.
 */
const TimesheetTable = () => {

    /**
    * Represents the current query-parameterized URI location,
    * for purposes of filtering the data.
    */
    const query = useQuery()

    /**
     * Represents the clockin data.
     */
    const [clockins, setClockins] = useState([])

    /**
     * Represents the DataGrid columns.
     */
    const columns = [
        { field: 'id', headerName: 'Id', width: 90 },
        {
            field: 'clockin_time',
            headerName: 'Clock-in Time',
            width: 150,
            editable: true,
        },
        {
            field: 'clockout_time',
            headerName: 'Clock-out Time',
            width: 150,
            editable: true
        },
        {
            field: 'covid_status',
            headerName: 'COVID-19 Status',
            width: 150,
            editable: false,
            renderCell: (params) => {
                const chipColor = params.value === 'Healthy' ? '#64e064' : '#ff5c33'
                return <Chip variant='outlined' sx={{ height: '25px', minWidth: '90px', borderColor: chipColor, color: chipColor }} label={params.value} />
            }
        }
    ]

    /**
     * Fetches clockins for the specified department.
     */
    const fetchClockins = async () => {
        let result = await EmployeeService.getClockinsForDepartment(query.get('timesheet'))
        setClockins(result);
    }

    useEffect(() => {
        fetchClockins();
    }, [])

    return (<>
        <DataGrid />
    </>)

}

/**
 * The Timesheets screen presents a user first with a dropdown to select which department
 * they'd like to review payroll for and then allows them to submit to narrow their search.
 * 
 * At this time, not 'all' departments can be viewed.
 * @returns {JSX.Element}
 */
const Timesheets = () => {

    /**
     * Represents all departments.
     */
    const [departments, setDepartments] = useState([])

    /**
     * Represents the selected department, as per the select component.
     */
    const [selectedDepartment, setSelectedDepartment] = useState("none")

    /**
     * Represents the full JSON of the current department, determined when
     * the user selection is confirmed.
     */
    const [currentDepartment, setCurrentDepartment] = useState(null)

    /**
     * Represents the clockin dataset.
     */
    const [clockins, setClockins] = useState([])

    /**
     * Fetches all departments from the API.
     */
    const fetchDepartments = async () => {
        let result = await EmployeeService.getAllDepartments()
        setDepartments(result);
    }

    /**
     * Grabs clockin data from the API.
     */
    const fetchClockins = async (id) => {
        let result = await EmployeeService.getClockinsForDepartment(id)
        setClockins(result)
    }

    /**
     * On render, fetch all departments.
     */
    useEffect(() => {
        fetchDepartments()
    }, [])

    /**
     * Represents a controllable selector allowing the user to select
     * the department to run timesheets for.
     */
    const departmentSelector = (
        <Box sx={{ textAlign: 'left' }}>
            <Typography sx={{ mb: 2 }}>Select a department from the list below to retrieve the timesheets for that department.</Typography>
            <Select value={selectedDepartment} onChange={(e) => {
                e.preventDefault()
                console.log(e.target.value)
                setSelectedDepartment(e.target.value)
            }} sx={{ minWidth: '30%' }}>
                <MenuItem key="none" value="none"><i>Select department...</i></MenuItem>
                {departments.map(department => {
                    const id = department.department_id;
                    return (<MenuItem key={`${id}`} value={`${id}`}>{department.department_name}</MenuItem>)
                })}
            </Select>
            <Button sx={{ display: 'block', mt: 2 }} variant="contained" onClick={async () => {
                if (selectedDepartment !== 'none') {
                    await fetchClockins(selectedDepartment);
                    sessionStorage.setItem('dept', selectedDepartment)
                    setCurrentDepartment(departments.filter(dep => dep.department_id == selectedDepartment)[0])
                }
            }}>RUN TIMESHEETS</Button>
        </Box>
    )

    /**
     * Represents the array set of predefined columns for the
     * clockin dataset.
     */
    const columns = [
        {
            field: 'employee_id',
            headerName: 'Employee ID',
            width: 150,
        },
        {
            field: 'employee_name',
            headerName: 'Employee Name',
            width: 300,
        },
        {
          field: 'clockin_time',
          headerName: 'Clockin Time',
          width: 300,
          renderCell: (params) => {
            return <Chip variant='outlined' sx={{height: '25px', minWidth: '90px', borderColor: '#ff5c33', color: '#ff5c33'}} label={params.value}/>
          }
        },
        {
          field: 'clockout_time',
          headerName: 'Clockout Time',
          width: 300,
          editable: false,
          renderCell: (params) => {
              const chipColor = params.value ? '#ff5c33' : '#64e064'
            return <Chip variant='outlined' sx={{height: '25px', minWidth: '90px', borderColor: chipColor, color: chipColor}} label={params.value || 'CLOCKED IN'}/>
          }
        },
        {
            headerName: 'Hours on Clock',
            width: 150,
            valueGetter: (params) =>
                `${params.row.clockin_time - params.row.clockout_time}`
        }
      ]

      const toolbar = () => {
          return (<GridToolbarContainer sx={{display: 'flex', justifyContent: 'space-between'}}>
              <GridToolbar/>
              <Button onClick={() => {
                  sessionStorage.removeItem('dep')
                  setCurrentDepartment()
                  }}>
                  <ArrowBackIcon fontSize='14px'/>
                  Back</Button>
          </GridToolbarContainer>)
      }

    return (
        !currentDepartment ? departmentSelector : <div style={{ height: '50vh', width: '100%', marginLeft: 'auto', marginRight: 'auto' }}>
            <DataGrid
            columns={columns}
            rows={clockins}
            checkboxSelection
            disableSelectionOnClick
            components={{Toolbar: toolbar}}
        />
        </div>
  )
}


export default Timesheets