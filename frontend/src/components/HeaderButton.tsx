import { ActionIcon, ActionIconVariant, DefaultProps, Tooltip } from "@mantine/core";
import { MouseEventHandler, ReactNode } from "react";

interface HeaderButtonProps {
  label: string;
  placement?: "start" | "center" | "end";
  variant?: ActionIconVariant;
  icon: ReactNode;
  onClick?: MouseEventHandler<HTMLButtonElement>;
  className?: DefaultProps["className"];
}

const HeaderButton = ({
  label,
  placement = "center",
  variant,
  icon,
  onClick,
  className
}: HeaderButtonProps) => {
  return (
    <Tooltip label={label} position="bottom" placement={placement} withArrow>
      <ActionIcon variant={variant ?? "outline"} className={className} onClick={onClick}>
        {icon}
      </ActionIcon>
    </Tooltip>
  );
};

export default HeaderButton;
