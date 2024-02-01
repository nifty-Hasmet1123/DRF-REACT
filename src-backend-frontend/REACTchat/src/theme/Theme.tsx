import { createTheme, responsiveFontSizes } from "@mui/material";

declare module "@mui/material/styles" {
    interface Theme {
        primaryAppBar: {
            height: number;
        };
    }
    interface ThemeOptions {
        primaryAppBar: {
            height: number;
        };
    }
}

function createMuiTheme() {
    let theme = createTheme({
        typography: {
            fontFamily: ["IBM Plex Sans", "sans-serif"].join(","),
        },
        primaryAppBar: {
            height: 50, // set theme here
        },
        components: {
            MuiAppBar: {
                defaultProps: {
                    color: "default",
                    elevation: 0,
                }
            }
        }
    });
    theme = responsiveFontSizes(theme);
    return theme;
}

export default createMuiTheme;