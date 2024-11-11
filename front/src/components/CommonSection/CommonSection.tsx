import { FC, ReactNode } from "react";
import { Container, Root } from "./styled";

type CommonSectionProps = {
  children: ReactNode;
};

export const CommonSection: FC<CommonSectionProps> = ({ children }) => {
  return (
    <Root>
      <Container>{children}</Container>
    </Root>
  );
};
