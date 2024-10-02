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
  
  export const TsubuModal: FC<Props> = memo((props) => {
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
          <ModalHeader textAlign="center">つぶグミ ソーダ</ModalHeader>
          <ModalCloseButton />
          <ModalBody mx={4}>
            <Image
              src="image/tsubu.jpg" 
              alt="つぶグミ ソーダ"
              boxSize="300px" 
              objectFit="cover" 
              mb={4} 
              mx="auto"
            />
            <p>通常のつぶグミのソーダ版である。</p>
            <p>
              コーラ、サイダー、メロンソーダ、グレープソーダ、ジンジャーエールの５種類のソーダ味があり、硬め触感でとてもおいしい
            </p>
            <p>通常のつぶぐみ、つぶグミバカンス、つぶグミPREMIUMがある。</p>
          </ModalBody>
        </ModalContent>
      </Modal>
    );
  });
  