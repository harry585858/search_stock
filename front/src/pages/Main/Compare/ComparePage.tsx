import React, { FC, useState, useEffect } from "react";
import { CommonSection } from "../../../components/CommonSection/CommonSection";
import { Header } from "../../../components/Header";
import {
  Root,
  SearchBar,
  SubmitIcon,
  TextSection,
  CompareList,
  ListData,
  DeleteButton,
} from "./styled";
import searchicon from "../../../assets/images/search.png";
import deleteicon from "../../../assets/images/close.png";
import { useStockData } from "../../../components/useStockData";
import {
  transformPredictData,
  usePredictData,
} from "../../../components/usePredictData";

interface listItem {
  id: number;
  name: string;
  predict: number | undefined;
  current: number | undefined;
  change: number | undefined;
}

const useGetVaried = (ticker: string) => {
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
  const lastPrediction = predictDataMdf[predictDataMdf.length - 1].value;
  const changed = lastPrediction - currentData;

  return { lastPrediction, currentData, changed };
};

export const ComparePage = () => {
  const [list, setList] = useState<listItem[]>([]);
  const [search, setSearch] = useState<string>("");
  const [listnum, setListnum] = useState<number>(0);
  const variedData = useGetVaried(search);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();

    if (listnum === 4) {
      alert("더이상 추가할 수 없습니다.");
      return;
    }

    const newList: listItem = {
      id: listnum,
      name: search,
      predict: variedData?.lastPrediction ?? 0,
      current: variedData?.currentData ?? 0,
      change: variedData?.changed ?? 0,
    };

    if (
      newList.predict === 0 &&
      newList.current === 0 &&
      newList.change === 0
    ) {
      alert("유효하지 않은 검색어입니다.");
      return;
    }

    setList((prev) => [...prev, newList]);
    setListnum((list) => list + 1);
    setSearch("");
  };

  return (
    <Root>
      <Header showLogo={true} />
      <CommonSection>
        <SearchBar onSubmit={handleSearch}>
          <TextSection
            type="text"
            name="value"
            value={search}
            onChange={(event) => setSearch(event.target.value.toUpperCase())}
            placeholder="검색어 입력..."
          />
          <SubmitIcon type="submit" disabled={search.length === 0}>
            <img src={searchicon} width={"24px"} height={"24px"} />
          </SubmitIcon>
        </SearchBar>

        {list &&
          list.map((item, index) => (
            <CompareList key={index}>
              <ListData>{index + 1}</ListData>
              <ListData>{item.name}</ListData>
              <ListData>Predict Data : {item.predict}</ListData>
              <ListData>Current Data : {item.current?.toFixed(2)}</ListData>
              <ListData>Predicted Change : {item.change?.toFixed(2)}</ListData>
              <DeleteButton
                onClick={() => {
                  const deleteItem = [...list];
                  deleteItem.splice(index, 1);
                  setList(deleteItem);
                  setListnum((listnum) => listnum - 1);
                }}
                disabled={item.id === -1}
              >
                <img src={deleteicon} width={"8px"} height={"8px"} />
              </DeleteButton>
            </CompareList>
          ))}
      </CommonSection>
    </Root>
  );
};
