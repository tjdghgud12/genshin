"";
import { useStore } from "zustand";
import { createStore, StoreApi } from "zustand/vanilla";

let fightPropLabelStoreInstance: StoreApi<IFightPropLabelStore> | null = null;

export interface IFightPropLabelStore {
  fightPropLabels: { [fightProp: string]: string };
  setFightPropLabels: (newFightPropLabels: { [fightProp: string]: string }) => void;
}

const createFightPropLabelStore = (initialState: IFightPropLabelStore["fightPropLabels"]): StoreApi<IFightPropLabelStore> => {
  return createStore<IFightPropLabelStore>((set) => ({
    fightPropLabels: initialState,
    setFightPropLabels: (newFightPropLabels: { [fightProp: string]: string }): void => set({ fightPropLabels: newFightPropLabels }),
  }));
};

const initFightPropLabelStore = (initialData: IFightPropLabelStore["fightPropLabels"]): void => {
  if (!fightPropLabelStoreInstance) fightPropLabelStoreInstance = createFightPropLabelStore(initialData);
};

const useFightPropLabelStore = <T>(selector?: (state: IFightPropLabelStore) => T): T => {
  if (!fightPropLabelStoreInstance) throw new Error("Fight prop label store not initialized");
  return useStore(fightPropLabelStoreInstance, selector ? selector : (state: IFightPropLabelStore): T => state as T);
};

const getFightPropLabels = (): IFightPropLabelStore["fightPropLabels"] => fightPropLabelStoreInstance?.getState().fightPropLabels ?? {};

export { getFightPropLabels, initFightPropLabelStore, useFightPropLabelStore };
