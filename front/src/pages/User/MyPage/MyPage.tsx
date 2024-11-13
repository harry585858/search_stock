import React from "react";
import { Root } from "./styled";
import { Header } from "../../../components/Header";

export const MyPage = () => {
  return (
    <Root>
      <Header showLogo={true} />
      Mypage
    </Root>
  );
};
