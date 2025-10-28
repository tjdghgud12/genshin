import { z } from "zod";

const fightPropsSchema = z.object({
  FIGHT_PROP_BASE_HP: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_HP: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_HP_PERCENT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_BASE_ATTACK: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ATTACK: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ATTACK_PERCENT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_BASE_DEFENSE: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_DEFENSE: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_DEFENSE_PERCENT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEMENT_MASTERY: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_CHARGE_EFFICIENCY: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_CRITICAL: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_CRITICAL_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_PHYSICAL_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_FIRE_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEC_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_WATER_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_GRASS_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_WIND_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ROCK_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ICE_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ATTACK_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_PHYSICAL_RES_MINUS: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_FIRE_RES_MINUS: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_WATER_RES_MINUS: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ICE_RES_MINUS: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEC_RES_MINUS: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_GRASS_RES_MINUS: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_WIND_RES_MINUS: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ROCK_RES_MINUS: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_DEFENSE_MINUS: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_DEFENSE_IGNORE: z.number({ error: "입력한 값을 확인해주세요." }).default(0),

  // 일반공격 관련
  FIGHT_PROP_NOMAL_ATTACK_CRITICAL: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_NOMAL_ATTACK_CRITICAL_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_NOMAL_ATTACK_FIRE_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_NOMAL_ATTACK_ELEC_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_NOMAL_ATTACK_WATER_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_NOMAL_ATTACK_GRASS_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_NOMAL_ATTACK_WIND_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_NOMAL_ATTACK_ROCK_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_NOMAL_ATTACK_ICE_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_NOMAL_ATTACK_ATTACK_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),

  // 강공격 관련
  FIGHT_PROP_CHARGED_ATTACK_CRITICAL: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_CHARGED_ATTACK_CRITICAL_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_CHARGED_ATTACK_FIRE_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_CHARGED_ATTACK_ELEC_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_CHARGED_ATTACK_WATER_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_CHARGED_ATTACK_GRASS_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_CHARGED_ATTACK_WIND_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_CHARGED_ATTACK_ROCK_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_CHARGED_ATTACK_ICE_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_CHARGED_ATTACK_ATTACK_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),

  // 낙하공격 관련
  FIGHT_PROP_FALLING_ATTACK_CRITICAL: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_FALLING_ATTACK_CRITICAL_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_FALLING_ATTACK_FIRE_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_FALLING_ATTACK_ELEC_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_FALLING_ATTACK_WATER_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_FALLING_ATTACK_GRASS_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_FALLING_ATTACK_WIND_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_FALLING_ATTACK_ROCK_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_FALLING_ATTACK_ICE_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_FALLING_ATTACK_ATTACK_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),

  // 원소 전투 스킬 관련
  FIGHT_PROP_ELEMENT_SKILL_CRITICAL: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEMENT_SKILL_CRITICAL_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEMENT_SKILL_FIRE_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEMENT_SKILL_ELEC_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEMENT_SKILL_WATER_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEMENT_SKILL_GRASS_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEMENT_SKILL_WIND_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEMENT_SKILL_ROCK_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEMENT_SKILL_ICE_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEMENT_SKILL_ATTACK_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),

  // 원소 폭발 관련
  FIGHT_PROP_ELEMENT_BURST_CRITICAL: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEMENT_BURST_CRITICAL_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEMENT_BURST_FIRE_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEMENT_BURST_ELEC_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEMENT_BURST_WATER_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEMENT_BURST_GRASS_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEMENT_BURST_WIND_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEMENT_BURST_ROCK_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEMENT_BURST_ICE_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),
  FIGHT_PROP_ELEMENT_BURST_ATTACK_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0),

  // 원소 반응 관련
  FIGHT_PROP_OVERLOADED_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0), // 과부하
  FIGHT_PROP_ELECTROCHARGED_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0), // 감전
  FIGHT_PROP_SUPERCONDUCT_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0), // 초전도
  FIGHT_PROP_SHATTER_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0), // 쇄빙
  FIGHT_PROP_HYPERBLOOM_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0), // 만개
  FIGHT_PROP_BLOOM_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0), // 개화
  FIGHT_PROP_AGGRAVATE_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0), // 촉진
  FIGHT_PROP_SPREAD_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0), // 발산
  FIGHT_PROP_VAPORIZE_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0), // 증발
  FIGHT_PROP_MELT_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0), // 융해
  FIGHT_PROP_BURNING_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0), // 연소
  FIGHT_PROP_IGNITION_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0), // 발화
  FIGHT_PROP_LUNARCHARGED_ADD_HURT: z.number({ error: "입력한 값을 확인해주세요." }).default(0), // 달감전
});

