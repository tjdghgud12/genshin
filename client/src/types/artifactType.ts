export interface IArtifactOptionInfo {
  key: string;
  value: number | string;
}

export interface IArtifactPartInfo {
  name: string;
  setName: string;
  id: number;
  type: string;
  mainStat: Record<string, number>;
  subStat: Record<string, number>[];
  icon: string;
}

export interface IArtifactSetsInfo {
  name: string;
  id: number;
  icon: string;
  numberOfParts: number;
  affix_list: { id: string; effect: string }[];
  options: {
    type: string;
    maxStack: number;
    description: string;
    label: string;
    requiredParts: number;
    active: boolean;
    stack: number;
    select: string | null;
    selectList: string[];
  }[];
}

export interface IArtifactInfo {
  parts: IArtifactPartInfo[];
  setInfo: IArtifactSetsInfo[];
}
