import styled from "styled-components";

export const Root = styled.div`
  width: 75%;
  gap: 20px;
`;
export const Sign = styled.div`
  width: 100%;
  input{
  width:50%;
  height:3em;
  border:none;
  border-radius:20px;
  box-shadow: 5px 5px 20px grey;
  }
  input[type="submit"]{
  background-color: #3410d6;
  color:white;
  font-size:1em;
  }
`;