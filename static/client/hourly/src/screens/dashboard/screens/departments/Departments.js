import React, { useState, useEffect } from 'react'
import { Accordion, AccordionSummary, AccordionDetails } from "../../components/AccordionView";
import { ExpandMore } from "@mui/icons-material";
import {
  Typography,
  Button,
  Stack
} from '@mui/material'
import LoadingCircle from '../../../../components/LoadingCircle';
import EmployeeService from '../../../../services/EmployeeService'
import useToast from '../../../../hooks/ui/Toast';
import useConfirmationDialog from '../../../../hooks/ui/Confirmation';

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
        <AccordionDetails>
          <Typography textAlign='left'><b>Manager: </b></Typography>
          <Stack direction='row' sx={{ mt: 5 }}>
            <Button variant="contained" color="error" onClick={() => {
              setConfirmMessage(`Are you sure you wish to delete the ${department.department_name} department?`)
              setConfirmOpen(true);
             }}>Delete</Button>
            <Button sx={{ ml: 2 }} disabled variant='contained'>Submit</Button>
          </Stack>
        </AccordionDetails>
      </Accordion>
    ))
  )


  return (
    <div>
      {departments.length > 0 ? renderDepartments : <LoadingCircle />}
      {Confirm}
    </div>
  )
}

/**
 * The Departments accordion is meant to display a listing of all active
 * departments.
 **/
export default Departments