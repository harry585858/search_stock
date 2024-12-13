import styled from "styled-components";

export const Root = styled.div`
  width: 100%;
  display: flex;
  form {
    width: 75%;
  }
`;

export const H2 = styled.h2`
  position: absolute;
  top: 30vh;
  left: 25vw;
  width: 30%;
  font-family: arial;
  color: #3410d6;
`;

export const H1 = styled.h1`
  width: 100%;
  font-family: arial;
  color: #3410d6;
  margin: 1em;
`;

export const RIGHT = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;

  width: 30%;
  height: 70vh;
  position: absolute;
  top: 20vh;
  left: 60vw;
  right: 90vw;

  border: none;
  border-radius: 20px;
  box-shadow: 1px 1px 3px grey;

  input {
    margin: 0.5em;
    height: 2em;
    width: 100%;
    border: 1px solid #3410d6;
    border-radius: 20px;
    padding: 1em;
    background-color: #faf9ff;
  }

  input[type="submit"] {
    font-size: 1em;
    background-color: #3410d6;
    color: white;
    height: 3em;
  }

  button {
    font-size: 1em;
    background-color: white;
    height: 3em;
    width: 90%;
    border: 1px solid #3410d6;
    border-radius: 20px;
    padding: 1em;
  }

  a {
    font-family: arial;
    text-decoration: none;
    color: 3410d6;
  }
`;
