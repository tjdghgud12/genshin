export interface IWeaponInfo {
  id: number;
  rarity: number;
  type: string;
  name: string;
  icon: string;
  route: string;
  options: {
    type: string;
    maxStack: number;
    description: string;
    label: string;
    select: string;
    selectList: string[];
  }[];
}
