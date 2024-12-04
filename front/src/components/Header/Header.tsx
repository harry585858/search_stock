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
      <HeaderSectionLeft>
        <StyledLink to="/">
          {showLogo && <h1 className="logo">STOCK AI</h1>}
        </StyledLink>
        <StyledLink to="/Stock/Details">Details</StyledLink>
        <StyledLink to="/Stock/Compare">Compare</StyledLink>
      </HeaderSectionLeft>

      <HeaderSectionRight>
        <StyledLink to="/User/SignInPage">
          <LoginButton>LOGIN</LoginButton>
        </StyledLink>
        <StyledLink to="/User/MyPage">
          <img id="user_icon" src={person} />
        </StyledLink>
      </HeaderSectionRight>
    </Root>
  );
};

const Root = styled.header`
  width: 95%;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  position: fixed;
  top: 0;
  z-index: 5;

  padding: 20px 10px 5px;

  font-family: OpenSansTTF;
  border-bottom: 1px solid #8c86a8;
  background-color: #ffffff;

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

const HeaderSectionLeft = styled.div`
  display: flex;
  align-items: baseline;
  gap: 40px;
`;

const HeaderSectionRight = styled.div`
  display: flex;
  align-items: center;
  gap: 20px;
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
  font-size: 12px;
  color: #fcfbff;
`;
