interface IcharactorPassiveStat {
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

const charactorConstellationStat: { [name: string]: { [key: string]: IcharactorPassiveStat[] } } = {
  감우: {},
  아야카: {},
  각청: {},
  나히다: {},
  '라이덴 쇼군': {},
  호두: {
    '진홍의 꽃다발': [], // 강공 스테미너 사용 제거
    '비처럼 내리는 불안': [], // 혈매향 데미지 계수 추가 증가
    '적색 피의 의식': [
      {
        type: 'FIGHT_PROP_ELEMENT_SKILL_ADD_LEVEL',
        rawValue: 3,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ], //
    '영원한 안식의 정원': [], // 호두 제외 치확 12퍼 추가 증가
    '꽃잎 향초의 기도': [
      {
        type: 'FIGHT_PROP_ELEMENT_BURST_ADD_LEVEL',
        rawValue: 3,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '나비 잔향': [
      {
        type: 'FIGHT_PROP_CRITICAL',
        rawValue: 1,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
  },
  야란: {
    '승부에 뛰어든 공모자': [], // 원소 전투 스킬 스텍형
    '올가미에 걸린 적': [], // 원소폭발 공격 추가 공격
    '노름꾼의 주사위': [
      {
        type: 'FIGHT_PROP_ELEMENT_BURST_ADD_LEVEL',
        rawValue: 3,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '이화접목의 현혹술': [
      {
        type: 'FIGHT_PROP_HP_PERCENT',
        rawValue: (stack: number) => stack * 0.1,
        maxOverlap: 4,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '눈보다 빠른 손': [
      {
        type: 'FIGHT_PROP_ELEMENT_SKILL_ADD_LEVEL',
        rawValue: 3,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '승자의 독식': [], // 일반 공격 강화. 일반공격을 타파의 화살로 전환하고, 해당 피해는 강공격 피해로 간주
  },
  푸리나: {
    '「사랑은 애걸해도 길들일 수 없는 새」': [], // 원소 폭발 열기 스텍 보정
    '「여자의 마음은 흔들리는 부평초」': [
      {
        type: 'FIGHT_PROP_HP_PERCENT',
        rawValue: (stack: number) => stack * 0.0035,
        maxOverlap: 400,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '「내 이름은 그 누구도 모르리라」': [
      {
        type: 'FIGHT_PROP_ELEMENT_BURST_ADD_LEVEL',
        rawValue: 3,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '「저승에서 느낀 삶의 소중함!」': [], // 소환물이 동작 시 원소 에너지 수급
    '「난 알았노라, 그대의 이름은…!」': [
      {
        type: 'FIGHT_PROP_ELEMENT_SKILL_ADD_LEVEL',
        rawValue: 3,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '「모두 사랑의 축배를 들렴!」': [
      {
        type: 'FIGHT_PROP_NORMAL_ATTACK_ADD_RATIO',
        rawValue: (hp: number) => hp * 0.43, // 기본 18% + 프뉴마(딜링) 상태 시 25퍼
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
      {
        type: 'FIGHT_PROP_CHARGED_ATTACK_ADD_RATIO',
        rawValue: (hp: number) => hp * 0.43,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
      {
        type: 'FIGHT_PROP_FALLING_ATTACK_ADD_RATIO',
        rawValue: (hp: number) => hp * 0.43,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
  },
  시틀라리: {
    '사백 개의 별빛': [], // 시틀라리 제외 파티원 신학 깃털 효과 부여
    '심장을 삼키는 자의 순행': [
      {
        // 본인 375 파티원 250
        type: 'FIGHT_PROP_ELEMENT_MASTERY',
        rawValue: 375,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
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
    '구름뱀의 깃털 왕관': [
      {
        type: 'FIGHT_PROP_ELEMENT_SKILL_ADD_LEVEL',
        rawValue: 3,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '죽음을 거부하는 자의 영혼 해골': [], // 원소 전투 스킬 사용 시 원마 기반 추가 피해
    '불길한 닷새의 주술': [
      {
        type: 'FIGHT_PROP_ELEMENT_BURST_ADD_LEVEL',
        rawValue: 3,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '아홉 번째 하늘의 계약': [
      {
        type: 'FIGHT_PROP_NORMAL_ADD_HURT',
        rawValue: (stack: number) => stack * 0.025,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
      {
        type: 'FIGHT_PROP_FIRE_ADD_HURT',
        rawValue: (stack: number) => stack * 0.015,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
      {
        type: 'FIGHT_PROP_WATER_ADD_HURT',
        rawValue: (stack: number) => stack * 0.015,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
  },
  느비예트: {
    '위대한 제정': [], // 경직저항
    '법의 계율': [
      {
        type: 'FIGHT_PROP_ELEMENT_SKILL_CRITICAL_HURT',
        rawValue: (stack: number) => stack * 0.14,
        maxOverlap: 3,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '고대의 의제': [
      {
        type: 'FIGHT_PROP_NORMAR_ATTACK_ADD_LEVEL',
        rawValue: 3,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '연민의 왕관': [], // 치유받을 시 원천의 방울 1개 생성
    '정의의 판결': [
      {
        type: 'FIGHT_PROP_ELEMENT_BURST_ADD_LEVEL',
        rawValue: 3,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '분노의 보상': [], // 강공 시 hp의 10% 계수로 추가 타격
  },
  마비카: {
    '밤 주인의 계시': [
      {
        type: 'FIGHT_PROP_ATTACK_PERCENT',
        rawValue: 0.4,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '잿더미의 대가': [
      {
        type: 'FIGHT_PROP_BASE_ATTACK',
        rawValue: 200,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
      {
        type: 'FIGHT_PROP_NORMAL_ATTACK_ADD_RATIO',
        rawValue: (att: number) => att * 0.6,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
      {
        type: 'FIGHT_PROP_CHARGED_ATTACK_ADD_RATIO',
        rawValue: (att: number) => att * 0.9,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
      {
        type: 'FIGHT_PROP_ELEMENT_BURST_ADD_RATIO',
        rawValue: (att: number) => att * 1.2,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '타오르는 태양': [
      {
        type: 'FIGHT_PROP_ELEMENT_BURST_ADD_LEVEL',
        rawValue: 3,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '「지도자」의 각오': [
      {
        type: 'FIGHT_PROP_NORMAL_ADD_HURT',
        rawValue: 0.1,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '진정한 의미': [
      {
        type: 'FIGHT_PROP_ELEMENT_SKILL_ADD_LEVEL',
        rawValue: 3,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
    '「인간의 이름」 해방': [
      {
        type: 'FIGHT_PROP_NORMAL_SUB_DEFENSE',
        rawValue: 0.2,
        maxOverlap: 1,
        overlapRatio: 1,
        conditionValueKey: '',
        improveOptionCheckKey: '',
      },
    ],
  },
};
