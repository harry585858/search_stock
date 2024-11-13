import { FC } from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";

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
      <StyledLink to="/User/SignInPage">LogIn</StyledLink>
      <StyledLink to="/User/MyPage">MyPage</StyledLink>
    </Root>
  );
};

const Root = styled.header`
  position: fixed;
  top: 0;
  left: 20px;
  width: 100%;
  display: flex;
  align-items: baseline;
  gap: 20px;
  border-bottom: 1px;

  .logo {
    display: inline;
  }
`;

const StyledLink = styled(Link)`
  text-decoration: none;
  color: inherit;

  &:visited {
    color: inherit;
  }
`;
