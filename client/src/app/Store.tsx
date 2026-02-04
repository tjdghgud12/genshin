"use client";

import { initArtifactSetsInfoStore } from "@/store/artifactStore";
import { initFightPropLabelStore } from "@/store/figthtPropLabelStore";
import { initWeaponInfoStore } from "@/store/weaponStore";
import { IArtifactSetsInfo } from "@/types/artifactType";
import { IWeaponInfo } from "@/types/weaponType";
import { Fragment } from "react";

const Store = ({
  weaponList,
  artifactSets,
  fightPropLabels,
}: {
  weaponList: { [id: string]: IWeaponInfo };
  artifactSets: { [name: string]: IArtifactSetsInfo };
  fightPropLabels: { [fightProp: string]: string };
}): React.ReactElement => {
  initWeaponInfoStore(weaponList);
  initArtifactSetsInfoStore(artifactSets);
  initFightPropLabelStore(fightPropLabels);

  return <Fragment />;
};

export default Store;
