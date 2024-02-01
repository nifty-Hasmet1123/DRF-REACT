import { useTheme } from "@mui/material/styles";
import { useEffect, useState } from "react";
import { Typography, Link, IconButton, Box, Drawer, AppBar, Toolbar } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import useMediaQuery from "@mui/material/useMediaQuery";

function PrimaryAppBar() {
    const [ sideMenu, setSideMenu ] = useState(false);
    const theme = useTheme();

    const isSmallScreen = useMediaQuery(theme.breakpoints.up("sm"));

    useEffect(() => {
        if (isSmallScreen && sideMenu) {
            setSideMenu(false);
        }
    }, [ isSmallScreen ])

    return (
        <AppBar 
            sx={{
                zIndex: (theme) => theme.zIndex.drawer + 2,
                backgroundColor: theme.palette.background.default,
                borderBottom: `1px solid ${theme.palette.divider}`,
            }}
            >
            <Toolbar 
                variant="dense" 
                sx={{ 
                    height: theme.primaryAppBar.height,
                    minHeight: theme.primaryAppBar.height 
                }}
            >
                <Box sx={{ display: { xs: "block", sm: "none" } }}>
                    <IconButton color="inherit" aria-label="open drawer" edge="start" sx={{ mr: 2 }} onClick={ () => setSideMenu(!sideMenu) }>
                        <MenuIcon />
                    </IconButton>
                </Box>

                <Drawer anchor="left" open={ sideMenu }>
                    {
                        [...Array(100)].map((_, idx) => {
                            return <Typography key={idx} paragraph>
                                {idx + 1}
                            </Typography>
                        })
                    }
                </Drawer>

                <Link href="/" underline="none" color="inherit">
                    <Typography 
                        variant="h6" 
                        component="div" 
                        noWrap 
                        sx={{
                            display: {
                                fontWeight: "700",
                                letterSpacing: "-0.5px"
                            }
                        }}
                    >
                        Django Chat
                    </Typography>
                </Link>
            </Toolbar>
        </AppBar>
    );
};

export default PrimaryAppBar;