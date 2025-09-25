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
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="냉혹한 마음 2스텍 소모")],
            ),
            "솟구치는 전투의 욕망": passiveSkillSchema(
                description="파도를 얼리는 광검 발동 시, 얼음 파도의 와류의 재발동 대기시간이 초기화되고 유라에게 냉혹한 마음 효과를 1스택 부여한다.", unlockLevel=4
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
                    skillConstellationOptionSchema(type=skillConstellationType.toggle, label="냉혹한 마음 소모"),
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
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="냉혹한 마음 소모")],
            ),
            contellationSchema(name="물보라 소녀", description="얼음 파도의 와류 차지 재사용 대기시간이 짧은 터치 재사용 대기시간과 같아질 만큼 감소한다."),
            contellationSchema(name="로렌스의 혈통", description="원소 폭발 레벨 +3"),
            contellationSchema(
                name="열등감 속 고집",
                description="HP가 50% 미만인 적에게 빛의 검이 가하는 피해가 25% 증가한다.",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="적 hp 50% 미만")],
            ),
            contellationSchema(name="기사의 소양", description="원소 전투 스킬 레벨 +3"),
            contellationSchema(
                name="고귀한 자의 의무",
                description="파도를 얼리는 광검에 의해 생성된 빛의 검은 즉시 에너지를 5스택 획득한다. 일반 공격, 원소전투 스킬, 혹은 원소폭발로 적에게 피해를 줘서 에너지 스택을 쌓으면 50%의 확률로 1스택이 더 쌓인다.",
            ),
        ],
    ),
    "모나": characterDataSchema(
        passiveSkill={
            "「할망구, 나 잡아 봐라!」": passiveSkillSchema(
                description="흐르는 허와 실 상태에 진입 후 2초 동안 만약 주변에 적이 존재하면 자동으로 허영을 하나 만들어낸다. 이러한 방식으로 생성된 허영은 2초 동안 지속되며 터지면서 가하는 피해는 수중 환원 피해의 50%이다.",
                unlockLevel=1,
            ),
            "「운명에 맡겨!」": passiveSkillSchema(description="모나의 물 원소 피해 보너스가 추가로 모나 원소 충전 효율의 20%만큼 상승한다.", unlockLevel=4),
        },
        activeSkill={
            "인과 간파": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["water"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["water"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["water"]),
                )
            ),
            "수중 환원": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(elementalSkill=damageBaseFightPropSchema(ATTACK=1, element=["water"])),
                additionalAttack=[additionalAttackSchema(name="폭렬", type="elementalSkill", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["water"]))],
            ),
            "별의 운명": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(ATTACK=1, element=["water"])),
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="성이(星異)")],
            ),
        },
        constellation=[
            contellationSchema(
                name="침몰한 예언",
                description="파티 내 자신의 캐릭터가 성이 상태의 적을 명중하면 8초 동안 물 원소 관련 반응의 효과가 상승한다.",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="성이 상태 적 공격")],
            ),
            contellationSchema(name="성월의 연주", description="일반 공격 명중 시 20%의 확률로 강공격을 1회 추가 발동한다."),
            contellationSchema(name="멈추지 않는 천상", description="원소 폭발 레벨 +3"),
            contellationSchema(
                name="절멸의 예언",
                description="파티 내 모든 캐릭터가 성이 상태의 적을 공격 시 치명타 확률이 15% 증가한다.",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="성이 상태 적 공격")],
            ),
            contellationSchema(name="운명의 우롱", description="원소 전투 스킬 레벨 +3"),
            contellationSchema(
                name="악운의 수식",
                description="흐르는 허와 실 상태에 진입 후 1초 이동할 때마다 모나의 다음 강공격 피해가 60% 증가한다. 이러한 방식으로 강공격 피해가 최대 180%까지 증가할 수 있다.",
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=3, label="시간(초)")],
            ),
        ],
    ),
}
