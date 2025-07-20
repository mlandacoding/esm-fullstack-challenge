import React, { useState, useEffect } from "react";
import Card from "@mui/material/Card";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import Plot from "react-plotly.js";
import { stringify } from "query-string";
import { BarChart } from '@mui/x-charts/BarChart';

import {
  Title,
  useList,
  ListContextProvider,
  DataTable,
  fetchUtils,
} from "react-admin";

import { API_BASE_URL } from "../utils/common";

const httpClient = async (url, options = {}) => {
  const { status, headers, body, json } = await fetchUtils.fetchJson(
    url,
    options,
  );
  return { status, headers, body, json };
};

const TopDriversByWins = ({ data }) => {
  const listContext = useList({ data });
  if (data) {
    return (
      <ListContextProvider value={listContext}>
        <DataTable resource="drivers" sx={{ boxShadow: 1 }}>
          <DataTable.Col source="id" />
          <DataTable.Col source="full_name" />
          <DataTable.Col source="nationality" />
          <DataTable.Col source="number_of_wins" />
        </DataTable>
      </ListContextProvider>
    );
  }
  return null;
};

const TopDriversByWinsBarChart = ({ data }) => {
  if (!data) return null;
  // Assume data is an array of driver objects with full_name and number_of_wins
  const sortedData = [...data].sort((a, b) => a.number_of_wins - b.number_of_wins);

  const y = sortedData.map((driver) => driver.full_name);
  const x = sortedData.map((driver) => driver.number_of_wins);

  return (
    <Plot
      data={[
        {
          x: x,
          y: y,
          type: "bar",
          orientation: "h",
          marker: { color: "#1976d2" },
        },
      ]}
      layout={{
        title: { text: "Top Drivers by Wins", font: { color: "#fff" } },
        xaxis: { title: "Number of Wins" , tickfont: { color: "#fff" }},
        yaxis: { title: "Driver", automargin: true, tickfont: { color: "#fff" } },
        margin: { l: 150, r: 30, t: 50, b: 50 },
        height: 400,
        paper_bgcolor: "transparent",
        plot_bgcolor: "transparent",
      }}
      style={{ width: "100%" }}
    />
  );
};

const BasicChart = () => {
  return (
    <Plot
      data={[
        {
          x: [1, 2, 3],
          y: [2, 6, 3],
          type: "scatter",
          mode: "lines+markers",
          marker: { color: "red" },
        },
        { type: "bar", x: [1, 2, 3], y: [2, 5, 3] },
      ]}
      layout={{ title: { text: "A Fancier Plot test" } }}
    />
  );
};



export const Dashboard = () => {
  const query = {
    range: "[0, 9]",
  };
  const url = `${API_BASE_URL}/dashboard/top_drivers_by_wins?${stringify(query)}`;
  const options = {
    method: "GET",
    headers: new Headers({
      Accept: "application/json",
    }),
  };
  const [topDriversData, setTopDriversData] = useState(null);
  useEffect(() => {
    httpClient(url, options).then(({ headers, json }) => {
      setTopDriversData(json);
    });
  }, []);

  return (
    <Box sx={{ m: 2 }}>
      <Title title="F1 Dashboard" />
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <Card sx={{ p: 2 }}>
            <Typography variant="h4" gutterBottom sx={{ textAlign: "left" }}>
              Top Drivers by Wins
            </Typography>
            <TopDriversByWins data={topDriversData} />
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card sx={{ p: 2 }}>
          <TopDriversByWinsBarChart data={topDriversData} />
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
