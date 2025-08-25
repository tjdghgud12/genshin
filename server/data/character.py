from enum import Enum
from pydantic import BaseModel
from typing import TypedDict, cast
from data.globalVariable import fightPropKeys
from models.character import passiveSkillType, activeSkillType, contellationType, skillConstellationOptionType, skillConstellationType


class CharacterFightPropSchema(TypedDict, total=True):
    # 공통
    FIGHT_PROP_BASE_HP: float
    FIGHT_PROP_HP: float
    FIGHT_PROP_HP_PERCENT: float
    FIGHT_PROP_BASE_ATTACK: float
    FIGHT_PROP_ATTACK: float
    FIGHT_PROP_ATTACK_PERCENT: float
    FIGHT_PROP_BASE_DEFENSE: float
    FIGHT_PROP_DEFENSE: float
    FIGHT_PROP_DEFENSE_PERCENT: float
    FIGHT_PROP_ELEMENT_MASTERY: float
    FIGHT_PROP_CHARGE_EFFICIENCY: float
    FIGHT_PROP_CRITICAL: float
    FIGHT_PROP_CRITICAL_HURT: float
    FIGHT_PROP_PHYSICAL_ADD_HURT: float
    FIGHT_PROP_FIRE_ADD_HURT: float
    FIGHT_PROP_ELEC_ADD_HURT: float
    FIGHT_PROP_WATER_ADD_HURT: float
    FIGHT_PROP_GRASS_ADD_HURT: float
    FIGHT_PROP_WIND_ADD_HURT: float
    FIGHT_PROP_ROCK_ADD_HURT: float
    FIGHT_PROP_ICE_ADD_HURT: float
    FIGHT_PROP_ATTACK_ADD_HURT: float
    FIGHT_PROP_PHYSICAL_RES_MINUS: float
    FIGHT_PROP_FIRE_RES_MINUS: float
    FIGHT_PROP_WATER_RES_MINUS: float
    FIGHT_PROP_ICE_RES_MINUS: float
    FIGHT_PROP_ELEC_RES_MINUS: float
    FIGHT_PROP_GRASS_RES_MINUS: float
    FIGHT_PROP_WIND_RES_MINUS: float
    FIGHT_PROP_ROCK_RES_MINUS: float
    FIGHT_PROP_DEFENSE_MINUS: float
    FIGHT_PROP_DEFENSE_IGNORE: float
    FIGHT_PROP_HEAL_ADD: float

    # 일반공격 관련
    FIGHT_PROP_NOMAL_ATTACK_CRITICAL: float
    FIGHT_PROP_NOMAL_ATTACK_CRITICAL_HURT: float
    FIGHT_PROP_NOMAL_ATTACK_FIRE_ADD_HURT: float
    FIGHT_PROP_NOMAL_ATTACK_ELEC_ADD_HURT: float
    FIGHT_PROP_NOMAL_ATTACK_WATER_ADD_HURT: float
    FIGHT_PROP_NOMAL_ATTACK_GRASS_ADD_HURT: float
    FIGHT_PROP_NOMAL_ATTACK_WIND_ADD_HURT: float
    FIGHT_PROP_NOMAL_ATTACK_ROCK_ADD_HURT: float
    FIGHT_PROP_NOMAL_ATTACK_ICE_ADD_HURT: float
    FIGHT_PROP_NOMAL_ATTACK_ATTACK_ADD_HURT: float

    # 강공격 관련
    FIGHT_PROP_CHARGED_ATTACK_CRITICAL: float
    FIGHT_PROP_CHARGED_ATTACK_CRITICAL_HURT: float
    FIGHT_PROP_CHARGED_ATTACK_FIRE_ADD_HURT: float
    FIGHT_PROP_CHARGED_ATTACK_ELEC_ADD_HURT: float
    FIGHT_PROP_CHARGED_ATTACK_WATER_ADD_HURT: float
    FIGHT_PROP_CHARGED_ATTACK_GRASS_ADD_HURT: float
    FIGHT_PROP_CHARGED_ATTACK_WIND_ADD_HURT: float
    FIGHT_PROP_CHARGED_ATTACK_ROCK_ADD_HURT: float
    FIGHT_PROP_CHARGED_ATTACK_ICE_ADD_HURT: float
    FIGHT_PROP_CHARGED_ATTACK_ATTACK_ADD_HURT: float

    # 낙하공격 관련
    FIGHT_PROP_FALLING_ATTACK_CRITICAL: float
    FIGHT_PROP_FALLING_ATTACK_CRITICAL_HURT: float
    FIGHT_PROP_FALLING_ATTACK_FIRE_ADD_HURT: float
    FIGHT_PROP_FALLING_ATTACK_ELEC_ADD_HURT: float
    FIGHT_PROP_FALLING_ATTACK_WATER_ADD_HURT: float
    FIGHT_PROP_FALLING_ATTACK_GRASS_ADD_HURT: float
    FIGHT_PROP_FALLING_ATTACK_WIND_ADD_HURT: float
    FIGHT_PROP_FALLING_ATTACK_ROCK_ADD_HURT: float
    FIGHT_PROP_FALLING_ATTACK_ICE_ADD_HURT: float
    FIGHT_PROP_FALLING_ATTACK_ATTACK_ADD_HURT: float

    # 원소 전투 스킬 관련
    FIGHT_PROP_ELEMENT_SKILL_CRITICAL: float
    FIGHT_PROP_ELEMENT_SKILL_CRITICAL_HURT: float
    FIGHT_PROP_ELEMENT_SKILL_FIRE_ADD_HURT: float
    FIGHT_PROP_ELEMENT_SKILL_ELEC_ADD_HURT: float
    FIGHT_PROP_ELEMENT_SKILL_WATER_ADD_HURT: float
    FIGHT_PROP_ELEMENT_SKILL_GRASS_ADD_HURT: float
    FIGHT_PROP_ELEMENT_SKILL_WIND_ADD_HURT: float
    FIGHT_PROP_ELEMENT_SKILL_ROCK_ADD_HURT: float
    FIGHT_PROP_ELEMENT_SKILL_ICE_ADD_HURT: float
    FIGHT_PROP_ELEMENT_SKILL_ATTACK_ADD_HURT: float

    # 원소 폭발 관련
    FIGHT_PROP_ELEMENT_BURST_CRITICAL: float
    FIGHT_PROP_ELEMENT_BURST_CRITICAL_HURT: float
    FIGHT_PROP_ELEMENT_BURST_FIRE_ADD_HURT: float
    FIGHT_PROP_ELEMENT_BURST_ELEC_ADD_HURT: float
    FIGHT_PROP_ELEMENT_BURST_WATER_ADD_HURT: float
    FIGHT_PROP_ELEMENT_BURST_GRASS_ADD_HURT: float
    FIGHT_PROP_ELEMENT_BURST_WIND_ADD_HURT: float
    FIGHT_PROP_ELEMENT_BURST_ROCK_ADD_HURT: float
    FIGHT_PROP_ELEMENT_BURST_ICE_ADD_HURT: float
    FIGHT_PROP_ELEMENT_BURST_ATTACK_ADD_HURT: float

    # 원소 반응 관련
    FIGHT_PROP_OVERLOADED_ADD_HURT: float  # 과부하
    FIGHT_PROP_ELECTRICSHOCK_ADD_HURT: float  # 감전
    FIGHT_PROP_SUPERCONDUCT_ADD_HURT: float  # 초전도
    FIGHT_PROP_HYPERBLOOM_ADD_HURT: float  # 만개
    FIGHT_PROP_AGGRAVATE_ADD_HURT: float  # 촉진
    FIGHT_PROP_EVAPORATION_ADD_HURT: float  # 증발
    FIGHT_PROP_MELT_ADD_HURT: float  # 융해
    FIGHT_PROP_COMBUSTION_ADD_HURT: float  # 연소
    FIGHT_PROP_IGNITION_ADD_HURT: float  # 발화


