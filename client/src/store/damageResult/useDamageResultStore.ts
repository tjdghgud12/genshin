"use client";

import { IDamageResultStore, damageResultStore } from "@/store/damageResult/damageResultStore";
import { useStore } from "zustand";

export function useDamageResultStore(): IDamageResultStore;
export function useDamageResultStore<T>(selector: (state: IDamageResultStore) => T): T;
export function useDamageResultStore<T>(selector?: (state: IDamageResultStore) => T): T | IDamageResultStore {
  return useStore(damageResultStore, selector ?? ((state: IDamageResultStore): T => state as T));
}
