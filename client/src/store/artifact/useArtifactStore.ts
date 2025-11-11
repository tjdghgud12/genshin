"use client";

import { IArtifactSetsInfoStore, artifactSetsInfoStore } from "@/store/artifact/artifactStore";
import { useStore } from "zustand";

export function useArtifactSetsInfoStore(): IArtifactSetsInfoStore;
export function useArtifactSetsInfoStore<T>(selector: (state: IArtifactSetsInfoStore) => T): T;
export function useArtifactSetsInfoStore<T>(selector?: (state: IArtifactSetsInfoStore) => T): T | IArtifactSetsInfoStore {
  return useStore(artifactSetsInfoStore, selector ?? ((state: IArtifactSetsInfoStore): T => state as T));
}
