import React from 'react';
import {
    Box,
    Button,
    Typography
} from '@mui/material'

/**
 * A Header is a reusable component that displays a
 * formatted section of typography denoting which page
 * the user is currently on.
 * @property {JSX.Element} action represents an action button that can be passed down
 * @returns {JSX.Element}
 */
const Header = (props) => {
  return <>
    <Box sx={{m: 4, display: 'flex', justifyContent: 'space-between'}} {...props}>
        <Typography variant='h4' fontWeight={700} color='var(--primary-dark)' textAlign='left'>{props.children}</Typography>
        {props.action}
    </Box>
  </>;
};

/**
 * A Header is a reusable component that displays a
 * formatted section of typography denoting which page
 * the user is currently on.
 * @returns {JSX.Element}
 */
export default Header;
