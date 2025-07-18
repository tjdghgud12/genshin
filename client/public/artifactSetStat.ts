interface IartifactSetStat {
  type: string;
  rawValue: number | [] | any;
  conditional: boolean;
  needCount: number;
  maxOverlap: number;
  overlapRatio: number;
  conditionValueKey: string;
}

// FIGHT_PROP_NORMAL_ADD_HURT의 세분화 필요
// FIGHT_PROP_NORMAL_ADD_HURT : 일반 피증
// FIGHT_PROP_NORMAL_ATTACK_ADD_HURT
// FIGHT_PROP_CHARGED_ATTACK_ADD_HURT
// FIGHT_PROP_FALLING_ATTACK_ADD_HURT
// FIGHT_PROP_ELEMENT_SKILL_ADD_HURT
// FIGHT_PROP_ELEMENT_BURST_ADD_HURT

const artifactSetStat: { [key: string]: IartifactSetStat[] } = {
  '얼음바람 속에서 길잃은 용사': [
    { type: 'FIGHT_PROP_ICE_ADD_HURT', rawValue: 0.15, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_CRITICAL', rawValue: 0.2, conditional: true, needCount: 4, maxOverlap: 2, overlapRatio: 1, conditionValueKey: '' },
  ],
  '뇌명을 평정한 존자': [
    { type: 'FIGHT_PROP_ELEC_SUB_HURT', rawValue: 0.4, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0.35, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
  ],
  '불 위를 걷는 현인': [
    { type: 'FIGHT_PROP_FIRE_SUB_HURT', rawValue: 0.4, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0.35, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
  ],
  '사랑받는 소녀': [
    { type: 'FIGHT_PROP_HEAL_ADD', rawValue: 0.15, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_HEALED_ADD', rawValue: 0.2, conditional: false, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
  ],
  '검투사의 피날레': [
    { type: '', rawValue: 0, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
  ],
  '청록색 그림자': [
    { type: 'FIGHT_PROP_WIND_ADD_HURT', rawValue: 0.15, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_DIFFUSION_ADD_HURT', rawValue: 0.6, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_NORMAL_SUB_REGISTANCE', rawValue: 0.4, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
  ],
  '대지를 유랑하는 악단': [
    { type: 'FIGHT_PROP_ELEMENT_MASTERY', rawValue: 80, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0.35, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
  ],
  '번개 같은 분노': [
    { type: 'FIGHT_PROP_ELEC_ADD_HURT', rawValue: 0, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_OVERLOADED_ADD_HURT', rawValue: 0.4, conditional: false, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_ELECTROCHARGED_ADD_HURT', rawValue: 0.4, conditional: false, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_SUPERCONDUCT_ADD_HURT', rawValue: 0.4, conditional: false, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_HYPERBLOOM_ADD_HURT', rawValue: 0.4, conditional: false, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_AGGRAVATE_ADD_HURT', rawValue: 0.2, conditional: false, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
  ],
  '불타오르는 화염의 마녀': [
    { type: 'FIGHT_PROP_FIRE_ADD_HURT', rawValue: 0.15, conditional: false, needCount: 2, maxOverlap: 3, overlapRatio: 0.5, conditionValueKey: '' },
    { type: 'FIGHT_PROP_OVERLOADED_ADD_HURT', rawValue: 0.4, conditional: false, needCount: 4, maxOverlap: 3, overlapRatio: 0.5, conditionValueKey: '' },
    { type: 'FIGHT_PROP_BURNING_ADD_HURT', rawValue: 0.4, conditional: false, needCount: 4, maxOverlap: 3, overlapRatio: 0.5, conditionValueKey: '' },
    { type: 'FIGHT_PROP_BURGEON_ADD_HURT', rawValue: 0.4, conditional: false, needCount: 4, maxOverlap: 3, overlapRatio: 0.5, conditionValueKey: '' },
    { type: 'FIGHT_PROP_VAPORIZE_ADD_HURT', rawValue: 0.15, conditional: false, needCount: 4, maxOverlap: 3, overlapRatio: 0.5, conditionValueKey: '' },
    { type: 'FIGHT_PROP_MELT_ADD_HURT', rawValue: 0.15, conditional: false, needCount: 4, maxOverlap: 3, overlapRatio: 0.5, conditionValueKey: '' },
  ],
  '옛 왕실의 의식': [
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0.2, conditional: true, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_ATTACK_PERCENT', rawValue: 0.2, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
  ],
  '피에 물든 기사도': [
    { type: 'FIGHT_PROP_PHYSICAL_ADD_HURT', rawValue: 0.25, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0.5, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
  ],
  '유구한 반암': [
    { type: 'FIGHT_PROP_ROCK_ADD_HURT', rawValue: 0.15, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0.35, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
  ],
  '날아오르는 유성': [
    { type: 'FIGHT_PROP_SHIELD_COST_MINUS_RATIO', rawValue: 0.35, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0.4, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
  ],
  '몰락한 마음': [
    { type: 'FIGHT_PROP_WATER_ADD_HURT', rawValue: 0.15, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0.3, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
  ],
  '견고한 천암': [
    { type: 'FIGHT_PROP_HP_PERCENT', rawValue: 0.2, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_ATTACK_PERCENT', rawValue: 0.2, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_SHIELD_COST_MINUS_RATIO', rawValue: 0.3, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
  ],
  '창백의 화염': [
    { type: 'FIGHT_PROP_PHYSICAL_ADD_HURT', rawValue: 0.25, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_ATTACK_PERCENT', rawValue: 0.09, conditional: true, needCount: 4, maxOverlap: 2, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_ATTACK_PERCENT', rawValue: 0.09, conditional: true, needCount: 4, maxOverlap: 2, overlapRatio: 1, conditionValueKey: '' },
  ],
  '추억의 시메나와': [
    { type: 'FIGHT_PROP_ATTACK_PERCENT', rawValue: 0.18, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0.5, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
  ],
  '절연의 기치': [
    { type: 'FIGHT_PROP_CHARGE_EFFICIENCY', rawValue: 0.2, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    {
      type: 'FIGHT_PROP_NORMAL_ADD_HURT',
      rawValue: (chargeEffi: number) => {
        const value = chargeEffi * 0.25;
        return value > 0.75 ? 0.75 : value;
      },
      conditional: true,
      needCount: 4,
      maxOverlap: 1,
      overlapRatio: 1,
      conditionValueKey: 'FIGHT_PROP_CHARGE_EFFICIENCY',
    },
  ],
  '풍요로운 꿈의 껍데기': [
    { type: 'FIGHT_PROP_DEFENSE_PERCENT', rawValue: 0, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_DEFENSE_PERCENT', rawValue: 0.06, conditional: true, needCount: 4, maxOverlap: 4, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_ROCK_ADD_HURT', rawValue: 0.06, conditional: true, needCount: 4, maxOverlap: 4, overlapRatio: 1, conditionValueKey: '' },
  ],
  '바다에 물든 거대 조개': [{ type: 'FIGHT_PROP_HEAL_ADD', rawValue: 0.15, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' }],
  '진사 왕생록': [
    { type: 'FIGHT_PROP_ATTACK_PERCENT', rawValue: 0.18, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_ATTACK_PERCENT', rawValue: 0.08, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_ATTACK_PERCENT', rawValue: 0.1, conditional: true, needCount: 4, maxOverlap: 4, overlapRatio: 1, conditionValueKey: '' },
  ],
  '제사의 여운': [
    { type: 'FIGHT_PROP_ATTACK_PERCENT', rawValue: 0.18, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_SKILL_ADD_RATIO', rawValue: (att: number) => att * 0.7, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: 'FIGHT_PROP_ATTACK' },
  ],
  '숲의 기억': [
    { type: 'FIGHT_PROP_GRASS_ADD_HURT', rawValue: 0.15, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_GRASS_SUB_REGISTANCE', rawValue: 0.3, conditional: false, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
  ],
  '도금된 꿈': [
    { type: 'FIGHT_PROP_ELEMENT_MASTERY', rawValue: 80, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_ELEMENT_MASTERY', rawValue: 50, conditional: true, needCount: 4, maxOverlap: 3, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_ATTACK_PERCENT', rawValue: 0.14, conditional: true, needCount: 4, maxOverlap: 3, overlapRatio: 1, conditionValueKey: '' },
  ],
  '모래 위 누각의 역사': [
    { type: 'FIGHT_PROP_WIND_ADD_HURT', rawValue: 0.15, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0.4, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
  ],
  '잃어버린 낙원의 꽃': [
    { type: 'FIGHT_PROP_ELEMENT_MASTERY', rawValue: 80, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_BLOOM_ADD_HURT', rawValue: 0.4, conditional: true, needCount: 4, maxOverlap: 4, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_HYPERBLOOM_ADD_HURT', rawValue: 0.4, conditional: true, needCount: 4, maxOverlap: 4, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_BURGEON_ADD_HURT', rawValue: 0.4, conditional: true, needCount: 4, maxOverlap: 4, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_BLOOM_ADD_HURT', rawValue: 0.1, conditional: true, needCount: 4, maxOverlap: 4, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_HYPERBLOOM_ADD_HURT', rawValue: 0.1, conditional: true, needCount: 4, maxOverlap: 4, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_BURGEON_ADD_HURT', rawValue: 0.1, conditional: true, needCount: 4, maxOverlap: 4, overlapRatio: 1, conditionValueKey: '' },
  ],
  '님프의 꿈': [
    { type: 'FIGHT_PROP_WATER_ADD_HURT', rawValue: 0.15, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_WATER_ADD_HURT', rawValue: [0.04, 0.09, 0.15], conditional: true, needCount: 4, maxOverlap: 3, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_ATTACK_PERCENT', rawValue: [0.07, 0.16, 0.25], conditional: true, needCount: 4, maxOverlap: 3, overlapRatio: 1, conditionValueKey: '' },
  ],
  '감로빛 꽃바다': [
    { type: 'FIGHT_PROP_HP_PERCENT', rawValue: 0.3, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0.1, conditional: true, needCount: 4, maxOverlap: 5, overlapRatio: 0.8, conditionValueKey: '' },
  ],
  '그림자 사냥꾼': [
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0.15, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_CRITICAL', rawValue: 0.12, conditional: true, needCount: 4, maxOverlap: 3, overlapRatio: 1, conditionValueKey: '' },
  ],
  '황금 극단': [
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0.2, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0.25, conditional: true, needCount: 4, maxOverlap: 2, overlapRatio: 1, conditionValueKey: '' },
  ],
  '지난날의 노래': [
    { type: 'FIGHT_PROP_HEAL_ADD', rawValue: 0, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    {
      type: 'FIGHT_PROP_SKILL_ADD_RATIO',
      rawValue: (heal: number) => (heal > 15000 ? 15000 : heal) * 0.08,
      conditional: true,
      needCount: 4,
      maxOverlap: 1,
      overlapRatio: 1,
      conditionValueKey: 'FIGHT_PROP_HEAL_RATIO',
    },
  ],
  '메아리숲의 야화': [
    { type: 'FIGHT_PROP_ATTACK_PERCENT', rawValue: 0.18, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_ROCK_ADD_HURT', rawValue: 0.2, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_ROCK_ADD_HURT', rawValue: 0.3, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
  ],
  '조화로운 공상의 단편': [
    { type: 'FIGHT_PROP_ATTACK_PERCENT', rawValue: 0.18, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0.18, conditional: true, needCount: 4, maxOverlap: 3, overlapRatio: 1, conditionValueKey: '' },
  ],
  '미완의 몽상': [
    { type: 'FIGHT_PROP_ATTACK_PERCENT', rawValue: 0.18, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0.1, conditional: true, needCount: 4, maxOverlap: 5, overlapRatio: 1, conditionValueKey: '' },
  ],
  '잿더미성 용사의 두루마리': [
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0.12, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0.28, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
  ],
  '흑요석 비전': [
    { type: 'FIGHT_PROP_NORMAL_ADD_HURT', rawValue: 0.15, conditional: false, needCount: 2, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
    { type: 'FIGHT_PROP_CRITICAL', rawValue: 0.4, conditional: true, needCount: 4, maxOverlap: 1, overlapRatio: 1, conditionValueKey: '' },
  ],
};

export default artifactSetStat;
