import React, { useState, useEffect } from "react";
import { CommonSection } from "../../components/CommonSection/CommonSection";
import { Header } from "../../components/Header";
import { Root, StockList } from "./styled";

export const MainPage = () => {
  const [stockData, setStockData] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/test")
      .then((response) => response.json())
      .then((stockData) => setStockData(stockData.message))
      .catch((error) => console.error("Error:", error));
  }, []);

  return (
    <Root>
      <Header showLogo={true} />
      {stockData ? (
        <CommonSection>
          <StockList>{stockData}</StockList>
        </CommonSection>
      ) : (
        <CommonSection>Loading</CommonSection>
      )}
    </Root>
  );
};
