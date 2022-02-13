import React from 'react';
import {
    Box,
    Typography
} from '@mui/material'

/**
 * A Header is a reusable component that displays a
 * formatted section of typography denoting which page
 * the user is currently on.
 * @returns {JSX.Element}
 */
const Header = (props) => {
  return <>
    <Box sx={{m: 4}} {...props}>
        <Typography variant='h4' fontWeight={700} color='var(--primary-dark)' textAlign='left'>{props.children}</Typography>
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
