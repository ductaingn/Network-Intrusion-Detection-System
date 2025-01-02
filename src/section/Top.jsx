import React from "react";

import { StatCard } from "../component";
import { Grid2 } from "@mui/material";
import { blue, teal } from "../theme";

const Top = () => (
  <Grid2 container spacing={2}>
    <Grid2 size={{ xs: 12, sm: 6, lg: 3 }}>
      <StatCard
        columnName={"pkt_len_mean"}
        chartColor={blue[500]}
      />
    </Grid2>
    <Grid2 size={{ xs: 12, sm: 6, lg: 3 }}>
      <StatCard
        columnName={"fwd_iat_tot"}
        chartColor={teal[500]}
      />
    </Grid2>
    <Grid2 size={{ xs: 12, sm: 6, lg: 3 }}>
      <StatCard
        columnName={"idle_max"}
        chartColor={teal[500]}
      />
    </Grid2>
  </Grid2>
);

export default Top;
