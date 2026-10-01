import { useContext } from "react";
import { BusinessContext } from "./BusinessContextValue";

export const useBusiness = () => useContext(BusinessContext);
