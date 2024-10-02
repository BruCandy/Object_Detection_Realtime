import {
    Image,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalHeader,
    ModalOverlay,
  } from "@chakra-ui/react";
  import { FC, memo } from "react";
  
  type Props = {
    isOpen: boolean;
    onClose: () => void;
  };
  
  export const KamukamulModal: FC<Props> = memo((props) => {
    const { isOpen, onClose } = props;
  
    return (
      <Modal
        isOpen={isOpen}
        onClose={onClose}
        autoFocus={false}
        motionPreset="slideInBottom"
      >
        <ModalOverlay />
        <ModalContent pb={2}>
          <ModalHeader textAlign="center">かむかむレモン</ModalHeader>
          <ModalCloseButton />
          <ModalBody mx={4}>
            <Image
              src="image/kamukamu.jpg" 
              alt="かむかむレモン"
              boxSize="300px" 
              objectFit="cover" 
              mb={4} 
              mx="auto"
            />
            <p>三菱食品の商品である。</p>
            <p>
              ソフトコーティングは甘く、外生地はサクッとした口どけで、中生地は
              なめらかなチューイング性のある酸っぱさに仕上がっている。
            </p>
            <p>また、１粒にビタミンCレモン10個分配合されている。</p>
          </ModalBody>
        </ModalContent>
      </Modal>
    );
  });
  