import React, { useState, useEffect } from "react";
import { useData } from "../Context";
import { styled } from "@mui/material/styles";
import { PieChart } from "@mui/x-charts/PieChart";
import { useDrawingArea } from "@mui/x-charts/hooks";
import {
  sky,
  teal,
  rose,
  fuchsia,
  emerald,
  yellow,
  blue,
  gray,
  pink,
} from "../theme";
import {
  Box,
  Card,
  Stack,
  Typography,
  CardContent,
  LinearProgress,
  linearProgressClasses,
} from "@mui/material";

const PieChartCard = ({ nameChart, columnName, ignoreValue = [], top = 5 }) => {
  const { data, currentData } = useData();

  const [, setLabels] = useState();
  const [total, setTotal] = useState(0);
  const [, setDataRaw] = useState([]);
  const [dataChart, setDataChart] = useState([]);

  // Pre calculate
  useEffect(() => {
    if (!data.length) return;

    const newLabels = new Set();
    data.forEach((row) => {
      if (!ignoreValue.includes(row[columnName])) {
        newLabels.add(row[columnName]);
      }
    });
    setLabels(newLabels);

    const initialDataRaw = Array.from(newLabels).map((item) => ({
      label: item,
      value: data.filter((row) => row[columnName] === item).length,
    }));

    setDataRaw(initialDataRaw);
    const initialTotal = initialDataRaw.reduce(
      (acc, item) => acc + item.value,
      0
    );
    setTotal(initialTotal);
  }, [data, columnName, ignoreValue]);

  useEffect(() => {
    if (!currentData) return;

    setDataRaw((prevDataRaw) => {
      const dataMap = new Map(prevDataRaw.map((d) => [d.label, d.value]));

      if (!ignoreValue.includes(currentData[columnName])) {
        if (dataMap.has(currentData[columnName])) {
          dataMap.set(
            currentData[columnName],
            dataMap.get(currentData[columnName]) + 1
          );
        } else {
          dataMap.set(currentData[columnName], 1);
        }

        setTotal((prevTotal) => prevTotal + 1);
      }

      const updatedDataRaw = Array.from(dataMap, ([label, value]) => ({
        label,
        value,
      }));

      // Sort and select top N, group the rest as "other"
      const sortedData = updatedDataRaw.sort((a, b) => b.value - a.value);
      const topN = sortedData.slice(0, top);
      const otherValue = sortedData
        .slice(top)
        .reduce((acc, item) => acc + item.value, 0);

      // Update colors
      const finalDataChart = [
        ...topN,
        { label: "other", value: otherValue },
      ].map((item, index) => ({
        ...item,
        color: colors[index % colors.length],
      }));

      setDataChart(finalDataChart);
      return updatedDataRaw;
    });
  }, [currentData, columnName, ignoreValue, top]);

  return (
    <Card variant="outlined" sx={{ height: "100%", flexGrow: 1 }}>
      <CardContent>
        <Typography variant="h4" component="h2" gutterBottom>
          {nameChart}
        </Typography>
        <Box className="center-root">
          <PieChart
            color={colors}
            margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
            series={[
              {
                data: dataChart,
                innerRadius: "50%",
                outerRadius: "80%",
                paddingAngle: 0,
                highlightScope: { faded: "global", highlighted: "item" },
              },
            ]}
            width={250}
            height={250}
            slotProps={{ legend: { hidden: true } }}
          >
            <PieCenterLabel primaryText={total} secondaryText="Total" />
          </PieChart>
        </Box>
        {dataChart.map((item, index) => (
          <Stack sx={{ gap: 1, flexGrow: 1 }} key={index}>
            <Stack direction="row" sx={{ pt: 1 }} className="center-horizon">
              <Typography variant="body2" sx={{ fontWeight: "550" }}>
                {item.label}
              </Typography>
              <Typography variant="body2" sx={{ color: "text.secondary" }}>
                {((item.value / total) * 100).toFixed(2)}%
              </Typography>
            </Stack>
            <LinearProgress
              variant="determinate"
              aria-label="Number of item by label"
              value={(item.value / total) * 100}
              sx={{
                [`& .${linearProgressClasses.bar}`]: {
                  backgroundColor: item.color,
                },
              }}
            />
          </Stack>
        ))}
      </CardContent>
    </Card>
  );
};

export default PieChartCard;

const PieCenterLabel = ({ primaryText, secondaryText }) => {
  const { width, height, left, top } = useDrawingArea();
  const primaryY = top + height / 2 - 10;
  const secondaryY = primaryY + 24;

  return (
    <React.Fragment>
      <StyledText variant="primary" x={left + width / 2} y={primaryY}>
        {primaryText}
      </StyledText>
      <StyledText variant="secondary" x={left + width / 2} y={secondaryY}>
        {secondaryText}
      </StyledText>
    </React.Fragment>
  );
};

const StyledText = styled("text", {
  shouldForwardProp: (prop) => prop !== "variant",
})(({ theme }) => ({
  textAnchor: "middle",
  dominantBaseline: "central",
  fill: (theme.vars || theme).palette.text.secondary,
  variants: [
    {
      props: {
        variant: "primary",
      },
      style: {
        fontSize: theme.typography.h5.fontSize,
      },
    },
    {
      props: ({ variant }) => variant !== "primary",
      style: {
        fontSize: theme.typography.body2.fontSize,
      },
    },
    {
      props: {
        variant: "primary",
      },
      style: {
        fontWeight: theme.typography.h5.fontWeight,
      },
    },
    {
      props: ({ variant }) => variant !== "primary",
      style: {
        fontWeight: theme.typography.body2.fontWeight,
      },
    },
  ],
}));

const colors = [
  sky[500],
  teal[500],
  rose[500],
  yellow[500],
  blue[500],
  fuchsia[500],
  emerald[500],
  gray[500],
  pink[500],
];
