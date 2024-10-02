import { Flex, Heading } from "@chakra-ui/react";
import { FC, memo } from "react";

export const Header: FC = memo(() => {
  return (
    <>
      <Flex
        as="nav"
        bg="green.500"
        color="gray.50"
        align="center"
        justify="space-between"
        padding={{ base: 3, md: 5 }}
      >
        <Flex align="center" as="a" mr={8}>
          <Heading as="h1" fontSize={{ base: "md", md: "lg" }}>
            Realtime Object Detection
          </Heading>
        </Flex>
      </Flex>
    </>
  );
});
