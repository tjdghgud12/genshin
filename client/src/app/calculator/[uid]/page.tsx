import CharacterTabs from "@/app/calculator/[uid]/components/CharacterTabs";
import UidSearchInput from "@/app/globalComponents/UidSearchInput";
import RootLoading from "@/app/loading";
import Store from "@/app/Store";
import api from "@/lib/axios";
import { IArtifactSetsInfo } from "@/types/artifactType";
import { IUidSearchResult } from "@/types/calculatorType";
import { IWeaponInfo } from "@/types/weaponType";
import Image from "next/image";
import Link from "next/link";
import { redirect } from "next/navigation";
import React, { Suspense } from "react";

const CalculatorPage = async ({ params }: { params: Promise<{ uid: string }> }): Promise<React.ReactElement> => {
  const { uid } = await params;

  try {
    const weaponList = Object.fromEntries((await api.get(`/weapons`)).data.map((weapon: IWeaponInfo) => [weapon.id, weapon]));
    const artifactSets = Object.fromEntries((await api.get(`/artifactsets`)).data.map((set: IArtifactSetsInfo) => [set.name, set]));
    const characters: IUidSearchResult[] = (await api.get(`/user/${uid}`)).data.characters;

    return (
      <main className="w-full h-full min-h-[500px] flex flex-col">
        <Suspense fallback={<RootLoading />} key={`${uid}-${Date.now()}`}>
          <div className="w-full flex">
            {/* Header */}
            <Link className="w-[80px] h-[80px] relative rounded-full py-1 px-3" href={`/`}>
              <Image src={`/img/homeIcon.png`} alt="" fill priority sizes="(max-width: 1200px) 7vw, 80px" />
            </Link>
            <UidSearchInput className="m-auto" value={uid} />
          </div>
          <Store weaponList={weaponList} artifactSets={artifactSets} />
          <CharacterTabs characters={characters} />
        </Suspense>
      </main>
    );
  } catch (error) {
    console.error(error);
    redirect(`/`);
  }
};

export default CalculatorPage;
