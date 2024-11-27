import React from "react";
import ReactDOM from "react-dom/client";
import { GlobalStyle } from "./global";
import "./global.css";
import { MainPage } from "./pages/Main/MainPage";
import { ComparePage } from "./pages/Main/Compare";
import { DetailsPage } from "./pages/Main/Details";
import { SignInPage } from "./pages/User/SignIn/SignInPage";
import { SignUpPage } from "./pages/User/SignUp";
import { MyPage } from "./pages/User/MyPage/MyPage";
import { BrowserRouter, Route, Routes } from "react-router-dom";

const root = ReactDOM.createRoot(document.getElementById("root") as any);

root.render(
  <React.StrictMode>
    <GlobalStyle />
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/User/MyPage" element={<MyPage />} />
        <Route path="/User/SignInPage" element={<SignInPage />} />
        <Route path="/User/SignUpPage" element={<SignUpPage />} />
        <Route path="/Stock/Details" element={<DetailsPage />} />
        <Route path="/Stock/Compare" element={<ComparePage />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
