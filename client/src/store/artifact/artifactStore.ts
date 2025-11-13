import { IArtifactSetsInfo } from "@/types/artifactType";
import { useStore } from "zustand";
import { createStore, StoreApi } from "zustand/vanilla";

let artifactSetsInfoStoreInstance: StoreApi<IArtifactSetsInfoStore> | null = null;

export interface IArtifactSetsInfoStore {
  artifactSets: { [name: string]: IArtifactSetsInfo };
  setArtifactSets: (newArtifactSets: { [name: string]: IArtifactSetsInfo }) => void;
}

const createArtifactSetsInfoStore = (initialState: IArtifactSetsInfoStore["artifactSets"]): StoreApi<IArtifactSetsInfoStore> => {
  return createStore<IArtifactSetsInfoStore>((set) => ({
    artifactSets: initialState,
    setArtifactSets: (newArtifactSets: { [name: string]: IArtifactSetsInfo }): void => set({ artifactSets: newArtifactSets }),
  }));
};

const initArtifactSetsInfoStore = (initialData: IArtifactSetsInfoStore["artifactSets"]): void => {
  if (!artifactSetsInfoStoreInstance) artifactSetsInfoStoreInstance = createArtifactSetsInfoStore(initialData);
};

const useArtifactSetsInfoStore = <T>(selector?: (state: IArtifactSetsInfoStore) => T): T => {
  if (!artifactSetsInfoStoreInstance) throw new Error("Artifact sets info store not initialized");
  return useStore(artifactSetsInfoStoreInstance, selector ?? ((state: IArtifactSetsInfoStore): T => state as T));
};

export { initArtifactSetsInfoStore, useArtifactSetsInfoStore };
