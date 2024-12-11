import React, { FC } from "react";
import axios from "axios";
import { CommonSection } from "../../components/CommonSection/CommonSection";
import { Header } from "../../components/Header";
import { useStockData } from "../../components/useStockData";
import { MainSection, Root, StockList } from "./styled";

axios.defaults.baseURL = "http://127.0.0.1:8000";

export const MainPage: FC = () => {
  const { dataDetails, loading } = useStockData("");

  const summary = dataDetails.filter(
    (data) => data.Datetime === dataDetails[dataDetails.length - 1].Datetime
  );

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
        <MainSection>
          Ticker AdjClose Volume
          {summary.map((stock, index) => (
            <StockList key={index}>
              {stock.Name} ${stock.AdjClose?.toFixed(2)} {stock.Volume}
            </StockList>
          ))}
        </MainSection>
      </CommonSection>
    </Root>
  );
};
