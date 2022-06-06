import { StoreonModule, createStoreon } from "storeon";

export interface State {
  token: string;
}

export interface Events {
  setToken: string;
  loadToken: undefined;
  storeToken: undefined;
}

let token: StoreonModule<State, Events> = (store) => {
  store.on("@init", () => ({ token: "" }));
  store.on("setToken", (_, event) => ({ token: event }));
  store.on("loadToken", () => {
    const t = localStorage.getItem("token")!;
    return { token: t ?? "" };
  });
  store.on("storeToken", (state) => localStorage.setItem("token", state.token));
};

const store = createStoreon<State, Events>([token]);

export default store;
