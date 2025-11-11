import { IArtifactSetsInfo } from "@/types/artifactType";
import { createStore } from "zustand/vanilla";

export interface IArtifactSetsInfoStore {
  artifactSets: { [name: string]: IArtifactSetsInfo };
  setArtifactSets: (newArtifactSets: { [name: string]: IArtifactSetsInfo }) => void;
}

export const artifactSetsInfoStore = createStore<IArtifactSetsInfoStore>(() => ({
  artifactSets: {},
  setArtifactSets: (newArtifactSets: { [name: string]: IArtifactSetsInfo }): void => artifactSetsInfoStore.setState({ artifactSets: newArtifactSets }),
}));
