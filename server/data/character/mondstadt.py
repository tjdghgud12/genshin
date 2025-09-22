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
    "유라": characterDataSchema(
        passiveSkill={
            "소용돌이치는 서리": passiveSkillSchema(
                description="홀드하여 얼음 파도의 와류 발동 시 한번에 냉혹한 마음 효과를 2스택 소모하면, 즉시 폭발하는 부서진 빛의 검이 생성된다. 이는 파도를 얼리는 광검으로 생성된 빛의 검 기초 피해 50%에 해당하는 물리 피해를 준다.",
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            "솟구치는 전투의 욕망": passiveSkillSchema(
                description="파도를 얼리는 광검 발동 시, 얼음 파도의 와류의 재발동 대기시간이 초기화되고 유라에게 냉혹한 마음 효과를 1스택 부여한다.",
                unlockLevel=4,
                options=[],
            ),
        },
        activeSkill={
            "페보니우스 검술·왕실": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                )
            ),
            "얼음 파도의 와류": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(elementalSkill=damageBaseFightPropSchema(ATTACK=1, element=["ice"])),
                options=[
                    skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=2, label="냉혹한 마음"),
                    skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="냉혹한 마음 소모"),
                ],
                additionalAttack=[additionalAttackSchema(name="얼음 소용돌이의 검", type="ice", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["ice"]))],
            ),
            "파도를 얼리는 광검": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(ATTACK=1, element=["ice"])),
                additionalAttack=[additionalAttackSchema(name="빛의 검", type="elementalBurst", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["physical"]))],
            ),
        },
        constellation=[
            contellationSchema(
                name="빛의 환상",
                description="얼음 파도의 와류의 냉혹한 마음 효과를 소모하면, 유라의 물리 피해 보너스가 30% 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            contellationSchema(
                name="물보라 소녀",
                description="얼음 파도의 와류 차지 재사용 대기시간이 짧은 터치 재사용 대기시간과 같아질 만큼 감소한다.",
                options=[],  # 한번 완전히 없애보자.
            ),
            contellationSchema(
                name="로렌스의 혈통",
                description="원소 폭발 레벨 +3",
                options=[],
            ),
            contellationSchema(
                name="열등감 속 고집",
                description="HP가 50% 미만인 적에게 빛의 검이 가하는 피해가 25% 증가한다.",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            contellationSchema(
                name="기사의 소양",
                description="원소 전투 스킬 레벨 +3",
                options=[],
            ),
            contellationSchema(
                name="고귀한 자의 의무",
                description="파도를 얼리는 광검에 의해 생성된 빛의 검은 즉시 에너지를 5스택 획득한다. 일반 공격, 원소전투 스킬, 혹은 원소폭발로 적에게 피해를 줘서 에너지 스택을 쌓으면 50%의 확률로 1스택이 더 쌓인다.",
                options=[],
            ),
        ],
    ),
}
