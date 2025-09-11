import { IArtifactInfo, IArtifactSetsInfo } from "@/types/artifactType";
import { IdamageCalculationResult } from "@/types/calculatorType";
import { ICharacterInfo } from "@/types/characterType";
import { IWeaponInfo } from "@/types/weaponType";
import { create } from "zustand";

export interface IUserCharacterData extends ICharacterInfo {
  weapon: IWeaponInfo;
  artifacts: IArtifactInfo;
}

export interface IUserCalculaterStore {
  weaponList: { [id: string]: IWeaponInfo };
  artifactSets: { [name: string]: IArtifactSetsInfo };
  damageResult: IdamageCalculationResult[];
  calculatorData: { info: IUserCharacterData; result: object }[];
  setWeaponList: (newWeaponList: { [id: string]: IWeaponInfo }) => void;
  setArtifactSets: (newArtifactSets: { [name: string]: IArtifactSetsInfo }) => void;
  setDamageResult: (newDamageResult: IdamageCalculationResult[]) => void;
  setCharacterInfo: (newCharactersInfo: IUserCharacterData) => void;
  setCalculateData: (newResult: object) => void;
  setTotalCalculatorData: (newCalculatorData: { info: IUserCharacterData; result: object }[]) => void;
}

export const useCalculatorStore = create<IUserCalculaterStore>((set) => ({
  weaponList: {},
  artifactSets: {},
  calculatorData: [],
  damageResult: [],
  setWeaponList: (newWeaponList): void => set(() => ({ weaponList: newWeaponList })),
  setArtifactSets: (newArtifactSets): void => set(() => ({ artifactSets: newArtifactSets })),
  setDamageResult: (newDamageResult): void => set(() => ({ damageResult: newDamageResult })),
  setCharacterInfo: (newCharactersInfo): void => set((state) => ({ calculatorData: { ...state.calculatorData, info: newCharactersInfo } })),
  setCalculateData: (newResult): void => set((state) => ({ calculatorData: { ...state.calculatorData, result: newResult } })),
  setTotalCalculatorData: (newTotalCalculatorData): void => set(() => ({ calculatorData: newTotalCalculatorData })),
}));
