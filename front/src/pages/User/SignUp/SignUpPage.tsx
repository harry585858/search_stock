import React from "react";
import { Header } from "../../../components/Header";
import { CommonSection } from "../../../components/CommonSection/CommonSection";
import { Root, Sign } from "./styled";

export const SignUpPage = () => {
  return (
    <Root>
      <Header showLogo={true} />
      <CommonSection>
        회원가입
        <Sign className="App">
          <form action="/makeresult" method="post">
            <input type="text" placeholder="아이디" name="id" />
            <input type="password" placeholder="비밀번호" name="pw" />
            <input type="email" placeholder="이메일" name="email" />
            <input type="checkbox"></input>가입 약관 및 개인정보 활용 정책에 동의합니다. 
            <input type="submit" value="회원가입" />
          </form>
        </Sign>
      </CommonSection>
    </Root>
  );
};