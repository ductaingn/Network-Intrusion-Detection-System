import React, { createContext, useContext, useEffect, useState } from "react";

const DataContext = createContext();

export const DataProvider = ({ children }) => {
  const [data, setData] = useState([]);
  const [currentData, setCurrentData] = useState(null);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8080');

    ws.onopen = () => {
      alert('WebSocket connection opened');
    };

    ws.onmessage = (event) => {
      const receivedData = JSON.parse(event.data);
      
      let value = JSON.parse(receivedData.value); // Parse the JSON string into an object
      const key = receivedData.key;
      value.ip_address = key; // Now you can safely assign the property
      setData((prevData) => [...prevData, value]);
      setCurrentData(value);
    };

    ws.onclose = () => {
      alert('WebSocket connection closed');
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <DataContext.Provider value={{ data, currentData }}>
      {children}
    </DataContext.Provider>
  );
};

export const useData = () => {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error("useData must be used within a DataProvider");
  }

  return context;
};