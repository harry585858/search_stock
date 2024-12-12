import React from "react";
import { Header } from "../../../components/Header";
import { CommonSection } from "../../../components/CommonSection/CommonSection";
import { Root } from "./styled";

export const SignUpPage = () => {
  return (
    <Root>
      <Header showLogo={true} />
      <CommonSection>회원가입<form action="/makeresult" method="post">
            <input type="text" placeholder="아이디" name="id">
            <input type="password" placeholder="비밀번호" name="pw">
            <input type="email" placeholder="이메일" name="email">
            <input type="submit"value="회원가입">
        </form></CommonSection>
      
    </Root>
  );
};
