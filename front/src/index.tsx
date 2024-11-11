import React from "react";
import ReactDOM from "react-dom/client";
import "./global.css";
import { MainPage } from "./pages/Main/MainPage";
import { SignInPage } from "./pages/User/SignIn/SignInPage";
import { MyPage } from "./pages/User/MyPage/MyPage";
import { BrowserRouter, Route, Routes } from "react-router-dom";

const root = ReactDOM.createRoot(document.getElementById("root") as any);

root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/User/MyPage" element={<MyPage />} />
        <Route path="/User/SignInPage" element={<SignInPage />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
