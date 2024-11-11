import { FC } from "react";
import styled from "styled-components";

type HeaderProps = {
  showLogo?: true;
  title?: string;
};

export const Header: FC<HeaderProps> = ({ showLogo, title }) => {
  return (
    <Root>
      {title && <h1 className="line-clamp-1">{title}</h1>}
      {showLogo && <h1 className="logo">STOCK AI</h1>}
    </Root>
  );
};

const Root = styled.header`
  position: fixed;
  z-index: 10;
  top: 0;
  left: 10%;
`;
