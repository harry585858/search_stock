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

export const SearchBar = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 60%;
  min-width: 500px;
  max-width: 720px;
  height: 35px;
  padding: 1px 8px 0px;
  background-color: #ffffff;
  border-radius: 18px;
  box-shadow: 0 0 8px #ededed;
`;

export const SearchSection = styled.input`
  width: 90%;
  height: 100%;
  border: none;
  background-color: transparent;

  &:focus {
    outline: none;
  }
`;

export const SubmitIcon = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border: none;
  background-color: transparent;
`;
