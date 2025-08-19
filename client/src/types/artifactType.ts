export interface IArtifactPartInfo {
  name: string;
  setName: string;
  id: number;
  type: string;
  mainStat: object;
  subStat: object[];
  icon: string;
}

export interface IArtifactSetsInfo {
  name: string;
  options: {
    type: string;
    maxStack: number;
    description: string;
    label: string;
    requiredParts: number;
  }[];
}

export interface IArtifactInfo {
  parts: IArtifactPartInfo[];
  setInfo: IArtifactSetsInfo[];
}
