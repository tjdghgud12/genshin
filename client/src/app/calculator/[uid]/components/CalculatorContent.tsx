import CharacterTabs from "@/app/calculator/[uid]/components/CharacterTabs";
import Store from "@/app/Store";
import api from "@/lib/axios";
import { IArtifactSetsInfo } from "@/types/artifactType";
import { IUidSearchResult } from "@/types/calculatorType";
import { IWeaponInfo } from "@/types/weaponType";
import { redirect } from "next/navigation";
import React from "react";

const CalculatorContent = async ({ uid }: { uid: string }): Promise<React.ReactElement> => {
  let weaponList: { [id: string]: IWeaponInfo };
  let artifactSets: { [name: string]: IArtifactSetsInfo };
  let characters: IUidSearchResult[];
  let fightPropLabels: { [fightProp: string]: string };

  try {
    weaponList = Object.fromEntries((await api.get(`/weapons`)).data.map((weapon: IWeaponInfo) => [weapon.id, weapon]));
    artifactSets = Object.fromEntries((await api.get(`/artifactsets`)).data.map((set: IArtifactSetsInfo) => [set.name, set]));
    fightPropLabels = (await api.get(`/fightPropLabels`)).data;
    characters = (await api.get(`/user/${uid}`)).data.characters;
  } catch (error) {
    console.error("Failed to fetch calculator data:", error);
    redirect(`/`);
  }

  return (
    <>
      <Store weaponList={weaponList} artifactSets={artifactSets} fightPropLabels={fightPropLabels} />
      <CharacterTabs characters={characters} />
    </>
  );
};

export default CalculatorContent;
