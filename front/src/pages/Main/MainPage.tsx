import { CommonSection } from "../../components/CommonSection/CommonSection";
import { Header } from "../../components/Header";
import { Root } from "./styled";

export const MainPage = () => {
  return (
    <Root>
      <Header showLogo={true} />
      <CommonSection>Main page</CommonSection>
    </Root>
  );
};