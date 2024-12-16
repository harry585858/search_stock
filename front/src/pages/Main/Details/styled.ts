import styled from "styled-components";

export const Root = styled.div`
  width: 100%;
  display: flex;
  justify-content: space-around;
  font-family: OpenSansTTF;
`;

export const DataSection = styled.div`
  width: 64%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 10px 2%;
  gap: 5px;

  position: absolute;
  left: 0px;
`;

export const DataHeader = styled.div`
  width: 90%;
  height: 45px;
  display: flex;
  align-items: center;
  gap: 20px;

  margin-top: 100px;
`;

export const Title = styled.span`
  font-size: 24px;
  font-weight: bold;
`;

export const Price = styled.span`
  font-size: 24px;
  font-weight: bold;
  font-stretch: condensed;
`;

export const Changed = styled.span`
  font-size: 14px;
  font-stretch: condensed;

  &.Up {
    color: #ff0000;
  }

  &.Down {
    color: #0000ff;
  }
`;

export const DataInterval = styled.div`
  width: 120px;
  height: 20px;
  overflow: clip;
  display: inline-flex;
  justify-content: space-around;

  border: 1px solid #3410d6;
  border-radius: 12px;
`;

export const SelectInterval = styled.button`
  width: 40px;

  border: none;
  background-color: transparent;

  color: #3410d6;
  font-stretch: condensed;

  &:focus {
    font-weight: bold;
    color: white;
    background-color: #3410d6;
  }
`;

export const Ratings = styled.span`
  font-size: 14px;
  font-stretch: condensed;
`;

export const Favorite = styled.button`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border: none;
  background-color: transparent;
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

export const ChartField = styled.div`
  width: 100%;
  border: 1px solid #dedaf1;
  border-radius: 8px;
  padding: 10px;
  background-color: #ffffff;
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

  font-family: OpenSansTTF;
  font-weight: bold;
  font-size: 16px;
`;
