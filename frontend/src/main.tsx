import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { StoreContext } from "storeon/react";
import App from "./App";
import store from "./store";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <StoreContext.Provider value={store}>
      <App />
    </StoreContext.Provider>
  </StrictMode>
);
