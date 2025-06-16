interface IweaponOptionStat {
  type: string;
  rawValue: number | [] | any;
  conditional: boolean;
  maxOverlap: number;
  overlapRatio: number;
  conditionValueKey: string;
  improveOptionCheckKey: string;
  conditionDescription: string;
}

// FIGHT_PROP_NORMAL_ADD_HURT의 세분화 필요
// FIGHT_PROP_NORMAL_ADD_HURT : 일반 피증
// FIGHT_PROP_NORMAL_ATTACK_ADD_HURT
// FIGHT_PROP_CHARGED_ATTACK_ADD_HURT
// FIGHT_PROP_FALLING_ATTACK_ADD_HURT
// FIGHT_PROP_ELEMENT_SKILL_ADD_HURT
// FIGHT_PROP_ELEMENT_BURST_ADD_HURT

const weaponOptionStat: { [key: string]: IweaponOptionStat[] } = {
  /*-------------------------------------------- 한손검 -------------------------------------------*/
  '안개를 가르는 회광': [
    {
      type: 'FIGHT_PROP_NORMAL_ADD_HURT',
      rawValue: [0.12, 0.15, 0.18, 0.21, 0.24],
      conditional: false,
      maxOverlap: 1,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '',
    },
    {
      type: 'FIGHT_PROP_NORMAL_ADD_HURT',
      rawValue: [
        [0.08, 0.16, 0.28],
        [0.1, 0.2, 0.32],
        [0.12, 0.24, 0.42],
        [0.14, 0.28, 0.49],
        [0.16, 0.32, 0.56],
      ],
      conditional: false,
      maxOverlap: 3,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '',
    },
  ],
  '고요히 샘솟는 빛': [
    {
      type: 'FIGHT_PROP_ELEMENT_SKILL_ADD_HURT',
      rawValue: [0.08, 0.1, 0.12, 0.14, 0.16],
      conditional: true,
      maxOverlap: 3,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '',
    },
    {
      type: 'FIGHT_PROP_HP_PERCENT',
      rawValue: [0.14, 0.175, 0.21, 0.245, 0.28],
      conditional: false,
      maxOverlap: 2,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '',
    },
  ],
  /*-------------------------------------------- 양손검 -------------------------------------------*/
  '타오르는 천 개의 태양': [
    {
      type: 'FIGHT_PROP_CRITICAL_HURT',
      rawValue: (nightsoul: boolean) => {
        const values = [0.2, 0.25, 0.3, 0.35, 0.4];
        return nightsoul ? values.map((v) => v * 1.75) : values;
      },
      conditional: true,
      maxOverlap: 1,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '성화 축복',
    },
    {
      type: 'FIGHT_PROP_ATTACK_PERCENT',
      rawValue: (nightsoul: boolean) => {
        const values = [0.28, 0.35, 0.42, 0.49, 0.56];
        return nightsoul ? values.map((v) => v * 1.75) : values;
      },
      conditional: true,
      maxOverlap: 1,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '성화 축복',
    },
  ],
  /*-------------------------------------------- 장병기 -------------------------------------------*/
  '호마의 지팡이': [
    {
      type: 'FIGHT_PROP_HP_PERCENT',
      rawValue: [0.2, 0.25, 0.3, 0.35, 0.4],
      conditional: false,
      maxOverlap: 1,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '',
    },
    {
      type: 'FIGHT_PROP_ATTACK',
      rawValue: (hp: number, halfHp: false) => {
        const ratio = [0.008, 0.01, 0.012, 0.014, 0.016];
        const addHalfHpPoint = [0.01, 0.012, 0.014, 0.018];
        return ratio.map((r, i) => (halfHp ? r + addHalfHpPoint[i] : r) * hp);
      },
      conditional: true,
      maxOverlap: 1,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: 'HP 50% 미만',
    },
  ],
  '예초의 번개': [
    {
      type: 'FIGHT_PROP_ATTACK_PERCENT',
      rawValue: (recharge: number) => {
        const values = [0.28, 0.35, 0.42, 0.49, 0.56];
        const max = [0.8, 0.9, 1, 1.1, 1.2];
        return values.map((v, i) => {
          const value = v * (recharge - 1);
          return max[i] > value ? max[i] : value;
        });
      },
      conditional: false,
      maxOverlap: 1,
      overlapRatio: 1,
      conditionValueKey: 'FIGHT_PROP_CHARGE_EFFICIENCY',
      improveOptionCheckKey: '',
      conditionDescription: '',
    },
    {
      type: 'FIGHT_PROP_CHARGE_EFFICIENCY',
      rawValue: [0.3, 0.35, 0.4, 0.45, 0.5],
      conditional: true,
      maxOverlap: 1,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '원소 충전 효율 증가',
    },
  ],
  '「어획」': [
    {
      type: 'FIGHT_PROP_NORMAL_ADD_HURT',
      rawValue: [0.16, 0.2, 0.24, 0.28, 0.32],
      conditional: false,
      maxOverlap: 1,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '',
    },
    {
      type: 'FIGHT_PROP_NORMAL_ADD_HURT',
      rawValue: [0.06, 0.075, 0.09, 0.105, 0.12],
      conditional: true,
      maxOverlap: 1,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '치명타 확률 증가',
    },
  ],
  /*-------------------------------------------- 법구 -------------------------------------------*/
  '떠오르는 천일 밤의 꿈': [
    {
      type: 'FIGHT_PROP_ELEMENT_MASTERY',
      rawValue: [32, 40, 48, 56, 64],
      conditional: false,
      maxOverlap: 3,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '',
    },
    {
      type: 'FIGHT_PROP_NORMAL_ADD_HURT',
      rawValue: [0.1, 0.14, 0.18, 0.22, 0.26],
      conditional: false,
      maxOverlap: 3,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '',
    },
  ],
  '영원히 샘솟는 법전': [
    {
      type: 'FIGHT_PROP_HP_PERCENT',
      rawValue: [0.16, 0.2, 0.24, 0.28, 0.32],
      conditional: false,
      maxOverlap: 1,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '',
    },
    {
      type: 'FIGHT_PROP_CHARGED_ATTACK_ADD_HURT',
      rawValue: [0.14, 0.18, 0.22, 0.26, 0.3],
      conditional: false,
      maxOverlap: 3,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '',
    },
  ],
  '별지기의 시선': [
    {
      type: 'FIGHT_PROP_ELEMENT_MASTERY',
      rawValue: [100, 125, 150, 175, 200],
      conditional: false,
      maxOverlap: 1,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '',
    },
    {
      type: 'FIGHT_PROP_NORMAL_ADD_HURT',
      rawValue: [0.28, 0.35, 0.42, 0.49, 0.56],
      conditional: true,
      maxOverlap: 1,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '',
    },
  ],
  /*-------------------------------------------- 활 -------------------------------------------*/
  '아모스의 활': [
    {
      type: 'FIGHT_PROP_NORMAL_ADD_HURT',
      rawValue: [0.12, 0.15, 0.18, 0.21, 0.24],
      conditional: true,
      maxOverlap: 1,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '',
    },
    {
      type: 'FIGHT_PROP_NORMAL_ADD_HURT',
      rawValue: [0.08, 0.1, 0.12, 0.14, 0.16],
      conditional: true,
      maxOverlap: 5,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '',
    },
  ],
  약수: [
    {
      type: 'FIGHT_PROP_HP_PERCENT',
      rawValue: [0.16, 0.2, 0.24, 0.28, 0.32],
      conditional: false,
      maxOverlap: 1,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '',
    },
    {
      type: 'FIGHT_PROP_NORMAL_ADD_HURT',
      rawValue: [0.2, 0.25, 0.3, 0.35, 0.4],
      conditional: false,
      maxOverlap: 1,
      overlapRatio: 1,
      conditionValueKey: '',
      improveOptionCheckKey: '',
      conditionDescription: '',
    },
  ],
};

export default weaponOptionStat;
