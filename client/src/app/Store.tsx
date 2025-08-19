"use client";

import { useCalculatorStore } from "@/store/useCalculatorStore";
import { Fragment, ReactElement, ReactNode, useEffect } from "react";

interface StoreProps {
  children: ReactNode;
  [key: string]: any;
}

const Store = ({ children, ...props }: StoreProps): ReactElement => {
  const { setWeaponList, setArtifactSets } = useCalculatorStore();

  useEffect(() => {
    if ((props as any).weaponList) setWeaponList((props as any).weaponList);
    if ((props as any).artifactSets) setArtifactSets((props as any).artifactSets);
  }, [props, setWeaponList, setArtifactSets]);

  return <Fragment>{children}</Fragment>;
};

export default Store;
