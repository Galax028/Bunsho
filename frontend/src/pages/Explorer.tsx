import { AxiosError } from "axios";
import {
  AppShell,
  Divider,
  Group,
  Header,
  MediaQuery,
  Navbar,
  Paper,
  Progress,
  Space,
  Text,
  TextInput,
  Title,
} from "@mantine/core";
import { useDisclosure, useViewportSize } from "@mantine/hooks";
import { useEffect, useState } from "react";
import { useStoreon } from "storeon/react";
import {
  IconChevronUp,
  IconClipboard,
  IconCloud,
  IconDownload,
  IconInfoCircle,
  IconLayoutGrid,
  IconMenu,
  IconPlus,
  IconSearch,
  IconServer,
  IconSettings,
  IconShare,
  IconUpload,
  IconUsers,
} from "@tabler/icons";
import { useLocation } from "wouter";
import FileListing, { FileListingProps } from "../components/FileListing";
import Logo from "../components/Logo";
import HeaderButton from "../components/HeaderButton";
import NavbarItem from "../components/NavbarItem";
import api from "../api";
import { Errors } from "../enums";
import { Events, State } from "../store";

const Explorer = () => {
  const { dispatch, token } = useStoreon<State, Events>("token");
  const [_, setLocation] = useLocation();
  const { height } = useViewportSize();
  const [opened, handlers] = useDisclosure(false);
  const [rootDir, setRootDir] = useState<FileListingProps["items"] | null>(
    null
  );

  useEffect(() => {
    if (!token) setLocation("/auth");
    api
      .get("/core/ls/0/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        console.log(res.data.listing);
        setRootDir(res.data.listing);
      })
      .catch((err: AxiosError) => {
        const data: { error: string; error_msg: string } = err.response!.data;
        if (data.error === Errors.Unauthorized) {
          dispatch("setToken", "");
          setLocation("/auth");
        }
      });
  }, []);

  return (
    <AppShell
      navbar={
        <Navbar
          p="xs"
          hiddenBreakpoint="lg"
          hidden={!opened}
          fixed={opened}
          width={{ sm: 300, xl: 300 }}
          height={height}
        >
          <Navbar.Section>
            <Group position="center">
              <Logo bg={false} size={28}></Logo>
              <Title order={2}>Bunsho</Title>
            </Group>
          </Navbar.Section>
          <Divider my="xs" />
          <Navbar.Section grow>
            <NavbarItem label="Storage" icon={<IconCloud />} withSubitems>
              <NavbarItem label="Pictures" size={4} />
              <NavbarItem label="Documents" size={4} />
              <NavbarItem
                label="Add Location"
                size={4}
                icon={<IconPlus size={16} />}
                iconSize={28}
              />
            </NavbarItem>
          </Navbar.Section>
          <Divider my="xs" />
          <Navbar.Section>
            <Paper p="md" sx={(t) => ({ background: t.colors.dark[5] })}>
              <Title order={4}>Storage Usage Analysis</Title>
              <Group>
                <Text sx={{ flexGrow: 1 }}>Location: Pictures</Text>
                <IconServer />
              </Group>
              <Progress size="sm" value={42} mt="xs" />
              <Text size="xs">42 GB used of 100 GB</Text>
            </Paper>
          </Navbar.Section>
          <Divider my="xs" />
          <Navbar.Section>
            <NavbarItem label="Manage Users" icon={<IconUsers />} />
            <NavbarItem label="Server Settings" icon={<IconSettings />} />
            <NavbarItem label="About Bunsho" icon={<IconInfoCircle />} />
          </Navbar.Section>
        </Navbar>
      }
      padding={0}
    >
      <Header p="xs" height={58} sx={(t) => ({ background: t.colors.dark[5] })}>
        <Group noWrap>
          <MediaQuery largerThan="lg" styles={{ display: "none" }}>
            <HeaderButton
              label="Toggle navbar"
              placement="start"
              icon={<IconMenu size={20} />}
              onClick={() => handlers.toggle()}
            />
          </MediaQuery>
          <HeaderButton
            label="Go to parent folder"
            placement="start"
            icon={<IconChevronUp size={20} />}
          />
          <TextInput
            value="/"
            onChange={() => console.log()}
            variant="default"
            rightSection={
              <HeaderButton
                label="Copy path URL to clipboard"
                variant="transparent"
                icon={<IconClipboard size={18} />}
              />
            }
            sx={{ minWidth: 250, width: 750 }}
          />
          <TextInput
            placeholder="Type here to search..."
            variant="default"
            icon={<IconSearch />}
            sx={{ minWidth: 250, width: 250 }}
          />
          <Space sx={{ flexGrow: 1 }} />
          <HeaderButton label="Share" icon={<IconShare size={20} />} />
          <HeaderButton label="Download" icon={<IconDownload size={20} />} />
          <HeaderButton label="Upload" icon={<IconUpload size={20} />} />
          <HeaderButton
            label="Grid view"
            placement="end"
            icon={<IconLayoutGrid />}
          />
        </Group>
      </Header>
      {rootDir && <FileListing items={rootDir} />}
    </AppShell>
  );
};

export default Explorer;
