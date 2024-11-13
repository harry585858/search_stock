import { CommonSection } from "../../../components/CommonSection/CommonSection";
import { Header } from "../../../components/Header";
import { Root } from "./styled";

export const DetailsPage = () => {
  return (
    <Root>
      <Header showLogo={true} />
      <CommonSection>details page</CommonSection>
    </Root>
  );
};
