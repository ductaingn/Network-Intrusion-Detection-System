import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

import { theme } from "./theme";
import { DataProvider } from "./Context";
import { ThemeProvider, CssBaseline } from "@mui/material";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
    <DataProvider>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <App />
      </ThemeProvider>
    </DataProvider>
);
