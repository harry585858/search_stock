import React, { FC, useState, useEffect } from "react";
import { CommonSection } from "../../../components/CommonSection/CommonSection";
import { Header } from "../../../components/Header";
import { Root, SearchBar, SubmitIcon, SearchSection } from "./styled";
import searchicon from "../../../assets/images/search.png";
import { useStockData } from "../../../components/useStockData";
import {
  transformPredictData,
  usePredictData,
} from "../../../components/usePredictData";

const useGetVaried = (ticker: string): number | null => {
  const stockData = useStockData(ticker).dataDetails;
  const predictData = usePredictData(ticker).predictDetails;

  useEffect(() => {
    console.log("현재 데이터:", stockData);
    console.log("예측 데이터:", predictData);
  }, [stockData, predictData]);

  if (
    !ticker ||
    !stockData ||
    stockData.length === 0 ||
    !predictData?.예측데이터
  )
    return null;

  const currentData = stockData[stockData.length - 1]?.Close;
  if (!currentData) return null;

  const predictDataMdf = transformPredictData(predictData.예측데이터);
  const lastPrediction = predictDataMdf[predictDataMdf.length - 1];

  return lastPrediction.value - currentData;
};

export const ComparePage = () => {
  const [search, setSearch] = useState("");
  const [difference, setDifference] = useState();

  const handleSearch = () => {
    setDifference(useGetVaried(search));
  };

  return (
    <Root>
      <Header showLogo={true} />
      <CommonSection>
        <SearchBar>
          <SearchSection
            type="text"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="검색어 입력..."
          />
          <SubmitIcon type="button" onClick={handleSearch}>
            <img src={searchicon} width={"24px"} height={"24px"} />
          </SubmitIcon>
        </SearchBar>

        {difference !== null && (
          <div>Predicted Change : {difference.toFixed(2)}</div>
        )}
      </CommonSection>
    </Root>
  );
};
