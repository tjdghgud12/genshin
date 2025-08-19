"use client";

import { useCalculatorStore } from "@/store/useCalculatorStore";
import { Fragment, ReactElement, ReactNode, useEffect } from "react";

interface StoreProps {
  children: ReactNode;
  [key: string]: any;
}

const Store = ({ children, weaponList, artifactSets, ...props }: StoreProps): ReactElement => {
  const { setWeaponList, setArtifactSets } = useCalculatorStore();

  useEffect(() => {
    if (weaponList) setWeaponList(weaponList);
  }, [weaponList, setWeaponList]);

  useEffect(() => {
    if (artifactSets) setArtifactSets(artifactSets);
  }, [artifactSets, setArtifactSets]);

  return <Fragment>{children}</Fragment>;
};

export default Store;
