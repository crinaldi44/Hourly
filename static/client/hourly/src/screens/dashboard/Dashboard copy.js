import * as React from 'react';
import { styled, useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import MuiDrawer from '@mui/material/Drawer';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import { Grid } from '@mui/material';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import {Routes, Route, Navigate, useLocation, useNavigate} from 'react-router-dom'
import DashboardHomeScreen from "./screens/DashboardHomeScreen";
import ManageEmployeesScreen from "./screens/ManageEmployeesScreen";
import ProtectedRoute from '../../hooks/auth/components/ProtectedRoute'
import DepartmentsScreen from "./screens/departments/DepartmentsScreen";
import AccountSettingsScreen from "./screens/settings/AccountSettingsScreen";
import { AccountBalance, ExitToApp, Home, People, Settings } from '@mui/icons-material';
import Authentication from '../../hooks/auth/authentication'
import { Avatar } from '@mui/material';


const drawerWidth = 280;

const openedMixin = (theme) => ({
  width: drawerWidth,
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: 'hidden',
});

const closedMixin = (theme) => ({
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: 'hidden',
  width: `calc(${theme.spacing(7)} + 1px)`,
  [theme.breakpoints.up('sm')]: {
    width: `calc(${theme.spacing(8)} + 1px)`,
  },
});

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'flex-end',
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
}));

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  backgroundColor: 'var(--primary-dark)',
  transition: theme.transitions.create(['width', 'margin'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    width: drawerWidth,
    flexShrink: 0,
    whiteSpace: 'nowrap',
    boxSizing: 'border-box',
    ...(open && {
      ...openedMixin(theme),
      '& .MuiDrawer-paper': openedMixin(theme),
    }),
    ...(!open && {
      ...closedMixin(theme),
      '& .MuiDrawer-paper': closedMixin(theme),
    }),
  }),
);

export default function Dashboard() {
  const theme = useTheme();
  const [open, setOpen] = React.useState(false);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const location = useLocation();

  const navigate = useNavigate();

  /**
   * Represents the array of navigation items of the form
   * object with {title: string, icon: Icon, path: string}.
   */
  const navigationItems = [
      {
          title: 'Dashboard',
          icon: <Home color={location.pathname === '/dashboard' ? 'primary' : undefined}/>,
          path: '/dashboard',
      },
      {
        title: 'Manage Employees',
        icon: <People color={location.pathname === '/dashboard/manage' ? 'primary' : undefined}/>,
        path: '/dashboard/manage',
      },
      {
        title: 'Departments',
        icon: <AccountBalance color={location.pathname === '/dashboard/departments' ? 'primary' : undefined}/>,
        path: '/dashboard/departments',
    },
  ]

  const lowerNavigationItems = [
    {
        title: 'Settings',
        icon: <Settings color={location.pathname === '/dashboard/settings' ? 'primary' : undefined}/>,
        path: '/dashboard/settings',
    },
    {
      title: 'Logout',
      icon: <ExitToApp/>,
      path: '/',
      action: () => {
          Authentication.deAuthenticate();
          navigate('/');
      }
    }
  ]

  /**
   * Recursively renders a navigation tree.
   * @param navigationItem the nav item to render for
   * @param index the current index
   */
  // const renderNavigationTree = (navigationItem, index = 0) => {

  //     if (index >= navigationItem.length) {
  //         return;
  //     }

  //     return (
  //         <React.Fragment>
  //           <ListItemButton
  //             onClick={() => {
  //                   navigate(navigationItem[index].path);
  //               }}
  //             key={navigationItem[index].title}
  //             sx={{
  //               minHeight: 48,
  //               justifyContent: open ? 'initial' : 'center',
  //               px: 2.5,
  //             }}
  //             selected={location.pathname === navigationItem[index].path}
  //           >
  //             <ListItemIcon
  //               sx={{
  //                 minWidth: 0,
  //                 mr: open ? 3 : 'auto',
  //                 justifyContent: 'center',
  //               }}
  //             >
  //               {navigationItem[index].icon}
  //             </ListItemIcon>
  //             <ListItemText primary={navigationItem[index].title} sx={{ opacity: open ? 1 : 0 }} />
  //           </ListItemButton>
  //           {renderNavigationTree(navigationItem, ++index)}
  //           </React.Fragment>
  //         )
  // }

  const renderNavigationTree = (navigationItems) => {

    return navigationItems.map(navItem => (
            <ListItemButton
              onClick={() => {
                    if (navItem.action) {
                      navItem.action()
                    } else {
                      navigate(navItem.path);
                    }
                }}
              key={navItem.title}
              sx={{
                minHeight: 48,
                justifyContent: open ? 'initial' : 'center',
                px: 2.5,
              }}
              selected={location.pathname === navItem.path}
            >
              <ListItemIcon
                sx={{
                  minWidth: 0,
                  mr: open ? 3 : 'auto',
                  justifyContent: 'center',
                }}
              >
                {navItem.icon}
              </ListItemIcon>
              <ListItemText primary={navItem.title} sx={{ opacity: open ? 1 : 0 }} />
            </ListItemButton>
    ))
  }

  /**
     * Represents the default Route. Should the user attempt to route to
     * any route that is not specified, we will reroute them to the dashboard.
     */
   const defaultRoute = <Navigate to={{
        pathname: '/dashboard',
    }}/>

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed" open={open}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            sx={{
              marginRight: 5,
              ...(open && { display: 'none' }),
            }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            Hourly
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer variant="permanent" open={open}>
        <DrawerHeader>
            <Box position='absolute' left={10} textAlign={'left'}>
                <Typography fontWeight={700} display="inline">Hourly</Typography>
                <Typography variant='body2' color='textSecondary'>Timesheet Management</Typography>
            </Box>
          <IconButton onClick={handleDrawerClose}>
            {theme.direction === 'rtl' ? <ChevronRightIcon /> : <ChevronLeftIcon />}
          </IconButton>
        </DrawerHeader>
        <Divider />
        <List>
         {renderNavigationTree(navigationItems)}
        </List>
        <Divider />
        <List>
          {renderNavigationTree(lowerNavigationItems)}
        </List>
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, p: 3, backgroundColor: 'var(--offwhite)', height: '100vh', display: 'flex', flexDirection: 'column' }}>
        <DrawerHeader />
                    <Routes>
                        {/* <Route path='/*' element={defaultRoute}/> */}
                        <Route path='/' exact element={<DashboardHomeScreen/>}/>
                        {/* <Route path='/' exact element={<Navigate to={{
                            pathname: '/dashboard/manage'
                        }}/>}/> */}
                        <Route path='/departments' exact element={<DepartmentsScreen/>}/>
                        <Route path='/manage' exact element={<ProtectedRoute element={<ManageEmployeesScreen/>}/>}/>
                        <Route path='/settings' exact element={<ProtectedRoute element={<AccountSettingsScreen/>}/>}/>
                    </Routes>
      </Box>
    </Box>
  );
}