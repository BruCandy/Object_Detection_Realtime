import { Page404 } from "../components/pages/Page404";
import { Route, Routes } from "react-router-dom";
import { Home } from "../components/pages/Home";
import { HeaderLayout } from "../components/templates/HeaderLayout";
import { ImageProvider } from "../providers/ImageProvider";

export const Router = () => {
  return (
    <ImageProvider>
      {" "}
      <Routes>
        <Route
          path="/"
          element={
            <HeaderLayout>
              <Home />
            </HeaderLayout>
          }
        />
        <Route path="*" element={<Page404 />} />
      </Routes>
    </ImageProvider>
  );
};