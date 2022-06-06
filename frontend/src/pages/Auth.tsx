import { AxiosError } from "axios";
import {
  Alert,
  Button,
  Center,
  Container,
  Divider,
  Group,
  Paper,
  PasswordInput,
  Stack,
  TextInput,
  Title,
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { useEffect, useRef, useState } from "react";
import { useStoreon } from "storeon/react";
import { useLocation } from "wouter";
import Logo from "../components/Logo";
import api from "../api";
import { Events, State } from "../store";

const Auth = () => {
  const { dispatch, token } = useStoreon<State, Events>("token");
  const [_, setLocation] = useLocation();
  const [error, setError] = useState(["", "none"]);
  const errorRef = useRef<HTMLDivElement>(null);
  const form = useForm({
    initialValues: {
      uname: "",
      passwd: "",
    },
  });
  const onFormSubmit = (values: { uname: string; passwd: string }) => {
    setError(["", error[1]]);
    api
      .post("/auth/login", values)
      .then((res) => {
        dispatch("setToken", res.data.token);
        dispatch("storeToken");
        setLocation("/");
      })
      .catch((err: AxiosError) =>
        setError([err.response!.data.error_msg, error[1]])
      );
  };

  useEffect(() => {
    if (token) setLocation("/");
  }, []);
  useEffect(() => {
    if (!errorRef.current) return;
    if (error[0] !== "") setError([error[0], "block"]);
    else setError([error[0], "none"]);
  }, [error[0]]);

  return (
    <Container
      fluid
      sx={(t) => ({
        backgroundColor: t.colors.blue[6],
        boxShadow: "inset 0 0 100px black",
      })}
    >
      <Center sx={{ height: "100vh" }}>
        <Paper p="xl" shadow="xl" radius="md" withBorder>
          <form onSubmit={form.onSubmit((values) => onFormSubmit(values))}>
            <Stack>
              <Stack align="center" spacing={0}>
                <Logo bg={false} size={88} />
                <Title>Bunsho</Title>
                <Alert
                  ref={errorRef}
                  color="red"
                  variant="outline"
                  mt="md"
                  style={{
                    display: error[1],
                    width: "280px",
                  }}
                >
                  {error[0]}
                </Alert>
              </Stack>
              <TextInput
                required
                label="Username"
                placeholder="Your username"
                {...form.getInputProps("uname")}
              />

              <PasswordInput
                required
                label="Password"
                placeholder="Your password"
                {...form.getInputProps("passwd")}
              />
              <Group position="center">
                <Divider sx={{ flexGrow: 1 }} />
                <Button type="submit">Login</Button>
                <Divider sx={{ flexGrow: 1 }} />
              </Group>
            </Stack>
          </form>
        </Paper>
      </Center>
    </Container>
  );
};

export default Auth;
