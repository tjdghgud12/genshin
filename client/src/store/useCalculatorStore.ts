import { IArtifactInfo } from "@/types/artifact";
import { ICharacterInfo } from "@/types/character";
import { IWeaponInfo } from "@/types/weapon";
import { create } from "zustand";

interface IUserCharacterData extends ICharacterInfo {
  weapon: IWeaponInfo;
  artifacts: IArtifactInfo;
}

interface IUserCalculaterStore {
  calculatorData: { info: IUserCharacterData; result: object } | [];
  setCharacterInfo: (newCharactersInfo: IUserCharacterData) => void;
  setCalculateData: (newResult: object) => void;
  setTotalCalculatorData: (newCalculatorData: { info: IUserCharacterData; result: object }) => void;
}

export const useCalculatorStore = create<IUserCalculaterStore>((set) => ({
  calculatorData: [],
  setCharacterInfo: (newCharactersInfo): void => set((state) => ({ calculatorData: { ...state.calculatorData, info: newCharactersInfo } })),
  setCalculateData: (newResult): void => set((state) => ({ calculatorData: { ...state.calculatorData, result: newResult } })),
  setTotalCalculatorData: (newTotalCalculatorData): void => set({ calculatorData: newTotalCalculatorData }),
}));
