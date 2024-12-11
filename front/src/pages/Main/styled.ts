import styled from "styled-components";

export const Root = styled.div`
  width: 100%;
  display: flex;
  justify-content: center;
`;

export const MainSection = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
  border-radius: 18px;
  box-shadow: 0 0 3px #7a7a7a;
`;

export const StockList = styled.div`
  width: 80%;
  height: 36px;
  display: flex;
  justify-content: space-around;
  align-items: center;

  margin: 5px 0px;

  border: 1px solid #0d22e1;
  border-radius: 15px;
`;
