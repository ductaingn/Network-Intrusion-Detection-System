import React from "react";

import { StatCard } from "../component";
import { Grid2 } from "@mui/material";
import { blue, teal } from "../theme";

// const Top = () => {
//   return (
//     <Grid2 container spacing={2}>
//       <Grid2 size={{ xs: 12, sm: 6, lg: 3 }}>
//         <StatCard
//           columnName={"Pkt Size Avg"}
//           chartColor={blue[500]}
//           hiThre={100}
//           meThre={60}
//         />
//       </Grid2>
//       <Grid2 size={{ xs: 12, sm: 6, lg: 3 }}>
//         <StatCard
//           columnName={"Pkt Len Mean"}
//           chartColor={blue[500]}
//           hiThre={100}
//           meThre={60}
//         />
//       </Grid2>
//       <Grid2 size={{ xs: 12, sm: 6, lg: 3 }}>
//         <StatCard
//           columnName={"Flow Duration"}
//           chartColor={teal[500]}
//           hiThre={10000000}
//           meThre={1000000}
//         />
//       </Grid2>
//       <Grid2 size={{ xs: 12, sm: 6, lg: 3 }}>
//         <StatCard
//           columnName={"Flow IAT Max"}
//           chartColor={teal[500]}
//           hiThre={10000000}
//           meThre={1000000}
//         />
//       </Grid2>
//     </Grid2>
//   );
// };


const Top = () => (
  <Grid2 container spacing={2}>
    <Grid2 size={{ xs: 12, sm: 6, lg: 3 }}>
      <StatCard
        columnName={"pkt_len_mean"}
        chartColor={blue[500]}
        hiThre={100}
        meThre={60}
      />
    </Grid2>
    <Grid2 size={{ xs: 12, sm: 6, lg: 3 }}>
      <StatCard
        columnName={"flow_byts_s"}
        chartColor={teal[500]}
        hiThre={10000000}
        meThre={1000000}
      />
    </Grid2>
    {/* <Grid2 size={{ xs: 12, sm: 6, lg: 3 }}>
      <StatCard
        columnName={"Flow IAT Max"}
        chartColor={teal[500]}
        hiThre={10000000}
        meThre={1000000}
      />
    </Grid2> */}
  </Grid2>
);

export default Top;
