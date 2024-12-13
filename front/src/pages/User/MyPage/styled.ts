import styled from "styled-components";

export const Root = styled.div`
  width: 100%;
  display: flex;
  justify-content: center;
  > h1 {
    position: absolute;
    top: 30%;
    left: 30%;
    font-family: arial;
    color: #3010d6;
  }
`;
export const RIGHT = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  align-items: center;
  position: absolute;
  top: 20vh;
  height: 70vh;
  background-color: #3010d6;
  left: 60vw;
  right: 90vw;
  width: 30%;
  display: flex;
  border: none;
  border-radius: 20px;
  box-shadow: 1px 1px 3px grey;
  h1 {
    color: white;
    font-family: arial;
  }
`;
