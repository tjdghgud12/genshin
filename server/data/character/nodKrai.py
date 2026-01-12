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
    "라우마": characterDataSchema(
        passiveSkill={
            "서리밤에 바치는 빛": passiveSkillSchema(
                description=(
                    "라우마가 원소전투 스킬 성가 · 밤의 안식 발동 후 20초 동안, 파티의 달빛 징조에 따라 각기 다른 강화 효과가 생성된다. 레벨이 다른 달빛 징조가 제공하는 강화 효과는 중첩되지 않는다."
                    "달빛 징조·초승"
                    "주변에 있는 파티 내 모든 캐릭터가 발동한 개화, 만개, 발화 반응으로 주는 피해에서 치명타가 발생할 수 있다. 치명타 확률은 15%, 치명타 피해는 100%로 고정된다. 해당 효과가 제공하는 치명타 확률은, 원소 반응에 치명타 발생을 부여하는 동일 종류의 효과와 중첩될 수 있다."
                    "달빛 징조·보름"
                    "주변에 있는 파티 내 모든 캐릭터가 주는 달 개화 반응 피해의 치명타 확률이 10%, 치명타 피해가 20% 증가한다"
                ),
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.select, selectList=["초승", "보름"], label="달빛 징조")],
            ),
            "샘물에 바치는 정화": passiveSkillSchema(
                description=(
                    "라우마의 원소 마스터리 1pt당, 라우마가 아래 버프 효과를 획득한다:"
                    "· 원소전투 스킬로 주는 피해가 0.04% 증가한다. 해당 방식으로 최대 32% 증가한다."
                    "· 강공격 「영체화」의 재사용 대기시간이 0.02% 감소한다. 해당 방식으로 「영체화」의 재사용 대기시간이 최대 20% 감소한다"
                ),
                unlockLevel=4,
            ),
            "달빛 징조의 축복·자연의 은총": passiveSkillSchema(
                description=(
                    "파티 내 캐릭터가 개화 반응 발동 시, 달 개화 반응으로 전환되며, 라우마의 원소 마스터리에 기반해 파티 내 캐릭터가 주는 달 개화 반응의 기본 피해가 증가한다: "
                    "원소 마스터리 1pt마다 달 개화 반응의 기본 피해가 0.0175% 증가한다. 해당 방식으로 피해가 최대 14% 증가한다."
                ),
                unlockLevel=0,
            ),
        },
        activeSkill={
            "숲의 여정": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["grass"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["grass"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["grass"]),
                )
            ),
            "성가·밤의 안식": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(elementalSkill=damageBaseFightPropSchema(ATTACK=1, element=["grass"])),
                additionalAttack=[
                    additionalAttackSchema(name="2단 홀드(달개화)", type="lunarBloom", baseFightProp=damageBaseFightPropSchema(ELEMENT_MASTERY=1, element=["grass"])),
                    additionalAttackSchema(
                        name="서리숲 성역", type="elementalSkill", baseFightProp=damageBaseFightPropSchema(ATTACK=0.33, ELEMENT_MASTERY=0.67, element=["grass"])
                    ),
                ],
            ),
            "성가·달빛 소원": activeSkillSchema(
                description=(
                    "모든 생명의 염원이 대지를 비추는 달빛이 되길. 라우마가 극북의 성가를 읊으면 「푸른 찬송가」를 18스택 획득한다."
                    "주변에 있는 파티 내 캐릭터가 개화, 만개, 발화, 달 개화 반응 피해를 줄 때 「푸른 찬송가」를 1스택 소모해 주는 피해를 증가시킨다."
                ),
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="푸른 찬송가")],
            ),
        },
        constellation=[
            contellationSchema(
                name="「입술이여, 나를 위해 시와 노래로」",
                description=(
                    "라우마가 원소전투 스킬 성가 · 밤의 안식 또는 원소폭발 성가 · 달빛 소원 발동 후, 「생명으로 엮은 실」을 획득한다. 지속 시간: 20초."
                    "지속 시간 동안 주변에 있는 파티 내 캐릭터가 달 개화 반응 발동 시, 주변에 있는 현재 필드 위 캐릭터의 HP를 라우마 원소 마스터리의 500%만큼 회복한다. 해당 효과는 1.9초마다 최대 1회 발동된다."
                    "또한, 라우마의 영체 상태 시 소모되는 스태미나가 40% 감소하고, 최대 지속 시간이 5초 증가한다"
                ),
            ),
            contellationSchema(
                name="「극북의 충고와 전설을 엮어라」",
                description=(
                    "원소폭발 성가 · 달빛 소원이 강화된다:"
                    "·「푸른 찬송가」의 효과가 강화된다: 주변에 있는 파티 내 모든 캐릭터가 개화, 만개, 발화 반응 발동으로 주는 피해가 추가로 라우마의 원소 마스터리의 500%만큼 증가한다. "
                    "주변에 있는 파티 내 모든 캐릭터가 주는 달 개화 반응 피해가 추가로 라우마 원소 마스터리의 400%만큼 증가한다."
                    "달빛 징조·보름: 주변에 있는 파티 내 모든 캐릭터가 주는 달 개화 반응 피해가 40% 증가한다"
                ),
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="달빛 징조·보름")],
            ),
            contellationSchema(name="「그대여, 교활한 여우의 길을 탐하지 말라」", description="원소폭발 레벨 +3"),
            contellationSchema(
                name="「그대여, 거대한 곰의 권력을 탐하지 말라」",
                description="원소전투 스킬 성가 · 밤의 안식의 서리숲 성역 공격이 적에게 명중 시, 라우마가 원소 에너지를 4pt 회복한다. 해당 효과는 5초마다 최대 1회 발동된다",
            ),
            contellationSchema(name="「진실을 증명할 수만 있다면」", description="원소전투 스킬 레벨 +3"),
            contellationSchema(
                name="「내 피와 눈물을 달빛에 바치리라」",
                description=(
                    "「서리숲 영역」으로 적 공격 시, 달 개화 반응 피해로 간주하는 풀 원소 범위 피해를 추가로 1회 준다. 해당 피해는 라우마 원소 마스터리의 185%에 해당하며,"
                    "「푸른 찬송가」를 소모하지 않고, 라우마가 「푸른 찬송가」를 2스택 획득한다. 또한 해당 방식으로 획득한 「푸른 찬송가」의 지속 시간이 갱신된다."
                    "한 번의 서리숲 성역 지속 시간 동안 해당 효과는 최대 8회 발동된다. 원소전투 스킬 성가 · 밤의 안식 발동 시, 해당 방식으로 획득한 「푸른 찬송가」는 사라진다."
                    "또한, 라우마가 「푸른 찬송가」를 보유한 상태로 일반 공격 진행 시 「푸른 찬송가」를 1스택 소모해 라우마 원소 마스터리의 150%에 해당하는 풀 원소 피해를 준다. 해당 피해는 달 개화 반응으로 간주한다."
                    "달빛 징조 · 보름: 주변에 있는 파티 내 모든 캐릭터가 주는 달 개화 반응 피해가 25% 승격한다"
                ),
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="달빛 징조·보름")],
                additionalAttack=[
                    additionalAttackSchema(name="서리숲 성역 추가피해", type="lunarBloom", baseFightProp=damageBaseFightPropSchema(ELEMENT_MASTERY=1.85, element=["grass"])),
                    additionalAttackSchema(name="일반 공격 추가피해", type="lunarBloom", baseFightProp=damageBaseFightPropSchema(ELEMENT_MASTERY=1.5, element=["grass"])),
                ],
            ),
        ],
    ),
    # "네페르": characterDataSchema(
    #     passiveSkill={
    #         "노드 클라이": passiveSkillSchema(description="노드 클라이는 달 개화 피증을 40% 증가시킨다", unlockLevel=1),
    #     },
    #     activeSkill={
    #         "노드 클라이": activeSkillSchema(description="노드 클라이는 달 개화 피증을 40% 증가시킨다", unlockLevel=1),
    #     },
    # ),
}
