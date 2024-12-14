import { useEffect, useState } from "react";
import axios from "axios";

interface PredictDataStruct {
  id: number;
  stock_code: string;
  [key: string]: number | string;
}

interface PredictChartProps {
  평균평점: number | null;
  즐겨찾기여부: boolean;
  예측데이터: PredictDataStruct[];
}

export const usePredictData = (ticker: string) => {
  const [predictDetails, setPredictDetails] =
    useState<PredictChartProps | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPredictData = async (interval: string) => {
      try {
        setLoading(true);
        const response = await axios.post<PredictChartProps>(
          `stockdetail/${interval}`,
          {
            stock_code: ticker,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        setPredictDetails(response.data);
        console.log(response.data);
      } catch (err) {
        setError("데이터 로딩 중 오류가 발생하였습니다.");
        console.log(err);
      } finally {
        setLoading(false);
      }
    };

    fetchPredictData("month");
  }, [ticker]);

  return { predictDetails, loading, error };
};

export const transformPredictData = (data: PredictDataStruct[]) => {
  // 모든 데이터를 키-값 형태로 변환
  return data.flatMap((entry) =>
    Object.entries(entry)
      .filter(([key]) => key !== "id" && key !== "stock_code") // 필요 없는 키 필터링
      .map(([key, value]) => ({
        key, // x축 데이터
        value: Number(value), // y축 데이터
        id: entry.id, // 그룹화 및 구분용
      }))
  );
};
