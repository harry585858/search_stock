import styled from "styled-components";

export const Root = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
`;

export const Container = styled.div`
  width: 95%;
  display: flex;
  justify-content: space-around;
  align-items: center;

  margin-top: 72px;
  padding: 10px;
`;

export const LeftSection = styled.div`
  width: 50%;
  display: flex;
  justify-content: center;
`;

export const DecoText = styled.div`
  width: 360px;
  text-align: center;
  font-family: NotoSansTTF;
  font-size: 24px;
  color: #3410d6;
`;

export const RightSection = styled.div`
  width: 30%;
  height: 85%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5px;

  border: none;
  border-radius: 20px;
  box-shadow: 0 0 10px #f0f0f0;

  font-family: NotoSansTTF;
  font-size: 13px;
  font-weight: 300;
  color: #908ca4;
`;

export const H1 = styled.h1`
  width: 100%;
  font-family: OpenSansTTF;
  font-stretch: condensed;
  font-size: 30px;
  text-align: center;
  color: #3410d6;
  margin: 30px;
  margin-bottom: 60px;
`;

export const FormSection = styled.form`
  width: 75%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 7px;
`;

export const InputSection = styled.input`
  width: 85%;
  height: 15px;

  padding: 12px;

  border: 1px solid #3410d6;
  border-radius: 20px;
  background-color: #faf9ff;

  color: #100447;
  font-family: NotoSansTTF;

  &::placeholder {
    color: #3410d6;
    font-weight: 200;
  }

  &:hover {
    background-color: #f4f1ff;
  }
  &:focus {
    outline: none;
  }
`;

export const LogInButton = styled.input`
  width: 92%;
  height: 40px;
  display: flex;
  align-items: center;

  border: none;
  border-radius: 20px;
  background-color: #3410d6;
  color: #ffffff;
  font-family: NotoSansTTF;
  font-weight: 600;

  &:hover {
    outline: none;
    background-color: #5934fc;
  }

  &:active {
    outline: none;
    background-color: #280ab0;
  }
`;

export const StyledLink = styled.a`
  width: 70%;
  font-family: NotoSansTTF;
  text-decoration: none;
  text-align: center;
  color: #3410d6;

  &:visited {
    color: #3410d6;
  }
`;

export const OptionButton = styled.button`
  width: 100%;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;

  color: #3410d6;
  border: 1px solid #3410d6;
  border-radius: 20px;
  background-color: #ffffff;

  font-family: NotoSansTTF;

  &:hover {
    background-color: #faf9ff;
  }

  &:active {
    font-weight: bold;

    color: #ffffff;
    background-color: #3410d6;
  }
`;
