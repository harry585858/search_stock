import React from "react";
import { CommonSection } from "../../components/CommonSection/CommonSection";
import { Header } from "../../components/Header";
import { Root, StockList } from "./styled";

/*function Stock({ st }) {
  return (
    <>
      {st.stockName} {st.currentPrice} {st.vol_per_day} {st.variance}
    </>
  );
}*/

export const MainPage = () => {
  /*const StockArray = [
    {
      id: 1,
      stockName: "example",
      currentPrice: 10000,
      vol_per_day: 25000,
      variance: 1.4,
    },
  ];*/

  return (
    <Root>
      <Header showLogo={true} />
      <CommonSection>*****</CommonSection>
    </Root>
  );
};
