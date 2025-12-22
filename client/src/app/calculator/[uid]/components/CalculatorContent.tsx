import CharacterTabs from "@/app/calculator/[uid]/components/CharacterTabs";
import Store from "@/app/Store";
import api from "@/lib/axios";
import { IArtifactSetsInfo } from "@/types/artifactType";
import { IUidSearchResult } from "@/types/calculatorType";
import { IWeaponInfo } from "@/types/weaponType";
import { redirect } from "next/navigation";
import React from "react";

/**
 * 데이터를 조회하고 하위 컴포넌트에 전달하는 서버 컴포넌트
 * Suspense 내부에서 사용되어 데이터 조회 중 fallback을 표시합니다.
 */
const CalculatorContent = async ({ uid }: { uid: string }): Promise<React.ReactElement> => {
  try {
    const weaponList = Object.fromEntries((await api.get(`/weapons`)).data.map((weapon: IWeaponInfo) => [weapon.id, weapon]));
    const artifactSets = Object.fromEntries((await api.get(`/artifactsets`)).data.map((set: IArtifactSetsInfo) => [set.name, set]));
    const characters: IUidSearchResult[] = (await api.get(`/user/${uid}`)).data.characters;

    return (
      <>
        <Store weaponList={weaponList} artifactSets={artifactSets} />
        <CharacterTabs characters={characters} />
      </>
    );
  } catch (error) {
    console.error(error);
    redirect(`/`);
  }
};

export default CalculatorContent;
