export interface IWeaponInfo {
  id: number;
  rarity: number;
  type: string;
  name: string;
  icon: string;
  route: string;
  option: {
    type: string;
    maxStack: number;
    description: string;
    label: string;
  }[];
}
