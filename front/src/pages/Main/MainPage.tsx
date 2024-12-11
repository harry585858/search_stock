import React, { FC } from "react";
import axios from "axios";
import { CommonSection } from "../../components/CommonSection/CommonSection";
import { Header } from "../../components/Header";
import { useStockData } from "../../components/useStockData";
import { MainSection, Root, StockList, P, H3, DIV1 } from "./styled";

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
          <DIV1>
          <H3>종목이름</H3>
          <H3>현재가격</H3>
          <H3>24H 거래량</H3>
          </DIV1>
          {summary.map((stock, index) => (
            <StockList key={index}>
              <P>{stock.Name}</P> <P>${stock.AdjClose?.toFixed(2)}</P> <P>{stock.Volume}</P>
            </StockList>
          ))}
        </MainSection>
      </CommonSection>
    </Root>
  );
};
