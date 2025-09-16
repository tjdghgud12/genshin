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
    "아를레키노": characterDataSchema(
        passiveSkill={
            "고통만이 갚을 수 있고": passiveSkillSchema(
                description="핏값을 보유한 적 처치 시 생명의 계약 부여. 부여 후 5초 후 핏값·결산으로 승급. 핏값·결산 회수 시 생명의 계약 부여", unlockLevel=1, options=[]
            ),
            "힘만이 지킬 수 있으며": passiveSkillSchema(
                description="전투 상태에서 불 원소 피해 보너스 40% 획득하고, 떠오르는 재약의 달로만 HP를 회복할 수 있다.",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.always)],
            ),
        },
        activeSkill={
            "사형장으로의 초대": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["physical", "fire"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["physical", "fire"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["physical", "fire"]),
                ),
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=145, label="생명의 계약 백분율")],
            ),
            "재가 된 만상": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(elementalSkill=damageBaseFightPropSchema(ATTACK=1, element=["fire"])),
                additionalAttack=[additionalAttackSchema(name="핏값", type="elementalSkill", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["fire"]))],
            ),
            "떠오르는 재액의 달": activeSkillSchema(description="불 원소 범위 피해를 준 다음. 재가 된 만상의 재사용 대기시간을 초기화하고 자신의 HP를 회복한다."),
        },
        constellation=[
            contellationSchema(
                name="「모든 원한과 빚은 내가 갚고...」",
                description="붉은 죽음의 무도회의 증가량이 100% 더 증가한다. 또한 붉은 죽음의 무도회 상태에서 일반 공격 또는 강공격 시, 아를레키노의 경직 저항력이 증가한다",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always)],
            ),
            contellationSchema(
                name="「모든 상벌은 내가 내릴 것이다...」",
                description="핏값 부여 시 바로 핏값·결산이 된다. 핏값·결산 회수 시 전방에 핏빛 화염을 소환해 공격력의 900%에 해당하는 불 원소 범위 피해를 준다. 고유 특성 '고통만이 갚을 수 있고' 를 해금해야한다.",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
                additionalAttack=[additionalAttackSchema(name="핏빛 화염", type="fire", baseFightProp=damageBaseFightPropSchema(ATTACK=9, element=["fire"]))],
            ),
            contellationSchema(
                name="「우리의 새 가족이 되었으니...」",
                description="사형장으로의 초대(일반 공격) 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="「앞으로 사이좋게 지내거라...」",
                description="아를레키노가 핏값 회수 성공 시, 떠오르는 재액의 달의 재사용 대기시간이 2초 감소한다. 또한 아를레키노가 원소 에너지를 15pt 회복한다. 해당 효과는 10초마다 최대 1회 발동한다",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always)],
            ),
            contellationSchema(
                name="「고독한 우리는 망자와 다름없으나...」",
                description="원소 폭발 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="「앞으로 우리는 새 생명을 누리리라」",
                description="떠오르는 재액의 달이 주는 피해가 아를레키노 공격력에 현재 생명의 계약의 700%를 곱한 값만큼 증가한다.재가 된 만상 발동 후 20초 동안 아를레키노의 일반 공격과 원소폭발의 치명타 확률이 10%, 치명타 피해가 70% 증가한다.",
                options=[
                    skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=145, label="생명의 계약 백문율"),
                    skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label=""),
                ],
            ),
        ],
    ),
}
