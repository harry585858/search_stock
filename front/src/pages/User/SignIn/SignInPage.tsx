import React from "react";
import {
  Root,
  Container,
  LeftSection,
  RightSection,
  FormSection,
  InputSection,
  LogInButton,
  OptionButton,
  StyledLink,
  H1,
  DecoText,
} from "./styled";
import { Header } from "../../../components/Header";

export const SignInPage = () => {
  return (
    <Root>
      <Header showLogo={true} />
      <Container>
        <LeftSection>
          <DecoText>
            로그인으로 Stock AI의 <br />
            확장된 기능을 경험하세요.
          </DecoText>
        </LeftSection>

        <RightSection>
          <H1>LOGIN</H1>
          <FormSection
            name="Login-data"
            action="http://localhost:8000/makelogin"
            method="post"
          >
            <InputSection name="id" type="text" placeholder="ID 입력..." />
            <InputSection name="pw" type="password" placeholder="PW 입력..." />
            <LogInButton type="submit" value="로그인" />
            <StyledLink href="http://localhost:8000/verify">
              비밀번호 변경/찾기
            </StyledLink>
          </FormSection>
          <hr />
          계정이 없으신가요?
          <StyledLink href="http://localhost:3000/User/SignUpPage">
            <OptionButton>회원가입</OptionButton>
          </StyledLink>
        </RightSection>
      </Container>
    </Root>
  );
};
