export interface IArtifactInfo {
  parts: {
    name: string;
    setName: string;
    id: number;
    type: string;
    mainStat: object;
    subStat: object[];
    icon: string;
  }[];
  setInfo: {
    name: string;
    option: {
      type: string;
      maxStack: number;
      description: string;
      active: boolean;
      stack: string;
    }[];
  }[];
}
