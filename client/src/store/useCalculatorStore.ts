import { IArtifactSetsInfo } from "@/types/artifactType";
import { IdamageCalculationResult } from "@/types/calculatorType";
import { IWeaponInfo } from "@/types/weaponType";
import { create } from "zustand";

export interface IUserCalculaterStore {
  weaponList: { [id: string]: IWeaponInfo };
  artifactSets: { [name: string]: IArtifactSetsInfo };
  damageResult: (IdamageCalculationResult | null)[];
  setWeaponList: (newWeaponList: { [id: string]: IWeaponInfo }) => void;
  setArtifactSets: (newArtifactSets: { [name: string]: IArtifactSetsInfo }) => void;
  setDamageResult: (newDamageResult: (IdamageCalculationResult | null)[]) => void;
}

export const useCalculatorStore = create<IUserCalculaterStore>((set) => ({
  weaponList: {},
  artifactSets: {},
  damageResult: [],
  setWeaponList: (newWeaponList): void => set(() => ({ weaponList: newWeaponList })),
  setArtifactSets: (newArtifactSets): void => set(() => ({ artifactSets: newArtifactSets })),
  setDamageResult: (newDamageResult): void => set(() => ({ damageResult: newDamageResult })),
}));
