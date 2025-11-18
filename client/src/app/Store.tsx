"use client";

import { initArtifactSetsInfoStore } from "@/store/artifactStore";
import { initWeaponInfoStore } from "@/store/weaponStore";
import { IArtifactSetsInfo } from "@/types/artifactType";
import { IWeaponInfo } from "@/types/weaponType";
import { Fragment, useRef } from "react";

const Store = ({ weaponList, artifactSets }: { weaponList: { [id: string]: IWeaponInfo }; artifactSets: { [name: string]: IArtifactSetsInfo } }): React.ReactElement => {
  const initialized = useRef(false);

  if (!initialized.current) {
    initWeaponInfoStore(weaponList);
    initArtifactSetsInfoStore(artifactSets);

    initialized.current = true;
  }

  return <Fragment />;
};

export default Store;
