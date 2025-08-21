export interface IArtifactOptionInfo {
  key: string;
  value: number | string;
}

export interface IArtifactPartInfo {
  name: string;
  setName: string;
  id: number;
  type: string;
  mainStat: IArtifactOptionInfo;
  subStat: IArtifactOptionInfo[];
  icon: string;
}

export interface IArtifactSetsInfo {
  name: string;
  id: number;
  icon: string;
  affix_list: { id: string; effect: string }[];
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
