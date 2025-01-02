import React from "react";
import "./App.css";

import { Top, Mid } from "./section";
import { Grid2 } from "@mui/material";

const App = () => {
  return (
    <Grid2
      container
      spacing={2}
      className="center-root"
      sx={{ paddingTop: "24px", paddingX: "5%" }}
    >
      <Grid2 sx={{ width: "100%" }}>
        <Top />
      </Grid2>
      <Grid2 sx={{ width: "100%" }}>
        <Mid />
      </Grid2>
    </Grid2>
  );
};

export default App;