// frontend/src/main.jsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css";
import { ThemeProvider } from "./context/ThemeContext"; // <-- Import the provider
import { NostrProvider } from "./context/NostrContext"; // <-- IMPORT
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ThemeProvider>
      <NostrProvider>
        {" "}
        {/* <-- WRAP */}
        <App />
      </NostrProvider>
    </ThemeProvider>
  </React.StrictMode>
);
