interface IcharacterPassiveStat {
  type: string;
  rawValue: number | [] | any;
  maxOverlap: number;
  overlapRatio: number;
  conditionValueKey: string;
  improveOptionCheckKey: string;
}

// FIGHT_PROP_NORMAL_ADD_HURT의 세분화 필요
// FIGHT_PROP_NORMAL_ADD_HURT : 일반 피증
// FIGHT_PROP_NORMAL_ATTACK_ADD_HURT
// FIGHT_PROP_CHARGED_ATTACK_ADD_HURT
// FIGHT_PROP_FALLING_ATTACK_ADD_HURT
// FIGHT_PROP_ELEMENT_SKILL_ADD_HURT
// FIGHT_PROP_ELEMENT_BURST_ADD_HURT

const characterPassiveStat: { [name: string]: { [key: string]: IcharacterPassiveStat[] } } = {
  감우: {
    '단 하나의 마음': [
      {
        type: 'FIGHT_PROP_CHARGED_ATTACK_CRITICAL',
        rawValue: 0.2,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    천지교태: [
      {
        type: 'FIGHT_PROP_ICE_ADD_HURT',
        rawValue: 0.3,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
  },
  아야카: {
    '천죄국죄 진사': [
      {
        type: 'FIGHT_PROP_NORMAL_ATTACK_ADD_HURT',
        rawValue: 0.3,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
      {
        type: 'FIGHT_PROP_CHARGED_ATTACK_ADD_HURT',
        rawValue: 0.3,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '한천선명 축사': [
      {
        type: 'FIGHT_PROP_ICE_ADD_HURT',
        rawValue: 0.18,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
  },
  각청: {
    '하늘에 닿은 뇌벌': [],
    '옥형의 품격': [
      {
        type: 'FIGHT_PROP_CRITICAL',
        rawValue: 0.15,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
      {
        type: 'FIGHT_PROP_CHARGE_EFFICIENCY',
        rawValue: 0.15,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
  },
  나히다: {
    '정선으로 포용한 명론': [
      {
        type: 'FIGHT_PROP_ELEMENT_MASTERY_PERCENT',
        rawValue: (elementMastery: number) => {
          const value = elementMastery * 0.25;
          return value > 250 ? 250 : value;
        },
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '지혜로 깨우친 지론': [
      {
        type: 'FIGHT_PROP_ELEMENT_SKILL_ADD_HURT',
        rawValue: (elementMastery: number) => {
          if (elementMastery > 200) {
            const value = (elementMastery - 200) * 0.001;
            return value > 0.8 ? 0.8 : value;
          } else return 0;
        },
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
      {
        type: 'FIGHT_PROP_ELEMENT_SKILL_CRITICAL',
        rawValue: (elementMastery: number) => {
          if (elementMastery > 200) {
            const value = (elementMastery - 200) * 0.0003;
            return value > 0.24 ? 0.24 : value;
          } else return 0;
        },
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
  },
  '라이덴 쇼군': {
    '수천수만의 염원': [],
    '비범한 옥체': [
      {
        type: 'FIGHT_PROP_ELEC_ADD_HURT',
        rawValue: (recharge: number) => {
          if (recharge > 1) return (recharge - 1) * 0.004;
          else return 0;
        },
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
  },
  호두: {
    '모습을 감춘 나비': [],
    '핏빛 분장': [
      {
        type: 'FIGHT_PROP_FIRE_ADD_HURT',
        rawValue: 0.33,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
  },
  야란: {
    '선공의 묘수': [
      {
        type: 'FIGHT_PROP_HP_PERCENT',
        rawValue: [0.06, 0.12, 0.18, 0.3],
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '마음 가는 대로': [
      {
        type: 'FIGHT_PROP_NORMAL_ADD_HURT',
        rawValue: (stack: number) => stack * 0.035 + 1,
        maxOverlap: 14,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
  },
  푸리나: {
    '끝없는 왈츠': [],
    '고독한 독백': [
      {
        type: 'FIGHT_PROP_ELEMENT_SKILL_ADD_HURT',
        rawValue: (hp: number) => {
          const value = Math.floor(hp / 1000) * 0.007;
          return value > 0.28 ? 0.28 : value;
        },
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
  },
  시틀라리: {
    '다섯 번째 하늘의 서리비': [
      {
        type: 'FIGHT_PROP_FIRE_SUB_REGISTANCE',
        rawValue: 0.2,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
      {
        type: 'FIGHT_PROP_WATER_SUB_REGISTANCE',
        rawValue: 0.2,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '하얀 불나비의 별옷': [
      {
        type: 'FIGHT_PROP_ELEMENT_SKILL_ADD_RATIO',
        rawValue: (elementMastery: number) => elementMastery * 0.9,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
      {
        type: 'FIGHT_PROP_ELEMENT_BURST_ADD_RATIO',
        rawValue: (elementMastery: number) => elementMastery * 12,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
  },
  느비예트: {
    '생존한 고대바다의 계승자': [
      {
        type: 'FIGHT_PROP_CHARGED_ATTACK_ADD_HURT',
        rawValue: (stack: number) => [0.1, 0.25, 0.6][stack],
        maxOverlap: 3,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '드높은 중재의 규율': [
      {
        type: 'FIGHT_PROP_WATER_ADD_HURT',
        rawValue: (stack: number) => stack * 0.006,
        maxOverlap: 50,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
  },
  마비카: {
    '타오르는 꽃의 선물': [
      {
        type: 'FIGHT_PROP_ATTACK_PERCENT',
        rawValue: 0.3,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    키온고지: [
      {
        type: 'FIGHT_PROP_NORMAL_ADD_HURT',
        rawValue: (stack: number) => stack * 0.002,
        maxOverlap: 200,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
  },
  // '향릉' : {},
};

export default characterPassiveStat;
