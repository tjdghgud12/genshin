from schemas.character import (
    characterDataSchema,
    passiveSkillSchema,
    activeSkillSchema,
    contellationSchema,
    skillBaseFightPropSchema,
    damageBaseFightPropSchema,
    skillConstellationOptionSchema,
    skillConstellationType,
    additionalAttackSchema,
)

info = {
    "나히다": characterDataSchema(
        passiveSkill={
            "정선으로 포용한 명론": passiveSkillSchema(
                description="원소 폭발 발동 시 원소마스터리 증가",
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="원소 폭발 발동")],
            ),
            "지혜로 깨우친 지론": passiveSkillSchema(
                description="원소 마스터리 200pt 초과 시 초과분 1pt 당 원소 전투 스킬의 삼업의 정화가 가하는 피해 및 치명타 확률 증가", unlockLevel=4
            ),
        },
        activeSkill={
            "마음에 비친 형상": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["grass"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["grass"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["grass"]),
                )
            ),
            "너른 헤아림": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    elementalSkill=damageBaseFightPropSchema(ATTACK=1, element=["grass"]),
                ),
                additionalAttack=[
                    additionalAttackSchema(name="삼업의 정화", type="elementalSkill", baseFightProp=damageBaseFightPropSchema(ATTACK=0.33, ELEMENT_MASTERY=0.67, element=["grass"]))
                ],
            ),
            "마음이 그리는 환상": activeSkillSchema(
                description="파티 내 불, 번개, 물 원소 타입 캐릭터가 있으면 각각 상응하는 효과가 발생",
                options=[
                    skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=2, label="불"),
                    skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=2, label="물"),
                    skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=2, label="번개"),
                ],
            ),
        },
        constellation=[
            contellationSchema(name="지혜를 머금은 씨앗", description="마야의 전당을 펼치고 파티 내 특정 원소 타입의 캐릭터 수량을 계산할 때 각 1명씩 추가로 집계"),
            contellationSchema(
                name="올곧은 선견의 뿌리",
                description="나히다 자신이 새긴 스칸다 씨앗 상태의 적은 다음과 같은 효과의 영향을 받는다. 연소, 개화, 만개, 발화 반응 피해가 치명타를 발동할 수 있다. 치명타 확률은 20%, 치명타 피해는 100%로 고정된다. 활성, 촉진, 발산 반응의 영향을 받은 후 8초 동안 방어력이 30% 감소한다.",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="스칸다 씨앗 상태")],
            ),
            contellationSchema(name="감화된 성취의 싹", description="원소 전투 스킬 레벨 +3"),
            contellationSchema(
                name="추론으로 드러난 줄기",
                description="스칸다 씨앗 상태에 있는 적 수당 나히다의 원소 마스터리 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=4, label="스칸다 씨앗 상태 적")],
            ),
            contellationSchema(name="깨달음을 주는 잎", description="원소 폭발 레벨 +3"),
            contellationSchema(
                name="달변으로 맺은 열매",
                description="원소 폭발 발동 후 일반공격 또는 강공격이 스칸다 씨앗 상태의 적 명중 시 삼업의 정화·업의 사면을 발동하고 나히다 공격력의 200%, 원소 마스터리의 400%에 기반해 풀 원소 피해",
                additionalAttack=[
                    additionalAttackSchema(
                        name="삼업의 정화·업의 사면", type="elementalSkill", baseFightProp=damageBaseFightPropSchema(ATTACK=2, ELEMENT_MASTERY=4, element=["grass"])
                    )
                ],
            ),
        ],
    ),
}
