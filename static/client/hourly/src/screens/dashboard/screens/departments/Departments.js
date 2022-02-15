import React, { useState, useEffect } from 'react'
import { Accordion, AccordionSummary, AccordionDetails } from "../../components/AccordionView";
import { ExpandMore } from "@mui/icons-material";
import {
  Typography,
  Button,
  Stack,
  Select,
  MenuItem
} from '@mui/material'
import LoadingCircle from '../../../../components/LoadingCircle';
import EmployeeService from '../../../../services/EmployeeService'
import useToast from '../../../../hooks/ui/Toast';
import useConfirmationDialog from '../../../../hooks/ui/Confirmation';


/**
 * DepartmentDetails will allow us to render a department's details within the accordion while
 * also allowing us to submit changes to that department.
 * @param {*} props 
 */
const DepartmentDetails = (props) => {

  const [employees, setEmployees] = useState(null)

  const [selected, setSelected] = useState(props.department.manager_id)

  const fetchEmployees = async () => {
    let response = await EmployeeService.getEmployeesForDepartment(props.department.department_id)
    setEmployees(response)
  }

  useEffect(() => {
    fetchEmployees();
  }, [])

  const handleChange = (event) => {
    setSelected(event.target.value)
  }

  /**
   * Updates the manager of department to the selected.
   */
  const handleSubmit = async () => {

    let department = {
      ...props.department,
      manager_id: selected
    }
    const response = await EmployeeService.updateDepartment(department)
    props.setToast('Action completed.')
    props.setToastOpen(true)
  }


  return (
    !employees ? <LoadingCircle /> :
      <AccordionDetails>
        <Typography textAlign='left' marginBottom='20px'><b>Employees:</b> {employees.length}</Typography>
        <Stack direction='column'>
          <Typography textAlign='left'><b>Manager: </b></Typography>
          <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              value={selected}
              label="Age"
              onChange={handleChange}
              sx={{height: '40px', maxWidth: '175px'}}
            >
              {employees.map(employee => (
                <MenuItem value={employee.id}>{employee.name}</MenuItem>
              ))}
            </Select>
        </Stack>
        <Stack direction='row' sx={{ mt: 5 }}>
          <Button variant="contained" color="error" onClick={() => {
            props.setConfirm(`Are you sure you wish to delete the ${props.department.department_name} department?`)
            props.setConfirmOpen(true);
          }}>Delete</Button>
          <Button sx={{ ml: 2 }} disabled={selected === props.department.manager_id} variant='contained' onClick={handleSubmit}>Submit</Button>
        </Stack>
      </AccordionDetails>
  )
}

/**
 * The Departments accordion is meant to display a listing of all active
 * departments.
 * @param props represents the props to accept
 **/
const Departments = () => {

  /**
   * Represents all currently stored departments.
   */
  const [departments, setDepartments] = useState([])

  /**
   * Represents the currently opened department
   */
  const [currentDepartment, setCurrentDepartment] = useState(0)

  /**
* Deletes the specified department.
*/
  async function deleteDepartment() {
    await EmployeeService.deleteDepartment(currentDepartment);
    setTimeout(() => {
      fetchData();
    }, 1000)
  }

  /**
   * Represents the Confirmation dialog for deletion.
   */
  const [setConfirmOpen, setConfirmAction, setConfirmMessage, Confirm] = useConfirmationDialog(deleteDepartment)

  const [setToastMsg, setToastOpen, setToastSeverity, Toast] = useToast()


  /**
   * Fetches data from the server.
   */
  const fetchData = async () => {
    let response = await EmployeeService.getAllDepartments()
    setDepartments(response)
  }

  /**
   * Represents action taken when the component renders.
   */
  useEffect(() => {
    fetchData();
  }, [])

  const renderDepartments = (
    departments.map(department => (
      <Accordion expanded={currentDepartment === department.department_id} onChange={() => {
        setCurrentDepartment(currentDepartment === department.department_id ? null : department.department_id)
      }}>
        <AccordionSummary
          expandIcon={<ExpandMore />}>
          <Typography>{department.department_name}</Typography>
        </AccordionSummary>
        <DepartmentDetails department={department} setConfirm={setConfirmMessage} setConfirmOpen={setConfirmOpen} setToast={setToastMsg} setToastOpen={setToastOpen} />
      </Accordion>
    ))
  )


  return (
    <div>
      {departments.length > 0 ? renderDepartments : <LoadingCircle />}
      {Confirm}
      {Toast}
    </div>
  )
}

/**
 * The Departments accordion is meant to display a listing of all active
 * departments.
 **/
export default Departments