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
import emptyFavorite from "../../../assets/images/favorite-empty.png";
import filledFavorite from "../../../assets/images/favorite-fill.png";
import FullStar from "../../../assets/images/ratings-fill.png";
import HalfStar from "../../../assets/images/ratings-half.png";
import EmptyStar from "../../../assets/images/ratings-empty.png";
import {
  Root,
  Sidebar,
  SideTab,
  DataTab,
  DataTitle,
  DataDetails,
  PredictButton,
  DataSection,
  DataHeader,
  Title,
  Price,
  Ratings,
  Changed,
  ChartField,
  DataInterval,
  SelectInterval,
  Favorite,
  SideItem,
} from "./styled";
import { Link, useLocation } from "react-router-dom";
import { StyledLink } from "../styled";

interface StockTickerProps {
  ticker: string;
}

const StockChart: FC<StockTickerProps> = ({ ticker }) => {
  const { dataDetails, loading } = useStockData(ticker);
  const chartData = dataDetails.map((data) => ({
    ...data,
    dayX: data.Datetime.substring(5, 10),
    hourX: data.Datetime.substring(11),
  }));

  if (loading) return <CommonSection>Loading...</CommonSection>;

  return (
    <ChartField>
      <ResponsiveContainer width={"100%"} height={400}>
        <LineChart data={chartData} margin={{ top: 10, right: 10 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="dayX" />
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
    </ChartField>
  );
};

const ShowHeader: FC<StockTickerProps> = ({ ticker }) => {
  const dataDetails = useStockData(ticker).dataDetails;
  const showName = dataDetails.length > 0 ? dataDetails[0].Name : "Unknown";
  const showPrice = dataDetails[dataDetails.length - 1]?.Close?.toFixed(2);
  const showChangedPrice =
    dataDetails.length > 1
      ? (dataDetails[dataDetails.length - 1]?.Close ?? 0) -
        (dataDetails[dataDetails.length - 2]?.Close ?? 0)
      : 0.0;
  const showChangedVolume =
    dataDetails.length > 1
      ? (dataDetails[dataDetails.length - 1]?.Volume ?? 0) -
        (dataDetails[dataDetails.length - 2]?.Volume ?? 0)
      : 0.0;
  const loadRatings = usePredictData(ticker).predictDetails;
  const showRatings = loadRatings?.평균평점 ?? 0;
  const [isFavorite, setFavorite] = useState(loadRatings?.즐겨찾기여부);

  return (
    <DataHeader>
      <Title>{showName}</Title>
      <Price>$ {showPrice}</Price>
      {showChangedPrice > 0 ? (
        <Changed className="Up">+{showChangedPrice.toFixed(2)}</Changed>
      ) : (
        <Changed className="Down">{showChangedPrice.toFixed(2)}</Changed>
      )}
      {showChangedVolume > 0 ? (
        <Changed className="Up">+{showChangedVolume}</Changed>
      ) : (
        <Changed className="Down">{showChangedVolume}</Changed>
      )}
      <Ratings>{showRatings}</Ratings>
      <DataInterval>
        <SelectInterval>1D</SelectInterval>
        <SelectInterval>1W</SelectInterval>
        <SelectInterval>1M</SelectInterval>
      </DataInterval>
      {isFavorite ? (
        <Favorite
          onClick={() => {
            setFavorite(!isFavorite);
          }}
        >
          <img src={filledFavorite} width={"20px"} height={"20px"} />
        </Favorite>
      ) : (
        <Favorite
          onClick={() => {
            setFavorite(!isFavorite);
          }}
        >
          <img src={emptyFavorite} width={"20px"} height={"20px"} />
        </Favorite>
      )}
    </DataHeader>
  );
};

const ShowStockData: FC<StockTickerProps> = ({ ticker }) => {
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
    { title: "VOLUME", value: stockInfoCur.Volume },
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

const PredictChart: FC<StockTickerProps> = ({ ticker }) => {
  const { predictDetails, loading } = usePredictData(ticker);

  if (loading) return <CommonSection>Loading...</CommonSection>;
  if (!predictDetails?.예측데이터)
    return <CommonSection>No Data Available</CommonSection>;

  const chartData = transformPredictData(predictDetails.예측데이터);

  return (
    <ChartField>
      <ResponsiveContainer width={"100%"} height={400}>
        <LineChart data={chartData} margin={{ top: 10, right: 10 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="key" tickFormatter={(tick) => tick.slice(5)} />
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
    </ChartField>
  );
};

const ShowPredictHeader: FC<StockTickerProps> = ({ ticker }) => {
  const stockDetails = useStockData(ticker).dataDetails;
  const predictLoader = usePredictData(ticker).predictDetails;
  if (!predictLoader?.예측데이터)
    return <CommonSection>No data Available</CommonSection>;
  const predictDataMdf = transformPredictData(predictLoader.예측데이터);

  const showName = stockDetails.length > 0 ? stockDetails[0].Name : "Unknown";
  const showPrice = predictDataMdf[predictDataMdf.length - 1].value;
  const showChangedPrice =
    predictDataMdf[predictDataMdf.length - 1].value -
    (stockDetails[stockDetails.length - 1]?.Close ?? 0);
  const loadRatings = predictLoader.평균평점;

  return (
    <DataHeader>
      <Title>{showName}</Title>
      <Price>$ {showPrice}</Price>
      {showChangedPrice > 0 ? (
        <Changed className="Up">+{showChangedPrice.toFixed(2)}</Changed>
      ) : (
        <Changed className="Down">{showChangedPrice.toFixed(2)}</Changed>
      )}
      <Ratings>{loadRatings}</Ratings>
      <DataInterval>
        <SelectInterval onClick={() => {}}>1D</SelectInterval>
        <SelectInterval>1W</SelectInterval>
        <SelectInterval>1M</SelectInterval>
      </DataInterval>
    </DataHeader>
  );
};

export const DetailsPage: FC = () => {
  const location = useLocation();
  const { ticker } = location.state || { ticker: "Unknown" };
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
        <ShowHeader ticker={ticker} />
        <StockChart ticker={ticker} />
        <ShowStockData ticker={ticker} />
        {!isPredict ? (
          <></>
        ) : (
          <>
            <ShowPredictHeader ticker={ticker} />
            <PredictChart ticker={ticker} />
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
          <StyledLink
            key={index}
            to={"/stock/details"}
            state={{ ticker: stock.Ticker }}
          >
            <SideTab>
              <SideItem>{stock.Name}</SideItem>
              <SideItem>${stock.AdjClose?.toFixed(2)}</SideItem>
              <SideItem>{stock.Volume}</SideItem>
            </SideTab>
          </StyledLink>
        ))}
      </Sidebar>
    </Root>
  );
};
