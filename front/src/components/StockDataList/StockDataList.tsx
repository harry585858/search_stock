import React from "react";

export type stockDataType = {
  id: number;
  name: string;
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
