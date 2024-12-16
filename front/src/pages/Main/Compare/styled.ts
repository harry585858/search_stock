import styled from "styled-components";

export const Root = styled.div`
  width: 100%;
  display: flex;
  justify-content: center;
`;

export const Section = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
  border-radius: 18px;
  box-shadow: 0 0 3px #7a7a7a;
`;

export const SearchBar = styled.form`
  display: flex;
  flex-direction: row;
  align-content: baseline;
  justify-content: space-around;

  width: 60%;
  min-width: 500px;
  max-width: 720px;
  height: 35px;
  padding: 1px 8px 0px;
  margin-bottom: 10px;

  background-color: #ffffff;
  border-radius: 18px;
  box-shadow: 0 0 8px #ededed;
`;

export const TextSection = styled.input`
  display: inline-flex;
  width: 85%;
  height: 100%;

  border: none;
  background-color: transparent;

  &:focus {
    outline: none;
  }
`;

export const SubmitIcon = styled.button`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 35px;
  height: 35px;
  border: none;
  background-color: transparent;
`;

export const CompareList = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-around;
  width: 80%;
  height: 50px;
  margin: 5px 0px;
  border: 1px solid #3410d6;
  background-color: #ffffff;
  border-radius: 18px;
`;

export const ListData = styled.div`
  display: inline-flex;
  justify-content: center;
`;

export const DeleteButton = styled.button`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  color: #3410d6;
  background-color: transparent;
`;
