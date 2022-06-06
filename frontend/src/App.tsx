import loadable from "@loadable/component";
import { Global, MantineProvider } from "@mantine/core";
import { useEffect } from "react";
import { useStoreon } from "storeon/react";
import { Events, State } from "./store";
import { Route, Switch } from "wouter";

const Pages = {
  Auth: loadable(() => import("./pages/Auth")),
  Explorer: loadable(() => import("./pages/Explorer")),
};

const App = () => {
  const { dispatch, token } = useStoreon<State, Events>("token");
  useEffect(() => dispatch("loadToken"), []);

  return (
    <MantineProvider
      withNormalizeCSS
      withGlobalStyles
      theme={{
        colorScheme: "dark",
        fontFamily: "Red Hat Text",
        fontSizes: {
          xs: 16,
          sm: 18,
          md: 20,
          lg: 22,
          xl: 24,
        },
        headings: {
          fontFamily: "Red Hat Text",
          fontWeight: 700,
        },
      }}
    >
      <Global
        styles={{
          "*, *::before, *::after": {
            boxSizing: "border-box",
            userSelect: "none",
          },
          "html, body, #root": {
            height: "100%",
          },
          input: {
            userSelect: "auto",
          },
        }}
      />
      <Switch>
        <Route path="/">
          <Pages.Explorer />
        </Route>
        <Route path="/auth">
          <Pages.Auth />
        </Route>
        <Route>{/* 404 Route */}</Route>
      </Switch>
    </MantineProvider>
  );
};

export default App;
