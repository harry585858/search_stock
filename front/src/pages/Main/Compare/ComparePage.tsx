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

const UseGetVaried = (ticker: string): number | null => {
  const stockData = useStockData(ticker).dataDetails;
  const predictData = usePredictData(ticker).predictDetails;

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
  const [search, setSearch] = useState<string>("");
  const [difference, setDifference] = useState<number | null>();

  const variedDifference = UseGetVaried(search);

  useEffect(() => {
    setDifference(variedDifference);
  }, [variedDifference]);

  const handleSearch = (e: React.MouseEvent) => {
    e.preventDefault();
    console.log("Search triggered:", search);
  };

  return (
    <Root>
      <Header showLogo={true} />
      <CommonSection>
        <SearchBar>
          <SearchSection
            type="text"
            value={search}
            onChange={(event) => setSearch(event.target.value.toUpperCase())}
            placeholder="검색어 입력..."
          />
          <SubmitIcon
            type="button"
            onClick={handleSearch}
            disabled={search.length === 0}
          >
            <img src={searchicon} width={"24px"} height={"24px"} />
          </SubmitIcon>
        </SearchBar>

        {difference !== null && (
          <div>Predicted Change : {difference?.toFixed(2)}</div>
        )}
      </CommonSection>
    </Root>
  );
};
