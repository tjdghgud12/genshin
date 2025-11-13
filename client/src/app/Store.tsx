"use client";

import { initArtifactSetsInfoStore } from "@/store/artifact/artifactStore";
import { initWeaponInfoStore } from "@/store/weapon/weaponStore";
import { IArtifactSetsInfo } from "@/types/artifactType";
import { IWeaponInfo } from "@/types/weaponType";
import { Fragment, useRef } from "react";

const Store = ({ weaponList, artifactSets }: { weaponList: { [id: string]: IWeaponInfo }; artifactSets: { [name: string]: IArtifactSetsInfo } }) => {
  const initialized = useRef(false);

  if (!initialized.current) {
    initWeaponInfoStore(weaponList);
    initArtifactSetsInfoStore(artifactSets);

    initialized.current = true;
  }

  return <Fragment />;
};

export default Store;
