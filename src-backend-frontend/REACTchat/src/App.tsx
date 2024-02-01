import React from "react";
import Home from "./pages/Home";
import { 
    createBrowserRouter,
    createRoutesFromElements,
    Route, 
    RouterProvider 
} from "react-router-dom";
import { ThemeProvider } from "@emotion/react";
import createMuiTheme from "./theme/Theme";

const router = createBrowserRouter(
    createRoutesFromElements(
        <Route>
            <Route path="/" element={ <Home /> }/>
        </Route>
    )
);

// App component
const App: React.FC = () => {
    const theme = createMuiTheme();
    return (
        <ThemeProvider theme={ theme }>
            <RouterProvider router={ router } />
        </ThemeProvider>
    )
};

export default App;
