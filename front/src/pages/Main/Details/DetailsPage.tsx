import React, { FC, useState } from "react";
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
import { CommonSection } from "../../../components/CommonSection/CommonSection";
import { Header } from "../../../components/Header";
import {
  usePredictData,
  transformPredictData,
} from "../../../components/usePredictData";
import { useStockData } from "../../../components/useStockData";
import {
  Root,
  Sidebar,
  SideTab,
  DataTab,
  DataTitle,
  DataDetails,
  PredictButton,
  DataSection,
  P,
} from "./styled";

interface StockChartProps {
  ticker: string;
}

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
            stroke="#3410d6"
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
            <P>{stock.Name} </P><P>${stock.AdjClose?.toFixed(2)}{" "}</P>
            <P>{stock.Volume?.toFixed(2)}</P>
          </SideTab>
        ))}
      </Sidebar>
    </Root>
  );
};
