import React from "react";
import "./App.css";
import { Root, RIGHT, H1, H2 } from "./styled";
import { Header } from "../../../components/Header";

export const SignInPage = () => {
  return (
    <Root>
      <Header showLogo={true} />
      <H2>로그인으로 Stock AI의 확장된 기능을 경험하세요.</H2>
      <RIGHT className="App">
        <H1>LOGIN</H1>
        <form
          name="Login-data"
          action="http://localhost:8000/makelogin"
          method="post"
        >
          <input name="id" type="text" placeholder="ID 입력..." />
          <input name="pw" type="password" placeholder="PW 입력..." />
          <input type="submit" value="Login" />
          <button>
            <a href="http://localhost:8000/verify">비밀번호 변경/찾기</a>
          </button>
        </form>
        <hr></hr>
        <a>계정이 없으신가요?</a>
        <button>
          <a href="http://localhost:3000/User/SignUppage">회원가입</a>
        </button>
      </RIGHT>
    </Root>
  );
};
