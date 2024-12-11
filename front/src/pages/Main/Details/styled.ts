import styled from "styled-components";

export const Root = styled.div`
  width: 100%;
  display: flex;
  justify-content: space-around;
`;

export const DataSection = styled.div`
  width: 65%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5px;

  position: absolute;
  left: 0px;
`;

export const Sidebar = styled.div`
  width: 30%;
  height: 480px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: fixed;
  top: 10px;
  right: 20px;
  gap: 10px;

  margin-top: 100px;
  padding-top: 50px;

  background-color: #ffffff;
  border-radius: 18px;
  box-shadow: 0 0 3px #7a7a7a;
`;

export const SideTab = styled.div`
  width: 90%;
  height: 36px;
  display: flex;
  justify-content: space-around;
  align-items: center;

  border-radius: 12px;
  border: 1px solid #3410d6;
`;

export const DataTab = styled.div`
  width: 90%;
  display: flex;
  justify-content: center;
  gap: 10px;

  border: 1px solid #3410d6;
  border-radius: 10px;

  #PredictTab {
    display: flex;
    margin-top: 60px;
  }
`;

export const DataTitle = styled.div`
  display: flex;
  gap: 6px;
  color: #a9a2c3;
`;

export const DataDetails = styled.div`
  font-family: OpenSansTTF;
  color: #000000;
`;

export const PredictButton = styled.button`
  width: 350px;
  height: 40px;

  border-radius: 18px;
  border: 0px;
  background-color: #3410d6;
  color: #ffffff;
`;
