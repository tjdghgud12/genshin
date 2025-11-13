import { IArtifactInfo } from "@/types/artifactType";
import { IWeaponInfo } from "@/types/weaponType";

export type TElement = "Fire" | "Water" | "Wind" | "Electric" | "Ice" | "Rock" | "Grass";

export interface IattackDamage {
  // 기본
  physicalDamage: number;
  elementalDamage: number;

  // 증폭
  meltDamage: number; // 융해
  reverseMeltDamage: number; // 역융해
  vaporizeDamage: number; // 증발
  reverseVaporizeDamage: number; // 역증발

  // 격화
  aggravateDamage: number; // 촉진
  spreadDamage: number; // 발산

  // 추가 계수
  physicalDamageAdditional: number; // 계수 추가 물리 데미지
  elementalDamageAdditional: number; // 계수 추가 원소 데미지
  meltDamageAdditional: number; // 계수 추가 융해
  reverseMeltDamageAdditional: number; // 계수 추가 역융해
  vaporizeDamageAdditional: number; // 계수 추가 증발
  reverseVaporizeDamageAdditional: number; // 계수 추가 역증발
}

export interface IdamageCalculationResult {
  // 일반 공격
  nomal: IattackDamage;
  nomalCritical: IattackDamage;
  nomalNonCritical: IattackDamage;
  // 강 공격
  charge: IattackDamage;
  chargeCritical: IattackDamage;
  chargeNonCritical: IattackDamage;
  // 낙하 공격
  falling: IattackDamage;
  fallingCritical: IattackDamage;
  fallingNonCritical: IattackDamage;
  // 원소 전투 스킬
  elementalSkill: IattackDamage;
  elementalSkillCritical: IattackDamage;
  elementalSkillNonCritical: IattackDamage;
  // 원소 폭발
  elementalBurst: IattackDamage;
  elementalBurstCritical: IattackDamage;
  elementalBurstNonCritical: IattackDamage;
  // 추가 타격
  custom: { [key: string]: IattackDamage };
  customCritical: { [key: string]: IattackDamage };
  customNonCritical: { [key: string]: IattackDamage };

  // 격변
  overloadedDamage: number; // 과부하
  electroChargedDamage: number; // 감전
  superconductDamage: number; // 초전도
  shatterDamage: number; // 쇄빙

  // 개별 치명타 옵션 보유 반응
  bloomDamage: number; // 개화 기대값
  bloomDamageCritical: number; // 개화 치명타
  bloomDamageNonCritical: number; // 개화 논치명타
  hyperBloomDamage: number; // 만개 기대값
  hyperBloomDamageCritical: number; // 만개 치명타
  hyperBloomDamageNonCritical: number; // 만개 논치명타
  burgeonDamage: number; // 발화 기대값
  burgeonDamageCritical: number; // 발화 치명타
  burgeonDamageNonCritical: number; // 발화 논치명타
  burningDamage: number; // 연소 기대값
  burningDamageCritical: number; // 연소 치명타
  burningDamageNonCritical: number; // 연소 논치명타

  // 달반응
  lunarChargedDamage: number; // 달감전 기대값
  lunarChargedDamageCritical: number; // 달감전 치명타
  lunarChargedDamageNonCritical: number; // 달감전 논치명타

  // 확산
  fireSwirlDamage: number; // 불확산
  waterSwirlDamage: number; // 물확산
  iceSwirlDamage: number; // 얼음확산
  elecSwirlDamage: number; // 번개확산
}

export interface IUidSearchResult {
  characterInfo: {
    level: number;
    name: string;
    element: TElement;
    icon: Record<string, string> & { is_costume: boolean };
    activeSkill: (Record<string, string | number | boolean | object> & {
      icon: string;
      level: number;
      name: string;
      description: string;
      options: (Record<string, string | number | boolean | object> & {
        type: string;
        label: string;
        maxStack: number;
        active: boolean;
        stack: number;
      })[];
    })[];
    passiveSkill: (Record<string, string | number | boolean | object> & {
      unlocked: boolean;
      icon: string;
      name: string;
      description: string;
      options: (Record<string, string | number | boolean | object> & {
        type: string;
        label: string;
        maxStack: number;
        active: boolean;
        stack: number;
      })[];
    })[];
    constellations: (Record<string, string | number | boolean | object> & {
      unlocked: boolean;
      icon: string;
      name: string;
      description: string;
      options: (Record<string, string | number | boolean | object> & {
        type: string;
        label: string;
        maxStack: number;
        active: boolean;
        stack: number;
      })[];
    })[];
    artifact: IArtifactInfo;

    weapon: IWeaponInfo;
    totalStat: Record<string, number>;
  };
  damage: IdamageCalculationResult | null;
}