ambrCharacterCurve: dict[str, dict] = {}

characterStats = cast(
    CharacterFightPropSchema,
    {
        key: (0.05 if key == fightPropKeys.CRITICAL.value else 0.5 if key == fightPropKeys.CRITICAL_HURT.value else 1.0 if key == fightPropKeys.CHARGE_EFFICIENCY.value else 0.0)
        for key in list(CharacterFightPropSchema.__annotations__.keys())
    },
)

fightPropTemplate: CharacterFightPropSchema = cast(CharacterFightPropSchema, {key: 0.0 for key in CharacterFightPropSchema.__annotations__.keys()})


passiveSkill = {
    "감우": {
        "단 하나의 마음": passiveSkillType(
            description="강공격 후 강공격 치명타 확률 증가", unlockLevel=1, options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")]
        ),
        "천지교태": passiveSkillType(
            description="원소 폭발 내부에 존재 시 얼음 원소 피해 증가",
            unlockLevel=4,
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
    },
    "카미사토 아야카": {
        "천죄국죄 진사": passiveSkillType(
            description="원소 전투 스킬 발동 후 일반공격 및 강공격 피해 증가",
            unlockLevel=1,
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
        "한천선명 축사": passiveSkillType(
            description="싸락눈 걸음 명중 후 얼음 원소 피해 증가", unlockLevel=4, options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")]
        ),
    },
    "각청": {
        "하늘에 닿은 뇌벌": passiveSkillType(
            description="원소 전투 스킬 발동 후 번개 원소 인챈트", unlockLevel=1, options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")]
        ),
        "옥형의 품격": passiveSkillType(
            description="원소 폭발 발동 후 치명타 확률 및 원소 충전 효율 증가",
            unlockLevel=4,
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
    },
    "나히다": {
        "정선으로 포용한 명론": passiveSkillType(
            description="원소 폭발 발동 시 원소마스터리 증가", unlockLevel=1, options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")]
        ),
        "지혜로 깨우친 지론": passiveSkillType(
            description="원소 마스터리 200pt 초과 시 초과분 1pt 당 원소 전투 스킬의 삼업의 정화가 가하는 피해 및 치명타 확률 증가",
            unlockLevel=4,
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
    },
    "라이덴 쇼군": {
        "수천수만의 염원": passiveSkillType(
            description="원소 입자 획득 시 원력 스텍 추가", unlockLevel=1, options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")]
        ),
        "비범한 옥체": passiveSkillType(
            description="원소 충전 효율이 100%초과 시 초과 분 1% 당 번개 원소 피해 증가",
            unlockLevel=4,
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
    },
    "호두": {
        "모습을 감춘 나비": passiveSkillType(
            description="피안접무 상태가 끝난 후 호두를 제외한 파티 내 모든 캐릭터의 치명타 확률 증가",
            unlockLevel=1,
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        "핏빛 분장": passiveSkillType(
            description="현재 hp가 50% 이하일 때 불 원소 피해 증가", unlockLevel=4, options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")]
        ),
    },
    "야란": {
        "선공의 묘수": passiveSkillType(
            description="파티 내 캐릭터의 원소 타입 종류 마다 야란의 최대 hp 증가",
            unlockLevel=1,
            options=[skillConstellationOptionType(type=skillConstellationType.stack, maxStack=4, label="원소 타입 종류 수")],
        ),
        "마음 가는 대로": passiveSkillType(
            description="원소 폭발 발동 시 필드 위 캐릭터가 가하는 피해가 1초마다 증가",
            unlockLevel=4,
            options=[skillConstellationOptionType(type=skillConstellationType.stack, maxStack=14, label="경과 시간(초)")],
        ),
    },
    "푸리나": {
        "끝없는 왈츠": passiveSkillType(
            description="필드 위 캐릭터가 치유 받을 시 푸리나의 치유가 아닌 동시에 회복량이 초과된 경우 주변 파티 내 캐릭터 hp 회복",
            unlockLevel=1,
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        "고독한 독백": passiveSkillType(
            description="푸리나의 최대 hp 1000pt 당 원소 전투 스킬 피해 증가",
            unlockLevel=4,
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
    },
    "시틀라리": {
        "다섯 번째 하늘의 서리비": passiveSkillType(
            description="융해 반응 발동 시 반응에 영향을 받은 적의 물 원소 및 불 원소 내성 감소",
            unlockLevel=1,
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
        "하얀 불나비의 별옷": passiveSkillType(
            description="원소 마스터리의 일정 비율 만큼 원소 전투 스킬 및 원소 폭발 피해 계수 추가",
            unlockLevel=4,
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
    },
    "느비예트": {
        "생존한 고대바다의 계승자": passiveSkillType(
            description="물 원소 관련 반응 발동 시 강공격 피해 증가",
            unlockLevel=1,
            options=[skillConstellationOptionType(type=skillConstellationType.stack, maxStack=3, label="생존한 용의 영광")],
        ),
        "드높은 중재의 규율": passiveSkillType(
            description="현재 hp 중 hp 최대치의 30%를 초과하는 부분을 기반으로 1% 당 물 원소 피해 증가",
            unlockLevel=4,
            options=[skillConstellationOptionType(type=skillConstellationType.stack, maxStack=50, label="hp 최대치 초과분(%)")],
        ),
    },
    "마비카": {
        "타오르는 꽃의 선물": passiveSkillType(
            description="파티 내 캐릭터가 밤혼 발산 발동 시 마비카의 공격력 증가",
            unlockLevel=1,
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
        "「키온고지」": passiveSkillType(
            description="원소 폭발 발동 후 발동 당시 전의 스텍 1pt당 피해 증가 및 지속 시간 동안 점차 감소",
            unlockLevel=4,
            options=[skillConstellationOptionType(type=skillConstellationType.stack, maxStack=200, label="전의")],
        ),
    },
    "에스코피에": {
        "밥이 보약": passiveSkillType(
            description="원소 폭발 발동 후 파티 내 모든 캐릭터 hp 회복",
            unlockLevel=1,
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
        "영감의 조미료": passiveSkillType(
            description="원소 전투 스킬 또는 원소 폭발 명중 시 파티 내 물 원소 캐릭터 또는 얼음 원소 캐릭터 수 마다 명중한 적 물 원소 내성 및 얼음 원소 내성 감소",
            unlockLevel=4,
            options=[skillConstellationOptionType(type=skillConstellationType.stack, maxStack=4, label="물 또는 얼음 원소 파티원 수")],
        ),
    },
    "스커크": {
        "이치 너머의 이치": passiveSkillType(
            description="빙결, 초전도, 얼음 확산, 얼음 결정 반응 발동 시 허계 균열 1개 생성. 허계 균열은 흡수 가능하며 흡수 시 원소 전투 스킬 및 원소 폭발 계수 증가",
            unlockLevel=1,
            options=[skillConstellationOptionType(type=skillConstellationType.stack, maxStack=3, label="흡수 허계 균열 수")],
        ),
        "흐름의 적멸": passiveSkillType(
            description="파티 내 주변에 있는 물 원소 또는 얼음 원소 캐릭터가 각각 물 원소 또는 얼음 원소 공격으로 적 명중 시 최종 데미지 증가(마지막 곱연산)",
            unlockLevel=4,
            options=[skillConstellationOptionType(type=skillConstellationType.stack, maxStack=3, label="죽음의 강")],
        ),
    },
}

activeSkill = {
    "감우": {},
    "카미사토 아야카": {},
    "각청": {},
    "나히다": {
        "마음이 그리는 환상": activeSkillType(
            description="파티 내 불, 번개, 물 원소 타입 캐릭터가 있으면 각각 상응하는 효과가 발생",
            options=[
                skillConstellationOptionType(type=skillConstellationType.stack, maxStack=2, label="불"),
                skillConstellationOptionType(type=skillConstellationType.stack, maxStack=2, label="물"),
                skillConstellationOptionType(type=skillConstellationType.stack, maxStack=2, label="번개"),
            ],
        )
    },
    "라이덴 쇼군": {
        "초월·악요개안": activeSkillType(
            description="원소 폭발의 원소 에너지 당 원소 폭발 피해 증가", options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")]
        )
    },
    "호두": {
        "나비의 서": activeSkillType(
            description="현재 hp의 30%를 소비하여 hp 최대치 기반 공격력 증가", options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")]
        )
    },
    "야란": {},
    "푸리나": {
        "성대한 카니발": activeSkillType(
            description="무대 열기 당 피해 증가 및 치유 보너스 증가", options=[skillConstellationOptionType(type=skillConstellationType.stack, maxStack=300, label="무대 열기")]
        )
    },
    "시틀라리": {},
    "느비예트": {},
    "마비카": {},
    "에스코피에": {},
    "스커크": {
        "극악기·멸": activeSkillType(
            description="일곱빛 섬광 모드에서 발동 가능. 주변 일정 범위 내의 허계 균열을 흡수하며, 흡수한 허계 균열 개수 당 일반 공격 피해 증가",
            options=[
                skillConstellationOptionType(
                    type=skillConstellationType.stack,
                    maxStack=3,
                    label="허계 균열 흡수",
                )
            ],
        )
    },
}

# 운명의자리
constellation = {
    "감우": [
        contellationType(
            name="이슬 먹는 신수",
            description="2단 차지 강공격 또는 서리꽃에 명중된 적의 얼음 원소 내성 감소 15%",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
        contellationType(
            name="획린(獲麟)",
            description="원소 전투 스킬 사용 가능 횟수 1회 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="구름 여행",
            description="원고 폭발 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="서수(西狩)",
            description="원소 폭발 영역 내에서 적이 받는 피해 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.stack, maxStack=5, label="피해 증가 중첩")],
        ),
        contellationType(
            name="잡초 근절",
            description="원소 전투 스킬 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="살생의 발걸음",
            description="원소 전투 스킬 발동 시 첫 번째 서리꽃 화살은 차징 없이 발동",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
    ],
    "카미사토 아야카": [
        contellationType(
            name="서리에 검게 물든 벚꽃",
            description="일반 공격 또는 강공격으로 얼음 원소 피해를 주면, 50% 확률로 원소 전투 스킬의 재사용 대기시간이 0.3초 감소",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="삼중 서리 관문",
            description="원소 폭발 발동 시 기존 공격력의 20%의 피해를 주는 소형 서리 관문 2개 추가",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="흩날리는 카미후부키",
            description="원소 폭발 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="영고성쇠",
            description="원소 폭발의 피해를 받은 적의 방어력 30% 감소",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
        contellationType(
            name="화운종월경",
            description="원소 전투 스킬 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="물에 비친 달",
            description="10초마다 강공격 피해를 0.5초간 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
    ],
    "각청": [
        contellationType(
            name="계뢰",
            description="뇌설이 존재하는 동안 다시 원소 전투 스킬 발동 시 공격력의 50%의 번개 원소 피해 추가",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="가연",
            description="일반 공격 또는 강공격이 번개 원소 영향을 받은 적 공격 시 50% 확률로 원소 입자 생성",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="등루",
            description="원소 폭발 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="조율",
            description="각청이 번개 원소 관련 반응 발동 뒤 10초간 공격력 25% 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
        contellationType(
            name="이등",
            description="원소 전투 스킬 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="염정",
            description="일반 공격, 강공격, 원소 전투 스킬 혹은 원소폭발 사용 시, 각청은 번개 원소 피해 보너스를 6% 획득",
            options=[skillConstellationOptionType(type=skillConstellationType.stack, maxStack=3, label="번개 원소 피해 보너스")],
        ),
    ],
    "나히다": [
        contellationType(
            name="지혜를 머금은 씨앗",
            description="마야의 전당을 펼치고 파티 내 특정 원소 타입의 캐릭터 수량을 계산할 때 각 1명씩 추가로 집계",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="올곧은 선견의 뿌리",
            description="나히다 자신이 새긴 스칸다 씨앗 상태의 적은 다음과 같은 효과의 영향을 받는다. 연소, 개화, 만개, 발화 반응 피해가 치명타를 발동할 수 있다. 치명타 확률은 20%, 치명타 피해는 100%로 고정된다. 활성, 촉진, 발산 반응의 영향을 받은 후 8초 동안 방어력이 30% 감소한다.",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
        contellationType(
            name="감화된 성취의 싹",
            description="원소 전투 스킬 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="추론으로 드러난 줄기",
            description="스칸다 씨앗 상태에 있는 적 수당 나히다의 원소 마스터리 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.stack, maxStack=4, label="스칸다 씨앗 상태 적 수")],
        ),
        contellationType(
            name="깨달음을 주는 잎",
            description="원소 폭발 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="달변으로 맺은 열매",
            description="원소 폭발 발동 후 일반공격 또는 강공격이 스칸다 씨앗 상태의 적 명중 시 삼업의 정화 · 업의 사면을 발동하고 나히다 공격력의 200%, 원소 마스터리의 400%에 기반해 풀 원소 피해",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
    ],
    "라이덴 쇼군": [
        contellationType(
            name="악요 명문(銘文)",
            description="염원이 깃든 백안지륜이 더욱 빠르게 원력을 축적",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="강철 절단",
            description="원소 폭발 상태 시 적의 방여력 60%를 무시한다",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
        contellationType(
            name="진영의 과거",
            description="원소 폭발 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="진리의 맹세",
            description="원소 폭발 종료 후 라이덴 쇼군을 제외한 파티원의 공력력 30% 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
        contellationType(
            name="쇼군의 현형",
            description="원소 전투 스킬 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="염원의 대행인",
            description="원소 폭발 상태에서 적 명중 시 라이덴 쇼군을 제외한 파티원의 원소 폭발 재사용 대기시간 감소",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
    ],
    "호두": [
        contellationType(
            name="진홍의 꽃다발",
            description="피안접무 상태일 때 강공격에 스테미너를 사용하지 않는다",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="비처럼 내리는 불안",
            description="혈매향의 피해가 hp최대치의 10%만큼 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="적색 피의 의식",
            description="원소 전투 스킬 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="영원한 안식의 정원",
            description="혈매향 상태 적 처치 시, 호두를 제외한 파티내 캐릭터의 치명타 확률 12% 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
        contellationType(
            name="꽃잎 향초의 기도",
            description="원소 폭발 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="나비 잔향",
            description="hp가 25%이하로 떨어지거나 전투 불능이 될 정도의 피해를 입으면 치명타 확률 100%, 모든 내성 200%, 경직 저항력이 대폭 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
    ],
    "야란": [
        contellationType(
            name="승부에 뛰어든 공모자",
            description="원소 전투 스킬 사용 가능 횟수 +1",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="올가미에 걸린 적",
            description="원소 폭발의 협동 공격 시 야란 hp 최대치의 14%의 추가 데미지. 쿨타임 1.8초",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="노름꾼의 주사위",
            description="원소 폭발 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="이화접목의 현혹술",
            description="원소 전투 스킬에 명중한 적 당 hp최대치 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.stack, maxStack=4, label="명중 적 수")],
        ),
        contellationType(
            name="눈보다 빠른 손",
            description="원소 전투 스킬 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="승자의 독식",
            description="원소 폭발 발동 시 일반공격 피해 증가 및 일반공격을 강공격으로 취급",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
    ],
    "푸리나": [
        contellationType(
            name="「사랑은 애걸해도 길들일 수 없는 새」",
            description="원소 폭발 발동 시 무대 열기 +150pt 및 무대 열기 최대치 +100pt",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="「여자의 마음은 흔들리는 부평초」",
            description="원소 폭발 발동 시 지속 시간 동인 무대 열기 당 hp최대치 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="「내 이름은 그 누구도 모르리라」",
            description="원소 폭발 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="「저승에서 느낀 삶의 소중함!」",
            description="원소 전투 스킬이 적 명중 또는 파티원 회복 시 원소 에너지 획득",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="「난 알았노라, 그대의 이름은…!」",
            description="원소 전투 스킬 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="「모두 사랑의 축배를 들렴!」",
            description="원소 전투 스킬 발동 시 일반공격, 강공격, 낙하공격이 hp최대치의 18%만큼 증가하는 물 원소 피해로 변경. 프뉴마 상태일 때 일반공격, 강공격, 낙하공격의 추락충격으로 주는 피해가 hp최대치의 25%만큼 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
    ],
    "시틀라리": [
        contellationType(
            name="사백 개의 별빛",
            description="파티 내 캐릭터가 공격 시 소모되는 별빛 검 스텍을 10개 획득. 별빛 검은 시틀라리의 원소 마스터리의 200%만큼 피해 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
        contellationType(
            name="심장을 삼키는 자의 순행",
            description="원소 전투 스킬 사용 시 원소 마스터리 증가 및 다섯 번째 하늘의 서리비 강화(물, 불 원소 내성 감소 각각 20% 추가 감소)",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
        contellationType(
            name="구름뱀의 깃털 왕관",
            description="원소 전투 스킬 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="죽음을 거부하는 자의 영혼 해골",
            description="서리 운석 폭풍 명중 시 시틀라리의 원소 마스터리의 1800%만큼의 추가 피해. 재사용 대기시간 8초",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
        contellationType(
            name="불길한 닷새의 저주",
            description="원소 폭발 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="아홉 번째 하늘의 계약",
            description="원소 전투 스킬이 밤혼이 없어도 유지 또한 원소 전투 스킬 발동 시 모든 밤혼 소모하며 이후 소모되는 밤혼 당 신비의 수 스텍 1pt 적립. 신비의 수 스텍 당 파티원 불 원소, 물 원소 피해 증가 + 시틀라리의 피해 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.stack, maxStack=40, label="밤혼 소모")],
        ),
    ],
    "마비카": [
        contellationType(
            name="밤 주인의 계시",
            description="전의 획득 후 공력력 40% 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
        contellationType(
            name="잿더미의 대가",
            description="기초 공격력 200pt 증가. 일반공격, 강공격, 원소폭발의 석양 베기로 주는 피해 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="타오르는 태양",
            description="원소 폭발 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="「지도자」의 각오",
            description="키온고지 효과 강화",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="진정한 의미",
            description="원소 전투 스킬 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="「인간의 이름」 해방",
            description="불볕 고리: 공격 적중 시 공격력의 200%에 해당하는 밤혼 성질의 불 원소 피해 추가. 바이크 : 주변 적 방어력 20% 감소 및 3초마다 공격력의 500%에 해당하는 밤혼 성질의 불 원소 피해 추가",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
    ],
    "느비예트": [
        contellationType(
            name="위대한 제정",
            description="생존한 용의 영광을 1 스택 획득 및 강공격 시 경직 저항력 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="법의 계율",
            description="생존한 용의 영광 1스텍 당 강공격 치명타 피해 14% 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="고대의 의제",
            description="일반공격 스킬 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="연민의 왕관",
            description="치유 받을 시 원천의 방울 1개 생성",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="정의의 판결",
            description="원소 폭발 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="분노의 보상",
            description="강공격 명중 시 hp최대치의 10% 물 원소 피해를 주는 격류 2개 소환",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
    ],
    "에스코피에": [
        contellationType(
            name="미각을 깨우는 식전 공연",
            description="파티 내 캐릭터의 원소 타입이 모두 물 또는 얼음인 경우, 원소 전투 스킬 또는 원소 폭발 발동 후 얼음 원소 피해를 줄 시 치명타 피해 60% 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
        contellationType(
            name="예술의 경지에 이른 스튜",
            description="원소 전투 스킬 발동 시 피해를 에스코피에의 공격력의 240%만큼 증가시키는 즉석 요리 스텍 획득",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
        contellationType(
            name="캐러멜화의 마법",
            description="원소 전투 스킬 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="로즈마리 비밀 레시피",
            description="식이 요법 지속시간 증가 및 식이 요법으로 치유 시 원소 에너지 획득",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="다채로운 소스의 교향곡",
            description="원소 폭발 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="무지갯빛 티타임",
            description="현재 필드 위에 있는 파티 내 자신의 캐릭터의 일반공격, 강공격, 낙하공격이 명중 시 에스코피에의 공격력의 500%에 해당하는 얼음 원소 추가 피해",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
    ],
    "스커크": [
        contellationType(
            name="요원",
            description="허계 균열 1개 흡수할 때 마다 스커크 공격력의 500%에 해당하는 얼음 원소 피해 추가",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="심연",
            description="원소 전투 스킬 발동 시 뱀의 계략 10pt 획득. 원소 폭발 사용 시 뱀의 계략 최대치 10pt 증가. 극악기 · 진 발동 후 공격력 70% 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.toggle, maxStack=1, label="")],
        ),
        contellationType(
            name="악연",
            description="원소 폭발 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="멸류",
            description="죽음의 강 효과 스텍마다 공격력 증가",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="소망",
            description="원소 전투 스킬 레벨 +3",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
        contellationType(
            name="근원",
            description="흡수한 허계 균열 수 당 극악기 · 참 스택 획득. 극악기 · 참 스택 마다 원소 폭발 발동 시 공격력의 750%에 해당하는 얼음 원소 피해 추가. 일곱빛 섬광 모드에서는 일반공격 또는 피격 시 협동 공격",
            options=[skillConstellationOptionType(type=skillConstellationType.always, maxStack=1, label="")],
        ),
    ],
}
