import React, { FC, useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import axios from "axios";
import { CommonSection } from "../../../components/CommonSection/CommonSection";
import { Header } from "../../../components/Header";
import {
  Root,
  Sidebar,
  SideTab,
  DataTab,
  DataTitle,
  DataDetails,
  PredictButton,
  DataSection,
} from "./styled";
import { stockDataProps } from "../../../components/StockDataProps/StockDataProps";

interface StockChartProps {
  ticker: string;
}

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

const useStockData = (ticker: string) => {
  const [dataDetails, setDataDetails] = useState<stockDataProps[]>([]);
  const [listData, setListData] = useState<stockDataProps[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response_Detail = await axios.get<stockDataProps[]>(
          `/api?ticker=${ticker}`
        );
        const response_Side = await axios.get<stockDataProps[]>("/api");
        setDataDetails(response_Detail.data);
        setListData(response_Side.data);
      } catch (error) {
        console.error("Error fetching data: ", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [ticker]);

  return { dataDetails, listData, loading };
};

const StockChart: FC<StockChartProps> = ({ ticker }) => {
  const { dataDetails, loading } = useStockData(ticker);

  if (loading) return <CommonSection>Loading...</CommonSection>;

  return (
    <ResponsiveContainer width={"100%"} height={550}>
      <LineChart
        data={dataDetails}
        margin={{ top: 150, right: 0, left: 0, bottom: 10 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="Datetime"
          tickFormatter={(tick) => tick.slice(11, 16)}
        />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey={"Close"}
          stroke="#3410d6"
          activeDot={{ r: 8 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

const ShowStockData: FC<StockChartProps> = ({ ticker }) => {
  const stockInfo = useStockData(ticker).dataDetails;

  if (!stockInfo || stockInfo.length === 0) {
    return <div>Loading...</div>;
  }

  const stockInfoCur = stockInfo[stockInfo.length - 1];
  const stockDetails = [
    { title: "HIGH", value: stockInfoCur.High?.toFixed(2) },
    { title: "LOW", value: stockInfoCur.Low?.toFixed(2) },
    { title: "OPENING", value: stockInfoCur.Open?.toFixed(2) },
    { title: "CLOSING", value: stockInfoCur.Close?.toFixed(2) },
    { title: "VOLUME", value: stockInfoCur.Volume?.toFixed(2) },
  ];

  return (
    <DataTab>
      {stockDetails.map((detail) => (
        <DataTitle key={detail.title}>
          {detail.title}
          <DataDetails>{detail.value}</DataDetails>
        </DataTitle>
      ))}
    </DataTab>
  );
};

const usePredictData = (ticker: string) => {
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

const transformPredictData = (data: PredictDataStruct[]) => {
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

const PredictChart: FC<StockChartProps> = ({ ticker }) => {
  const { predictDetails, loading } = usePredictData(ticker);

  if (loading) return <CommonSection>Loading...</CommonSection>;
  if (!predictDetails?.예측데이터)
    return <CommonSection>No Data Available</CommonSection>;

  const chartData = transformPredictData(predictDetails.예측데이터);

  return (
    <ResponsiveContainer width={"100%"} height={500}>
      <LineChart
        data={chartData}
        margin={{ top: 10, right: 0, left: 0, bottom: 10 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="key" tickFormatter={(tick) => tick.slice(11, 16)} />
        <YAxis />
        <Tooltip />
        <Legend />
        {Array.from(new Set(chartData.map((d) => d.id))).map((id) => (
          <Line
            key={id}
            type="monotone"
            dataKey="value"
            data={chartData.filter((d) => d.id === id)}
            stroke={`#${Math.floor(Math.random() * 16777215).toString(16)}`} // 랜덤 색상
            name={`Stock ${id}`}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
};

const ShowPredictData: FC<StockChartProps> = ({ ticker }) => {
  const { predictDetails, loading, error } = usePredictData(ticker);

  if (loading) return <CommonSection>Loading...</CommonSection>;
  if (error) return <CommonSection>{error}</CommonSection>;

  return (
    <DataTab id="PredictTab">
      <DataTitle>
        Ratings <DataDetails>{predictDetails?.평균평점}</DataDetails>
      </DataTitle>
      <DataTitle>
        Favorite{" "}
        <DataDetails>{predictDetails?.즐겨찾기여부 ? "Y" : "N"}</DataDetails>
      </DataTitle>
      {predictDetails?.예측데이터.map((data) => (
        <DataTitle key={data.id}>
          <DataDetails>
            {Object.entries(data)
              .filter(([key]) => key !== "id" && key !== "stock_code")
              .map(([key, value]) => (
                <span key={key}>
                  {key}: {value}{" "}
                </span>
              ))}
          </DataDetails>
        </DataTitle>
      ))}
    </DataTab>
  );
};

export const DetailsPage: FC<StockChartProps> = ({ ticker }) => {
  const [isPredict, setPredict] = useState(false);
  const [showButton, setShowButton] = useState(true);
  const sideData = useStockData("").listData;
  const sideDataCur = sideData.filter(
    (data) => data.Datetime === sideData[sideData.length - 1].Datetime
  );

  return (
    <Root>
      <Header showLogo={true} />
      <DataSection>
        <StockChart ticker={ticker} />
        <ShowStockData ticker={ticker} />
        {!isPredict ? (
          <></>
        ) : (
          <>
            <PredictChart ticker={ticker} />
            <ShowPredictData ticker={ticker} />
          </>
        )}
        {!showButton ? (
          <></>
        ) : (
          <PredictButton
            onClick={() => {
              setPredict(true);
              setShowButton(false);
            }}
          >
            Predict
          </PredictButton>
        )}
      </DataSection>

      <Sidebar>
        {sideDataCur.map((stock, index) => (
          <SideTab key={index}>
            {stock.Name} ${stock.AdjClose?.toFixed(2)}{" "}
            {stock.Volume?.toFixed(2)}
          </SideTab>
        ))}
      </Sidebar>
    </Root>
  );
};
