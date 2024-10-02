import ReactDOM from "react-dom/client";
import { ChakraProvider } from "@chakra-ui/react";

import React from "react";
import theme from "./theme/theme.ts";
import { BrowserRouter } from "react-router-dom";
import { Router } from "./router/Router.tsx";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <BrowserRouter>
        <Router />
      </BrowserRouter>
    </ChakraProvider>
  </React.StrictMode>
);
