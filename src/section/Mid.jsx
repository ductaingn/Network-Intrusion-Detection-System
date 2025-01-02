import React from "react";

import { Grid2 } from "@mui/material";
import { PieChartCard } from "../component";

const Mid = () => {
  return (
    <Grid2 container spacing={2}>
      <Grid2 size={4} className="center-root">
        <PieChartCard
          nameChart={"IP Address Under Attack"}
          columnName={"ip_address"}
          ignoreValue={["0"]}
          top={7}
        />
      </Grid2>
      <Grid2 size={4} className="center-root">
        <PieChartCard
          nameChart={"Attack Type"}
          columnName={"prediction"} // Ten cot can lay du lieu
          ignoreValue={["Benign"]}
          top={7}
        />
      </Grid2>
    </Grid2>
  );
};

export default Mid;
