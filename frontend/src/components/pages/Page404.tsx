import { FC, memo } from "react";
import styled from "styled-components";

export const Page404: FC = memo(() => {
    return <Sp>404ページです。</Sp>
})

const Sp = styled.p`
    color: red;
    font-size: 24px;
    text-align: center;
`