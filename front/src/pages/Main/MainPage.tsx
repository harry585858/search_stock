import React, { useState, useEffect } from "react";
import axios from "axios";
import { CommonSection } from "../../components/CommonSection/CommonSection";
import { Header } from "../../components/Header";
import { Root, StockList } from "./styled";

export const MainPage = () => {
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/test"); // Flask API 호출
        setStockData(response.data); // 데이터를 상태에 저장
        setLoading(false); // 로딩 완료
      } catch (err: any) {
        setError(err); // 에러 처리
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>; // 로딩 중일 때
  if (error) return <div>Error: {error}</div>; // 에러 발생 시

  return (
    <Root>
      <Header showLogo={true} />
      {stockData && <CommonSection>Name: {stockData}</CommonSection>}
    </Root>
  );
};
