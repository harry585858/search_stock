import { Header } from "../../../components/Header";
import { CommonSection } from "../../../components/CommonSection/CommonSection";
import { Root } from "./styled";

export const SignUpPage = () => {
  return (
    <Root>
      <Header showLogo={true} />
      <CommonSection>회원가입</CommonSection>
    </Root>
  );
};
