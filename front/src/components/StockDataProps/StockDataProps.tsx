export interface stockDataProps {
  Datetime: string;
  Ticker: string;
  Name: string;
  Open: number | null;
  High: number | null;
  Low: number | null;
  Close: number | null;
  AdjClose: number | null;
  Volume: number | null;
}
