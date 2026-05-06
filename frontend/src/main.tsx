// AI Optimized by Skills Agent: React entrypoint renders the Quick-Career skeleton UI.
import React from "react";
import ReactDOM from "react-dom/client";

import { App } from "./App";
import "./styles.css";

// AI Optimized by Skills Agent: StrictMode surfaces unsafe UI patterns early during development.
ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
