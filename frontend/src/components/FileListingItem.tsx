import { Grid, Text, UnstyledButton } from "@mantine/core";
import { useElementSize } from "@mantine/hooks";
import { IconFile, IconFolder } from "@tabler/icons";

export interface FileListingItemProps {
  data: {
    name: string;
    mimetype: string;
    size: string;
    created: number;
    is_directory: boolean;
  };
  background: 5 | 6;
}

const FileListingItem = ({ data, background }: FileListingItemProps) => {
  return (
    <UnstyledButton sx={(t) => ({ borderRadius: t.radius.sm })}>
      <Grid
        columns={20}
        align="center"
        sx={(t) => ({
          background: t.colors.dark[background],
          padding: 5,
          border: `1px solid ${t.colors.dark[8]}`,
          borderRadius: t.radius.sm,
          cursor: "pointer",
        })}
      >
        <Grid.Col span={1}>
          {data.is_directory ? (
            <IconFolder size={38} />
          ) : (
            <IconFile size={38} />
          )}
        </Grid.Col>
        <Grid.Col span={14}>
          <Text weight={700}>{data.name}</Text>
        </Grid.Col>
        <Grid.Col span={2}>
          <Text>{data.size}</Text>
        </Grid.Col>
        <Grid.Col span={3}>
          <Text>{new Date(data.created * 1000).toLocaleString()}</Text>
        </Grid.Col>
      </Grid>
    </UnstyledButton>
  );
};

export default FileListingItem;
