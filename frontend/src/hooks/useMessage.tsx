import { Box, Button, useToast } from "@chakra-ui/react";
import { MouseEvent, useCallback, useState } from "react";

type Props = {
  title: string;
  onClickButton: (event: MouseEvent<HTMLButtonElement>) => void;
  isModalOpen: boolean;
  showButton?: boolean;
};

export const useMessage = () => {
  const toast = useToast();
  const [isToastOpen, setToastOpen] = useState(false);

  const showToast = useCallback(
    (props: Props) => {
      const { title, onClickButton, isModalOpen, showButton } = props;

      if (!isModalOpen && !isToastOpen) {
        toast.closeAll();

        toast({
          title: title,
          status: "info",
          position: "top",
          duration: 5000,
          isClosable: true,
          description: showButton ? (
            <Box display="flex" justifyContent="right" mt={4}>
              <Button
                onClick={(event) => {
                  toast.closeAll();
                  onClickButton(event);
                  setToastOpen(true);
                }}
              >
                詳細
              </Button>
            </Box>
          ) : null,
          onCloseComplete: () => {
            setToastOpen(false);
          },
        });
      }
    },
    [toast]
  );

  return { showToast };
};
