import React, { FC, useState, useEffect } from "react";
import axios from "axios";
import { CommonSection } from "../../components/CommonSection/CommonSection";
import { Header } from "../../components/Header";
import { stockDataProps } from "../../components/StockDataProps/StockDataProps";
import { Root, StockList } from "./styled";
import { useScrollEvent } from "../../components/useScrollEvent";

axios.defaults.baseURL = "http://127.0.0.1:8000";

export const MainPage: FC = () => {
  const [stockData, setStockData] = useState<stockDataProps[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<stockDataProps[]>("/api");
        setStockData(response.data);
        setLoading(false);
        console.log(stockData);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const summary = stockData.filter(
    (data) => data.Datetime === stockData[stockData.length - 1].Datetime
  );

  console.log(stockData);

  if (loading)
    return (
      <Root>
        <Header showLogo={true} />
        <CommonSection>Loading...</CommonSection>
      </Root>
    );

  return (
    <Root>
      <Header showLogo={true} />
      <CommonSection>
        <StockList>Ticker AdjClose Volume</StockList>
        {summary.map((stock, index) => (
          <StockList key={index}>
            {stock.Name} ${stock.AdjClose?.toFixed(2)}{" "}
            {stock.Volume?.toFixed(2)}
          </StockList>
        ))}
      </CommonSection>
    </Root>
  );
};
