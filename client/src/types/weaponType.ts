export interface IWeaponInfo {
  id: number;
  rarity: number;
  type: string;
  name: string;
  icon: string;
  route: string;
  level: number;
  refinement: number;
  options: (Record<string, string | number | boolean | object> & {
    type: string;
    maxStack: number;
    description: string;
    label: string;
    select: string;
    selectList: string[];
    active: boolean;
    stack: number;
  })[];
}
