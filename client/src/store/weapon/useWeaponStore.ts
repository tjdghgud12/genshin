"use client";

import { IWeaponInfoStore, weaponInfoStore } from "@/store/weapon/weaponStore";
import { useStore } from "zustand";

export function useWeaponInfoStore(): IWeaponInfoStore;
export function useWeaponInfoStore<T>(selector: (state: IWeaponInfoStore) => T): T;
export function useWeaponInfoStore<T>(selector?: (state: IWeaponInfoStore) => T): T | IWeaponInfoStore {
  return useStore(weaponInfoStore, selector ?? ((state: IWeaponInfoStore): T => state as T));
}
