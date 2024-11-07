import React from "react";
import logo from "./logo.svg";
import "./App.css";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>Enter your ID and PW to Sign up.</p>
        <form
          name="Login-data"
          action="http://localhost:8000/makelogin"
          method="post"
        >
          <input name="id" type="text" placeholder="ID 입력..." />
          <input name="pw" type="password" placeholder="PW 입력" />
          <input type="submit" value="Login" />
        </form>
      </header>
    </div>
  );
}

export default App;
