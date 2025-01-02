import React, { useEffect, useState } from "react";

import { useData } from "../Context";
import { areaElementClasses } from "@mui/x-charts/LineChart";
import { SparkLineChart } from "@mui/x-charts/SparkLineChart";
import {
  Box,
  Card,
  Chip,
  Stack,
  useTheme,
  Typography,
  CardContent,
} from "@mui/material";

const StatCard = ({ columnName, chartColor, hiThre, meThre }) => {
  const theme = useTheme();
  const { data, currentData } = useData();

  const [value, setValue] = useState(0);
  const [last50Data, setLast50Data] = useState([]);
  const [chipValue, setChipValue] = useState({});

  useEffect(() => {
    if (!data) {
      return;
    }

    const parsedData = data.map((row) => {
      const parsedValue = parseFloat(row[columnName]);
      return Number.isNaN(parsedValue) ? 0 : parsedValue;
    });

    setLast50Data(parsedData.slice(-50));
  }, [data, columnName]);

  useEffect(() => {
    if (!currentData) {
      return;
    }

    const currentValue = parseFloat(currentData[columnName]);
    const validCurrentValue = Number.isNaN(currentValue) ? 0 : currentValue;

    setLast50Data((prev) => {
      return [...prev.slice(1), validCurrentValue];
    });

    setValue(validCurrentValue);

    if (validCurrentValue > hiThre) {
      setChipValue({
        bgColor: theme.palette.error.light,
        textColor: theme.palette.error.dark,
        borderColor: theme.palette.error.main,
        level: "high",
      });
    } else if (validCurrentValue > meThre) {
      setChipValue({
        bgColor: theme.palette.warning.light,
        textColor: theme.palette.warning.dark,
        borderColor: theme.palette.warning.main,
        level: "medium",
      });
    } else {
      setChipValue({
        bgColor: theme.palette.success.light,
        textColor: theme.palette.success.dark,
        borderColor: theme.palette.success.main,
        level: "low",
      });
    }
  }, [data, currentData, columnName, theme, hiThre, meThre]);

  const title = columnName;
  const randomId = Math.floor(Math.random() * 1000);

  return (
    <Card variant="outlined" sx={{ height: "100%", flexGrow: 1 }}>
      <CardContent>
        <Typography variant="h4" component="h2" gutterBottom>
          {title}
        </Typography>
        <Stack
          direction="column"
          sx={{ justifyContent: "space-between", flexGrow: "1", gap: 1 }}
        >
          <Stack sx={{ justifyContent: "space-between" }}>
            <Stack direction="row" className="center-horizon">
              <Typography variant="h2">{formatNumber(value)}</Typography>
              <Chip
                sx={{
                  color: chipValue.textColor,
                  bgcolor: chipValue.bgColor,
                  borderColor: chipValue.borderColor,
                  fontWeight: "bold",
                }}
                variant="outlined"
                label={`${chipValue.level}`}
              />
            </Stack>
            <Typography
              variant="subtitle2"
              sx={{ paddingTop: "4px", color: "text.secondary" }}
            >
              Last 50 Packets
            </Typography>
          </Stack>
          <Box sx={{ width: "100%", height: 100 }}>
            <SparkLineChart
              colors={[chartColor]}
              data={last50Data}
              area
              showHighlight
              showTooltip
              xAxis={{
                scaleType: "band",
                visible: false,
              }}
              sx={{
                [`& .${areaElementClasses.root}`]: {
                  fill: `url(#area-gradient-${randomId})`,
                },
              }}
            >
              <AreaGradient
                color={chartColor}
                id={`area-gradient-${randomId}`}
              />
            </SparkLineChart>
          </Box>
        </Stack>
      </CardContent>
    </Card>
  );
};

export default StatCard;

const AreaGradient = ({ color, id }) => {
  return (
    <defs>
      <linearGradient id={id} x1="50%" y1="0%" x2="50%" y2="100%">
        <stop offset="0%" stopColor={color} stopOpacity={0.7} />
        <stop offset="100%" stopColor={color} stopOpacity={0.0} />
      </linearGradient>
    </defs>
  );
};

const formatNumber = (number) => {
  return number.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};
