import { Box, Image, Spinner, useDisclosure, VStack } from "@chakra-ui/react";
import { FC, memo, useEffect, useRef, useState } from "react";
import { PrimaryButton } from "../atoms/button/PrimaryButton";
import { useMessage } from "../../hooks/useMessage";
import { TsubuModal } from "../organisms/modal/TsubuModal";
import { KamukamulModal } from "../organisms/modal/KamukamuModal";

export const Home: FC = memo(() => {
  const [isVisible, setVisible] = useState(false);
  const videoRef = useRef<HTMLImageElement | null>(null);
  const websocket = useRef<WebSocket | null>(null);
  const [labels, setLabels] = useState<string[]>([]);
  const [isLoading, setLoading] = useState(true);
  const {
    isOpen: isOpenTsubu,
    onOpen: onOpenTsubu,
    onClose: onCloseTsubu,
  } = useDisclosure();
  const {
    isOpen: isOpenKamukamu,
    onOpen: onOpenKamukamu,
    onClose: onCloseKamukamu,
  } = useDisclosure();
  const { showToast } = useMessage();

  const [lastDetectedLabel, setLastDetectedLabel] = useState<string | null>(
    null
  );
  const [lastDetectedTime, setLastDetectedTime] = useState<number>(0);

  const span = 5000;

  const startWebSocket = () => {
    websocket.current = new WebSocket("ws://localhost:8001/ws");

    websocket.current.onmessage = (event) => {
      if (typeof event.data === "string") {
        const jsonDate = JSON.parse(event.data);
        setLabels(jsonDate.labels);
      } else {
        const blob = new Blob([event.data], { type: "image/jpeg" });
        const url = URL.createObjectURL(blob);
        setLoading(false);

        if (videoRef.current) {
          videoRef.current.src = url;
          setTimeout(() => URL.revokeObjectURL(url), 100);
        }
      }
    };

    websocket.current.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    websocket.current.onclose = () => {
      console.log("WebSocket connection closed.");
    };
  };

  const stopWebSocket = () => {
    if (websocket.current) {
      websocket.current.close();
      websocket.current = null;
    }
  };

  useEffect(() => {
    return () => {
      stopWebSocket();
    };
  }, []);

  useEffect(() => {
    // console.log(labels);
    // console.log(labels.length);

    const isAnyModalOpen = isOpenTsubu || isOpenKamukamu;
    const currentTime = new Date().getTime();
    // console.log("isAnyModalOpen:", isAnyModalOpen);

    if (
      labels.length >= 2 &&
      (lastDetectedLabel !== "many" || currentTime - lastDetectedTime > span)
    ) {
      showToast({
        title: "検出対象を一つに絞ってください！！！",
        onClickButton: () => {}, //onClickButtonは機能しないため、何を渡しても構わない
        isModalOpen: isAnyModalOpen,
        showButton: false,
      });
      setLastDetectedLabel("many");
      setLastDetectedTime(currentTime);
    } else if (
      labels.length === 1 &&
      labels[0] === "tsubu" &&
      (lastDetectedLabel !== "tsubu" || currentTime - lastDetectedTime > span)
    ) {
      showToast({
        title: "つぶグミを検出しました！",
        onClickButton: onOpenTsubu,
        isModalOpen: isAnyModalOpen,
        showButton: true,
      });
      setLastDetectedLabel("tsubu");
      setLastDetectedTime(currentTime);
    } else if (
      labels.length === 1 &&
      labels[0] === "kamukamu" &&
      (lastDetectedLabel !== "kamukamu" ||
        currentTime - lastDetectedTime > span)
    ) {
      showToast({
        title: "かむかむレモンを検出しました！",
        onClickButton: onOpenKamukamu,
        isModalOpen: isAnyModalOpen,
        showButton: true,
      });
      setLastDetectedLabel("kamukamu");
      setLastDetectedTime(currentTime);
    }
  }, [labels, isOpenTsubu, isOpenKamukamu]);

  const onClickStart = () => {
    setVisible(true);
    startWebSocket();
  };

  const onClickStop = () => {
    setVisible(false);
    stopWebSocket();
    setLoading(true);
  };

  return (
    <VStack spacing={4} align="center" justify="center">
      <Box height="30px" />
      {isVisible ? (
        isLoading ? (
          <Spinner size="xl" />
        ) : (
          <img
            ref={videoRef}
            alt="Waiting"
            width="400"
            height="400"
            // onLoad={() => {
            //   console.log("Image loaded");
            //   setLoading(false);
            // }}
            // onError={() => console.log("Image failed to load")}
          />
        )
      ) : (
        <Image
          src="gibbresh.png"
          fallbackSrc="https://via.placeholder.com/400"
        />
      )}
      {isVisible ? (
        <PrimaryButton onClick={onClickStop}>Stop</PrimaryButton>
      ) : (
        <PrimaryButton onClick={onClickStart}>Start</PrimaryButton>
      )}
      <TsubuModal isOpen={isOpenTsubu} onClose={onCloseTsubu} />
      <KamukamulModal isOpen={isOpenKamukamu} onClose={onCloseKamukamu} />
    </VStack>
  );
});
