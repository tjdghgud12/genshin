import { IArtifactInfo } from "@/types/artifactType";
import { ICharacterInfo } from "@/types/characterType";
import { IWeaponInfo } from "@/types/weaponType";
import { create } from "zustand";

export interface IUserCharacterData extends ICharacterInfo {
  weapon: IWeaponInfo;
  artifacts: IArtifactInfo;
}

export interface IUserCalculaterStore {
  weaponList: IWeaponInfo[];
  calculatorData: { info: IUserCharacterData; result: object } | [];
  setWeaponList: (newWeaponList: IWeaponInfo[]) => void;
  setCharacterInfo: (newCharactersInfo: IUserCharacterData) => void;
  setCalculateData: (newResult: object) => void;
  setTotalCalculatorData: (newCalculatorData: { info: IUserCharacterData; result: object }) => void;
}

export const useCalculatorStore = create<IUserCalculaterStore>((set) => ({
  weaponList: [],
  calculatorData: [],
  setWeaponList: (newWeaponList): void => set((state) => ({ weaponList: newWeaponList })),
  setCharacterInfo: (newCharactersInfo): void => set((state) => ({ calculatorData: { ...state.calculatorData, info: newCharactersInfo } })),
  setCalculateData: (newResult): void => set((state) => ({ calculatorData: { ...state.calculatorData, result: newResult } })),
  setTotalCalculatorData: (newTotalCalculatorData): void => set({ calculatorData: newTotalCalculatorData }),
}));
