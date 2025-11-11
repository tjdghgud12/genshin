import { IdamageCalculationResult } from "@/types/calculatorType";
import { createStore } from "zustand/vanilla";

export interface IDamageResultStore {
  damageResult: (IdamageCalculationResult | null)[];
  setDamageResult: (newDamageResult: (IdamageCalculationResult | null)[]) => void;
}

export const damageResultStore = createStore<IDamageResultStore>(() => ({
  damageResult: [],
  setDamageResult: (newDamageResult: (IdamageCalculationResult | null)[]): void => damageResultStore.setState({ damageResult: newDamageResult }),
}));
