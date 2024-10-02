import { Button } from "@chakra-ui/react";
import { FC, memo, ReactNode } from "react";

type Props = {
  children: ReactNode;
  disabled?: boolean;
  loading?: boolean;
  type?: "button" | "submit" | "reset";
  onClick?: () => void;
};

export const PrimaryButton: FC<Props> = memo((props) => {
  const {
    children,
    disabled = false,
    loading = false,
    onClick,
    type = "button",
  } = props;

  return (
    <Button
      bg="teal.400"
      color="white"
      _hover={{ opacity: 0.8 }}
      isDisabled={disabled || loading}
      isLoading={loading}
      onClick={onClick}
      type={type}
    >
      {children}
    </Button>
  );
});