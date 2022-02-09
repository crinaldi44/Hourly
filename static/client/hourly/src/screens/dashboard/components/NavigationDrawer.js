import React, { useState } from 'react';
import { Drawer, Button, Box, List, Divider, ListItem } from '@mui/material';

/**
 * Represents the navigation bar.
 * @returns {JSX.Element}
 */
export default function NavigationDrawer() {

  /**
   * Represents the current state of the navigation drawer.
   */
  const [state, setState] = useState()

  /**
   * Toggles the navigation drawer state.
   * @param {*} anchor 
   * @param {*} open 
   * @returns 
   */
  const toggleDrawer = (anchor, open) => (event) => {
      if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
        return
      }
      setState({...state, [anchor]: open })
  }

  /**
   * Represents the list of selectable items.
   * @param {*} anchor 
   */
  const list = (anchor) => (
    <Box
      sx={{ width: anchor === 'top' || anchor === 'bottom' ? 'auto' : 250 }}
      role="presentation"
      onClick={toggleDrawer(anchor, false)}
      onKeyDown={toggleDrawer(anchor, false)}
    >
      <List>
        {['Inbox', 'Starred', 'Send email', 'Drafts'].map((text, index) => (
          <ListItem button key={text}>
            <ListItemIcon>
              {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
            </ListItemIcon>
            <ListItemText primary={text} />
          </ListItem>
        ))}
      </List>
      <Divider />
      <List>
        {['All mail', 'Trash', 'Spam'].map((text, index) => (
          <ListItem button key={text}>
            <ListItemIcon>
              {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
            </ListItemIcon>
            <ListItemText primary={text} />
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <>
      <Drawer
            anchor={anchor}
            open={state[anchor]}
            onClose={toggleDrawer(anchor, false)}
          >
            {list(anchor)}
      </Drawer>
    </>
  )
};
