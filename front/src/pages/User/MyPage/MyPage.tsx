import React from "react";
import { Root } from "./styled";
import { Header } from "../../../components/Header";
import { CommonSection } from "../../../components/CommonSection/CommonSection";

export const MyPage = () => {
  return (
    <Root>
      <Header showLogo={true} />
      <CommonSection>MyPage</CommonSection>
    </Root>
  );
};
