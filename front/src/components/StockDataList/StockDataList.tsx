import React from "react";

export type stockDataType = {
  id: string;
  stock_name: string;
  stock_code: string;
  currentPrice?: number;
  volume?: number;
  changedPrice?: number;
  changedPercent?: number;
  ratings?: number;

  highPrice?: number;
  lowPrice?: number;
  opening?: number;
  closing?: number;
};
