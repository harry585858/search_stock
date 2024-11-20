import React, { useState, useEffect } from "react";
import axios from "axios";
import { CommonSection } from "../../components/CommonSection/CommonSection";
import { Header } from "../../components/Header";
import { Root, StockList } from "./styled";

export const MainPage = () => {
  const [stockData, setStockData] = useState<any>(null); // 상태 타입을 any로 설정
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<any>(null); // 에러 타입을 any로 설정

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
  if (error) return <div>Error: {error.message || error}</div>; // 에러 발생 시

  // stockData가 객체일 경우 속성에 접근하여 출력
  return (
    <Root>
      <Header showLogo={true} />
      {stockData && (
        <CommonSection>
          {/* stockData.message가 있다고 가정하고 이를 출력 */}
          <div>{stockData.message}</div>
        </CommonSection>
      )}
    </Root>
  );
};
