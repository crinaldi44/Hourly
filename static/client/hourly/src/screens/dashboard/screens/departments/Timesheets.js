import { 
    MenuItem, 
    Select,
    Button,
    Box,
    Typography,
    Chip
} from '@mui/material'
import {DataGrid} from '@mui/x-data-grid'
import React, {useState, useEffect} from 'react'
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
            return <Chip variant='outlined' sx={{height: '25px', minWidth: '90px', borderColor: chipColor, color: chipColor}} label={params.value}/>
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
        <DataGrid/>
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

    const [selectedDepartment, setSelectedDepartment] = useState("none")

    const [currentDepartment, setCurrentDepartment] = useState(0)

    /**
     * Fetches all departments from the API.
     */
    const fetchDepartments = async () => {
        let result = await EmployeeService.getAllDepartments()
        setDepartments(result);
    }

    /**
     * On render, fetch all departments.
     */
    useEffect(() => {
        fetchDepartments()
    }, [])
    
    

  return ( <Box sx={{textAlign: 'left'}}>
      <Typography sx={{mb: 2}}>Select a department from the list below to retrieve the timesheets for that department.</Typography>
    <Select value={selectedDepartment} onChange={(e) => {
        e.preventDefault()
        setSelectedDepartment(e.target.value)
        }} sx={{minWidth: '30%'}}>
        <MenuItem key="none" value="none"><i>Select department...</i></MenuItem>
        {departments.map(department => {
            const id = department.department_id;
            return (<MenuItem key={`${id}`} value={`${id}`}>{department.department_name}</MenuItem>)
        })}
    </Select>
    <Button sx={{display: 'block', mt: 2}} variant="contained">RUN TIMESHEETS</Button>
  </Box>
  )
}


export default Timesheets