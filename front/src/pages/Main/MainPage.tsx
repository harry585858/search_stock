import React, { FC, useState, useEffect } from "react";
import { CommonSection } from "../../components/CommonSection/CommonSection";
import { Header } from "../../components/Header";
import { Root, StockList } from "./styled";
import { stockDataType } from "../../components/StockDataList/StockDataList";

export const MainPage = () => {
  /*const [stockArray, setStockArray] = useState<stockDataType[]>([
    {
      id: 0,
      name: "example",
      currentPrice: 10000,
      volume: 10000,
      changedPercent: 1.4,
    },
  ]);*/

  const [stockArray, setStockArray] = useState<stockDataType[]>([]);

  useEffect(() => {
    fetch("/test")
      .then((response) => response.json())
      .then((stockArray) => {
        setStockArray(stockArray);
      })
      .catch((err) => console.log(err));
  }, []);

  return (
    <Root>
      <Header showLogo={true} />
      {typeof stockArray === "undefined" ? (
        <CommonSection>Loading</CommonSection>
      ) : (
        <CommonSection>
          {stockArray.map((st) => (
            <StockList>
              <h3>{st.name}</h3>
              <p>현재 가격 : {st.currentPrice}</p>
            </StockList>
          ))}
        </CommonSection>
      )}
    </Root>
  );
};
