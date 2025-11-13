import { IWeaponInfo } from "@/types/weaponType";
import { useStore } from "zustand";
import { createStore, StoreApi } from "zustand/vanilla";

let weaponStoreInstance: StoreApi<IWeaponInfoStore> | null = null;

export interface IWeaponInfoStore {
  weaponList: { [id: string]: IWeaponInfo };
  setWeaponList: (newWeaponList: { [id: string]: IWeaponInfo }) => void;
}

const createWeaponInfoStore = (initialState: IWeaponInfoStore["weaponList"]): StoreApi<IWeaponInfoStore> => {
  return createStore<IWeaponInfoStore>((set) => ({
    weaponList: initialState,
    setWeaponList: (newWeaponList: { [id: string]: IWeaponInfo }): void => set({ weaponList: newWeaponList }),
  }));
};

const initWeaponInfoStore = (initialData: IWeaponInfoStore["weaponList"]): void => {
  if (!weaponStoreInstance) {
    weaponStoreInstance = createWeaponInfoStore(initialData); // ✅ 여기에 저장!
  }
};

const useWeaponInfoStore = <T>(selector?: (state: IWeaponInfoStore) => T): T => {
  if (!weaponStoreInstance) throw new Error("Weapon store not initialized");
  return useStore(weaponStoreInstance, selector ? selector : (state: IWeaponInfoStore): T => state as T);
};

export { initWeaponInfoStore, useWeaponInfoStore };
