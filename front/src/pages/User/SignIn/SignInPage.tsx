import React from "react";
import "./App.css";
import { Root } from "./styled";
import { Header } from "../../../components/Header";

export const SignInPage = () => {
  return (
    <Root>
      <Header showLogo={true} />
      <div className="App">
        <header className="App-header">
          <p>Enter your ID and PW to Sign up.</p>
          <form
            name="Login-data"
            action="http://localhost:8000/makelogin"
            method="post"
          >
            <input name="id" type="text" placeholder="ID 입력..." />
            <input name="pw" type="password" placeholder="PW 입력..." />
            <input type="submit" value="Login" />
          </form>
        </header>
      </div>
    </Root>
  );
};
