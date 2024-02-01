import { Box, CssBaseline } from "@mui/material";

import PrimaryAppBar from "./templates/PrimaryAppBar";
// create a sx attribute value for MUI
const boxSx = {
    display: "flex"
}

function Home() {
    return (
        <Box sx={ boxSx }>
            <CssBaseline />
            <PrimaryAppBar />
        </Box>
    );
};

export default Home;