import { useEffect, useState } from "react";
import { stockDataProps } from "../StockDataProps/StockDataProps";
import axios from "axios";

export const useStockData = (ticker: string) => {
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
