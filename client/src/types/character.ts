export interface ICharacterInfo {
  name: string;
  level: number;
  ascension: number;
  icon: { [key: string]: string | boolean };
  passiveSkill: {
    type: string;
    maxStack: number;
    description: string;
    unlockLevel: number;
    name: string;
    icon: string;
    unlocked: boolean;
    active: boolean;
    stack: number;
  }[];
  activeSkill: {
    name: string;
    level: number;
    type: string;
    icon: string;
    description: string;
    active: boolean;
    stack: number;
  }[];
  constellations: {
    name: string;
    type: string;
    maxStack: number;
    description: string;
    icon: string;
    unlocked: boolean;
    active: boolean;
    stack: number;
  }[];
  totalStat: object;
}
