import { IWeaponInfo } from "@/types/weaponType";
import { createStore } from "zustand/vanilla";

export interface IWeaponInfoStore {
  weaponList: { [id: string]: IWeaponInfo };
  setWeaponList: (newWeaponList: { [id: string]: IWeaponInfo }) => void;
}

export const weaponInfoStore = createStore<IWeaponInfoStore>(() => ({
  weaponList: {},
  setWeaponList: (newWeaponList: { [id: string]: IWeaponInfo }): void => weaponInfoStore.setState({ weaponList: newWeaponList }),
}));
