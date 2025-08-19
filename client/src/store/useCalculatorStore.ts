import { IArtifactInfo, IArtifactSetsInfo } from "@/types/artifactType";
import { ICharacterInfo } from "@/types/characterType";
import { IWeaponInfo } from "@/types/weaponType";
import { create } from "zustand";

export interface IUserCharacterData extends ICharacterInfo {
  weapon: IWeaponInfo;
  artifacts: IArtifactInfo;
}

export interface IUserCalculaterStore {
  weaponList: IWeaponInfo[];
  artifactSets: IArtifactSetsInfo[];
  calculatorData: { info: IUserCharacterData; result: object } | [];
  setWeaponList: (newWeaponList: IWeaponInfo[]) => void;
  setArtifactSets: (newArtifactSets: IArtifactSetsInfo[]) => void;
  setCharacterInfo: (newCharactersInfo: IUserCharacterData) => void;
  setCalculateData: (newResult: object) => void;
  setTotalCalculatorData: (newCalculatorData: { info: IUserCharacterData; result: object }) => void;
}

export const useCalculatorStore = create<IUserCalculaterStore>((set) => ({
  weaponList: [],
  artifactSets: [],
  calculatorData: [],
  setWeaponList: (newWeaponList): void => set(() => ({ weaponList: newWeaponList })),
  setArtifactSets: (newArtifactSets): void => set(() => ({ artifactSets: newArtifactSets })),
  setCharacterInfo: (newCharactersInfo): void => set((state) => ({ calculatorData: { ...state.calculatorData, info: newCharactersInfo } })),
  setCalculateData: (newResult): void => set((state) => ({ calculatorData: { ...state.calculatorData, result: newResult } })),
  setTotalCalculatorData: (newTotalCalculatorData): void => set({ calculatorData: newTotalCalculatorData }),
}));
