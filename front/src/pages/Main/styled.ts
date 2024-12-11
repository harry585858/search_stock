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
  box-shadow: 0 0 5px #aaaaaa;
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
  background-color:#FAFAFF;
`;
export const P = styled.p`
  font-family:arial;
  &:first-child{
  width: 30%;
  text-align:left;
  left:10%;
  }
  &:nth-child(2){
  left:10%;
  }
  &:last-child{
  text-align:right;
  }
`;
export const H3 = styled.p`
 &:first-child{
  width: 30%;
  text-align:left;
  left:10%;
  float:left;
  }
  &:nth-child(2){
  left:10%;
   float:left;
  }
  &:last-child{
  text-align:right;
   float:left;
  }
`;
export const DIV1 = styled.div`
 width: 80%;
  height: 36px;
  display: flex;
  justify-content: space-around;
  align-items: center;

  margin: 5px 0px;
`;