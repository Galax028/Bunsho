import { ScrollArea, Stack } from "@mantine/core";
import { useViewportSize } from "@mantine/hooks";
import FileListingItem, { FileListingItemProps } from "./FileListingItem";

export interface FileListingProps {
  items: [FileListingItemProps["data"]];
}

const FileListing = ({ items }: FileListingProps) => {
  const { height } = useViewportSize();
  const folderItems = items
    .filter((item) => item.is_directory)
    .sort((a, b) => a.name.localeCompare(b.name));
  const fileItems = items
    .filter((item) => !item.is_directory)
    .sort((a, b) => a.name.localeCompare(b.name));

  return (
    <ScrollArea sx={{ height: height - 100 }} scrollbarSize={5}>
      <Stack p="xl">
        {folderItems.map((item, index) => (
          <FileListingItem
            data={item}
            key={index}
            background={index % 2 === 0 ? 5 : 6}
          />
        ))}
        {fileItems.map((item, index) => (
          <FileListingItem
            data={item}
            key={index}
            background={index % 2 === 0 ? 5 : 6}
          />
        ))}
      </Stack>
    </ScrollArea>
  );
};

export default FileListing;
