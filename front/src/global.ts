import { createGlobalStyle } from "styled-components";
import NotoSansTTF from "./assets/fonts/NotoSansKR-VariableFont_wght.ttf";
import BigShotOneTTF from "./assets/fonts/BigshotOne-Regular.ttf";
import OpenSansTTF from "./assets/fonts/OpenSans-VariableFont_wdth,wght.ttf";

export const GlobalStyle = createGlobalStyle`
@font-face {
    font-family: 'BigshotOneTTF';
    src: local('BigShotOneTTF'), local('BigShotOneTTF');
    font-style: normal;
    src:url(${BigShotOneTTF}) format('truetype');
}

@font-face {
    font-family: 'NotoSansTTF' ;
    src: local('NotoSansTTF'), local('NotoSansTTF');
    font-style: normal;
    src: url(${NotoSansTTF}) format('truetype');
}

@font-face {
    font-family: 'OpenSansTTF';
    src: local()('OpenSansTTF'), local()('OpenSansTTF');
    font-style:normal;
    src: url(${OpenSansTTF}) format('truetype');
}
`;