const fightPropLabels: Record<string, string> = {
  FIGHT_PROP_BASE_HP: `기초 체력`,
  FIGHT_PROP_HP: `체력`,
  FIGHT_PROP_HP_PERCENT: `체력(%)`,
  FIGHT_PROP_BASE_ATTACK: `기초 공격력`,
  FIGHT_PROP_ATTACK: `공격력`,
  FIGHT_PROP_ATTACK_PERCENT: `공격력(%)`,
  FIGHT_PROP_BASE_DEFENSE: `기초 방어력`,
  FIGHT_PROP_DEFENSE: `방어력`,
  FIGHT_PROP_DEFENSE_PERCENT: `방어력(%)`,
  FIGHT_PROP_ELEMENT_MASTERY: `원소 마스터리`,
  FIGHT_PROP_CHARGE_EFFICIENCY: `원소 충전 효율(%)`,
  FIGHT_PROP_CRITICAL: `치명타 확률(%)`,
  FIGHT_PROP_CRITICAL_HURT: `치명타 피해(%)`,
  FIGHT_PROP_PHYSICAL_ADD_HURT: `물리 피해 보너스(%)`,
  FIGHT_PROP_FIRE_ADD_HURT: `불 원소 피해 보너스(%)`,
  FIGHT_PROP_ELEC_ADD_HURT: `번개 원소 피해 보너스(%)`,
  FIGHT_PROP_WATER_ADD_HURT: `물 원소 피해 보너스(%)`,
  FIGHT_PROP_GRASS_ADD_HURT: `풀 원소 피해 보너스(%)`,
  FIGHT_PROP_WIND_ADD_HURT: `바람 원소 피해 보너스(%)`,
  FIGHT_PROP_ROCK_ADD_HURT: `바위 원소 피해 보너스(%)`,
  FIGHT_PROP_ICE_ADD_HURT: `얼음 원소 피해 보너스(%)`,
  FIGHT_PROP_ATTACK_ADD_HURT: `피해 보너스(%)`,
  FIGHT_PROP_PHYSICAL_RES_MINUS: `물리 내성 감소(%)`,
  FIGHT_PROP_FIRE_RES_MINUS: `불 원소 내성 감소(%)`,
  FIGHT_PROP_WATER_RES_MINUS: `물 원소 내성 감소(%)`,
  FIGHT_PROP_ICE_RES_MINUS: `얼음 원소 내성 감소(%)`,
  FIGHT_PROP_ELEC_RES_MINUS: `번개 원소 내성 감소(%)`,
  FIGHT_PROP_GRASS_RES_MINUS: `풀 원소 내성 감소(%)`,
  FIGHT_PROP_WIND_RES_MINUS: `바람 원소 내성 감소(%)`,
  FIGHT_PROP_ROCK_RES_MINUS: `바위 원소 내성 감소(%)`,
  FIGHT_PROP_DEFENSE_MINUS: `방어력 감소(%)`,
  FIGHT_PROP_DEFENSE_IGNORE: `방어력 무시(%)`,
  FIGHT_PROP_HEAL_ADD: `치유 보너스(%)`,

  // 일반공격 관련
  FIGHT_PROP_NOMAL_ATTACK_CRITICAL: `일반 공격 치명타 확률(%)`,
  FIGHT_PROP_NOMAL_ATTACK_CRITICAL_HURT: `일반 공격 치명타 피해(%)`,
  FIGHT_PROP_NOMAL_ATTACK_FIRE_ADD_HURT: `일반 공격 불 원소 피해 보너스(%)`,
  FIGHT_PROP_NOMAL_ATTACK_ELEC_ADD_HURT: `일반 공격 번개 원소 피해 보너스(%)`,
  FIGHT_PROP_NOMAL_ATTACK_WATER_ADD_HURT: `일반 공격 물 원소 피해 보너스(%)`,
  FIGHT_PROP_NOMAL_ATTACK_GRASS_ADD_HURT: `일반 공격 풀 원소 피해 보너스(%)`,
  FIGHT_PROP_NOMAL_ATTACK_WIND_ADD_HURT: `일반 공격 바람 원소 피해 보너스(%)`,
  FIGHT_PROP_NOMAL_ATTACK_ROCK_ADD_HURT: `일반 공격 바위 원소 피해 보너스(%)`,
  FIGHT_PROP_NOMAL_ATTACK_ICE_ADD_HURT: `일반 공격 얼음 원소 피해 보너스(%)`,
  FIGHT_PROP_NOMAL_ATTACK_ATTACK_ADD_HURT: `일반 공격 물리 피해 보너스(%)`,

  // 강공격 관련
  FIGHT_PROP_CHARGED_ATTACK_CRITICAL: `강공격 치명타 확률(%)`,
  FIGHT_PROP_CHARGED_ATTACK_CRITICAL_HURT: `강공격 치명타 피해(%)`,
  FIGHT_PROP_CHARGED_ATTACK_FIRE_ADD_HURT: `강공격 불 원소 피해 보너스(%)`,
  FIGHT_PROP_CHARGED_ATTACK_ELEC_ADD_HURT: `강공격 번개 원소 피해 보너스(%)`,
  FIGHT_PROP_CHARGED_ATTACK_WATER_ADD_HURT: `강공격 물 원소 피해 보너스(%)`,
  FIGHT_PROP_CHARGED_ATTACK_GRASS_ADD_HURT: `강공격 풀 원소 피해 보너스(%)`,
  FIGHT_PROP_CHARGED_ATTACK_WIND_ADD_HURT: `강공격 바람 원소 피해 보너스(%)`,
  FIGHT_PROP_CHARGED_ATTACK_ROCK_ADD_HURT: `강공격 바위 원소 피해 보너스(%)`,
  FIGHT_PROP_CHARGED_ATTACK_ICE_ADD_HURT: `강공격 얼음 원소 피해 보너스(%)`,
  FIGHT_PROP_CHARGED_ATTACK_ATTACK_ADD_HURT: `강공격 물리 피해 보너스(%)`,

  // 낙하공격 관련
  FIGHT_PROP_FALLING_ATTACK_CRITICAL: `낙하 공격 치명타 확률(%)`,
  FIGHT_PROP_FALLING_ATTACK_CRITICAL_HURT: `낙하 공격 치명타 피해(%)`,
  FIGHT_PROP_FALLING_ATTACK_FIRE_ADD_HURT: `낙하 공격 불 원소 피해 보너스(%)`,
  FIGHT_PROP_FALLING_ATTACK_ELEC_ADD_HURT: `낙하 공격 번개 원소 피해 보너스(%)`,
  FIGHT_PROP_FALLING_ATTACK_WATER_ADD_HURT: `낙하 공격 물 원소 피해 보너스(%)`,
  FIGHT_PROP_FALLING_ATTACK_GRASS_ADD_HURT: `낙하 공격 풀 원소 피해 보너스(%)`,
  FIGHT_PROP_FALLING_ATTACK_WIND_ADD_HURT: `낙하 공격 바람 원소 피해 보너스(%)`,
  FIGHT_PROP_FALLING_ATTACK_ROCK_ADD_HURT: `낙하 공격 바위 원소 피해 보너스(%)`,
  FIGHT_PROP_FALLING_ATTACK_ICE_ADD_HURT: `낙하 공격 얼음 원소 피해 보너스(%)`,
  FIGHT_PROP_FALLING_ATTACK_ATTACK_ADD_HURT: `낙하 공격 물리 피해 보너스(%)`,

  // 원소 전투 스킬 관련
  FIGHT_PROP_ELEMENT_SKILL_CRITICAL: `원소 전투 스킬 치명타 확률(%)`,
  FIGHT_PROP_ELEMENT_SKILL_CRITICAL_HURT: `원소 전투 스킬 치명타 피해(%)`,
  FIGHT_PROP_ELEMENT_SKILL_FIRE_ADD_HURT: `원소 전투 스킬 불 원소 피해 보너스(%)`,
  FIGHT_PROP_ELEMENT_SKILL_ELEC_ADD_HURT: `원소 전투 스킬 번개 원소 피해 보너스(%)`,
  FIGHT_PROP_ELEMENT_SKILL_WATER_ADD_HURT: `원소 전투 스킬 물 원소 피해 보너스(%)`,
  FIGHT_PROP_ELEMENT_SKILL_GRASS_ADD_HURT: `원소 전투 스킬 풀 원소 피해 보너스(%)`,
  FIGHT_PROP_ELEMENT_SKILL_WIND_ADD_HURT: `원소 전투 스킬 바람 원소 피해 보너스(%)`,
  FIGHT_PROP_ELEMENT_SKILL_ROCK_ADD_HURT: `원소 전투 스킬 바위 원소 피해 보너스(%)`,
  FIGHT_PROP_ELEMENT_SKILL_ICE_ADD_HURT: `원소 전투 스킬 얼음 원소 피해 보너스(%)`,
  FIGHT_PROP_ELEMENT_SKILL_ATTACK_ADD_HURT: `원소 전투 스킬 물리 피해 보너스(%)`,

  // 원소 폭발 관련
  FIGHT_PROP_ELEMENT_BURST_CRITICAL: `원소 폭발 치명타 확률(%)`,
  FIGHT_PROP_ELEMENT_BURST_CRITICAL_HURT: `원소 폭발 치명타 피해(%)`,
  FIGHT_PROP_ELEMENT_BURST_FIRE_ADD_HURT: `원소 폭발 불 원소 피해 보너스(%)`,
  FIGHT_PROP_ELEMENT_BURST_ELEC_ADD_HURT: `원소 폭발 번개 원소 피해 보너스(%)`,
  FIGHT_PROP_ELEMENT_BURST_WATER_ADD_HURT: `원소 폭발 물 원소 피해 보너스(%)`,
  FIGHT_PROP_ELEMENT_BURST_GRASS_ADD_HURT: `원소 폭발 풀 원소 피해 보너스(%)`,
  FIGHT_PROP_ELEMENT_BURST_WIND_ADD_HURT: `원소 폭발 바람 원소 피해 보너스(%)`,
  FIGHT_PROP_ELEMENT_BURST_ROCK_ADD_HURT: `원소 폭발 바위 원소 피해 보너스(%)`,
  FIGHT_PROP_ELEMENT_BURST_ICE_ADD_HURT: `원소 폭발 얼음 원소 피해 보너스(%)`,
  FIGHT_PROP_ELEMENT_BURST_ATTACK_ADD_HURT: `원소 폭발 물리 피해 보너스(%)`,

  // 원소 반응 관련
  FIGHT_PROP_OVERLOADED_ADD_HURT: `과부하 피해 증가(%)`, // 과부하
  FIGHT_PROP_ELECTROCHARGED_ADD_HURT: `감전 피해 증가(%)`, // 감전
  FIGHT_PROP_SUPERCONDUCT_ADD_HURT: `초전도 피해 증가(%)`, // 초전도
  FIGHT_PROP_SHATTER_ADD_HURT: `쇄빙 피해 증가(%)`, // 쇄빙
  FIGHT_PROP_BLOOM_ADD_HURT: `만개 피해 증가(%)`, // 개화
  FIGHT_PROP_HYPERBLOOM_ADD_HURT: `만개 피해 증가(%)`, // 만개
  FIGHT_PROP_AGGRAVATE_ADD_HURT: `촉진 피해 증가(%)`, // 촉진
  FIGHT_PROP_SPREAD_ADD_HURT: `발산 피해 증가(%)`, // 발산
  FIGHT_PROP_VAPORIZE_ADD_HURT: `증발 피해 증가(%)`, // 증발
  FIGHT_PROP_MELT_ADD_HURT: `융해 피해 증가(%)`, // 융해
  FIGHT_PROP_BURNING_ADD_HURT: `연소 피해 증가(%)`, // 연소
  FIGHT_PROP_BURGEON_ADD_HURT: `발화 피해 증가(%)`, // 발화
  FIGHT_PROP_SWIRL_ADD_HURT: `확산 피해 증가(%)`, // 확산
  FIGHT_PROP_LUNARCHARGED_ADD_HURT: `달감전 피해 증가(%)`, // 달감전
};

export { fightPropLabels, fightPropsSchema };
