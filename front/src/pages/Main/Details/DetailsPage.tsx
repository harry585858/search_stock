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
import { Root, Sidebar } from "./styled";
import { stockDataProps } from "../../../components/StockDataProps/StockDataProps";

interface StockChartProps {
  ticker: string;
}

const useStockData = (ticker: string) => {
  const [data, setData] = useState<stockDataProps[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<stockDataProps[]>(`/api?ticker=${ticker}`);
        setData(response.data);
      } catch (error) {
        console.error("Error fetching data: ", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [ticker]);

  return { data, loading };
};

const StockChart: FC<StockChartProps> = ({ ticker }) => {
  const { data, loading } = useStockData(ticker);

  if (loading) return <CommonSection>Loading...</CommonSection>;

  return (
    <ResponsiveContainer width="68%" height={500}>
      <LineChart
        data={data}
        margin={{ top: 200, right: 0, bottom: 5, left: 0 }}
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

export const DetailsPage: FC = () => {
  return (
    <Root>
      <Header showLogo={true} />
      <StockChart ticker="AAPL" />
      <Sidebar> Menus</Sidebar>
    </Root>
  );
};