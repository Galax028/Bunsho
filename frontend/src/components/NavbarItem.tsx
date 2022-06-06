import {
  Collapse,
  Divider,
  Group,
  ThemeIcon,
  Title,
  TitleOrder,
  UnstyledButton,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { ReactNode } from "react";
import { IconChevronDown, IconChevronUp } from "@tabler/icons";

interface NavbarItemProps {
  label: string;
  size?: TitleOrder;
  icon?: ReactNode;
  iconSize?: number;
  withSubitems?: boolean;
  children?: ReactNode;
}

const NavbarItem = ({
  label,
  size = 3,
  icon,
  iconSize = 36,
  withSubitems = false,
  children,
}: NavbarItemProps) => {
  const [opened, handlers] = useDisclosure(false);

  return (
    <>
      <UnstyledButton
        p="xs"
        onClick={() => withSubitems && handlers.toggle()}
        sx={(t) => ({
          width: "100%",
          borderRadius: t.radius.md,
          "&:focus-visible, &:hover": {
            background: t.colors.dark[5],
          },
        })}
      >
        <Group>
          {icon && <ThemeIcon size={iconSize}>{icon}</ThemeIcon>}
          <Title order={size} sx={{ flexGrow: 1 }}>
            {label}
          </Title>
          {withSubitems && (opened ? <IconChevronDown /> : <IconChevronUp />)}
        </Group>
      </UnstyledButton>
      {withSubitems && (
        <Collapse in={opened}>
          <Group ml="xl">
            <Divider orientation="vertical" size="md" sx={{ height: "auto" }} />
            <Group mt="xs" spacing="xs" sx={{ width: "90%" }}>
              {children}
            </Group>
          </Group>
        </Collapse>
      )}
    </>
  );
};

export default NavbarItem;
