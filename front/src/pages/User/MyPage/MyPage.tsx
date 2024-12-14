import React from "react";
import { RIGHT, Root } from "./styled";
import { Header } from "../../../components/Header";
import { CommonSection } from "../../../components/CommonSection/CommonSection";

export const MyPage = () => {
  return (
    <Root>
      <Header showLogo={true} />
      <h1>아이디</h1>
      <RIGHT>
        <h1>즐겨찾기한 목록</h1>

      </RIGHT>
    </Root>
  );
};
