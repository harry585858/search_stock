import React, { FC } from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";
import person from "../../assets/images/person.png";

type HeaderProps = {
  showLogo?: true;
};

export const Header: FC<HeaderProps> = ({ showLogo }) => {
  return (
    <Root>
      <StyledLink to="/">
        {showLogo && <h1 className="logo">STOCK AI</h1>}
      </StyledLink>
      <StyledLink to="/Stock/Details">Predict</StyledLink>
      <StyledLink to="/Stock/Compare">Compare</StyledLink>
      <StyledLink to="/User/SignInPage">
        <LoginButton>LogIn</LoginButton>
      </StyledLink>
      <StyledLink to="/naver/login">naver Login</StyledLink>
      <StyledLink to="/verify">비밀번호 변경</StyledLink>
      <StyledLink to="/User/MyPage">
        <img id="user_icon" src={person} />
      </StyledLink>
    </Root>
  );
};

const Root = styled.header`
  width: 95%;
  display: flex;
  align-items: baseline;
  position: fixed;
  top: 0;
  gap: 20px;

  padding-top: 20px;
  padding-bottom: 10px;

  font-family: OpenSansTTF;
  border-bottom: 1px solid #8c86a8;

  .logo {
    display: inline;
    font-family: BigShotOneTTF;
    font-size: 36px;
    color: #3410d6;
  }

  #user_icon {
    width: 28px;
    height: 28px;
  }
`;

const StyledLink = styled(Link)`
  text-decoration: none;
  color: inherit;

  &:visited {
    color: inherit;
  }
`;

const LoginButton = styled.button`
  width: 72px;
  height: 24px;
  display: inline-flex;
  align-items: center;
  justify-content: center;

  background-color: #3410d6;
  border: none;
  border-radius: 10px;

  font-family: NotoSansTTF;
  font-weight: bold;
  color: #fcfbff;
`;
