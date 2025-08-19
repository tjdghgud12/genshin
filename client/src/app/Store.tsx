"use client";

import { useCalculatorStore } from "@/store/useCalculatorStore";
import { IArtifactSetsInfo } from "@/types/artifactType";
import { IWeaponInfo } from "@/types/weaponType";
import { Fragment, ReactElement, ReactNode, useEffect } from "react";

interface StoreProps {
  children: ReactNode;
  weaponList?: IWeaponInfo[];
  artifactSets?: IArtifactSetsInfo[];
}

const Store = ({ children, weaponList, artifactSets, ..._props }: StoreProps): ReactElement => {
  const { setWeaponList, setArtifactSets } = useCalculatorStore();

  useEffect(() => {
    if (weaponList) setWeaponList(weaponList);
    if (artifactSets) setArtifactSets(artifactSets);
  }, [weaponList, artifactSets, setWeaponList, setArtifactSets]);

  return <Fragment>{children}</Fragment>;
};

export default Store;
