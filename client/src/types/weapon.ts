export interface IWeaponInfo {
  id: number;
  name: string;
  refinement: number;
  level: number;
  icon: string;
  option: {
    type: string;
    maxStack: number;
    description: string;
    active: boolean;
    stack: number;
  }[];
  stat: object;
}
