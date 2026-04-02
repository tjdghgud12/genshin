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
        witchsEve=True,
        passiveSkill={
            "「할망구, 나 잡아 봐라!」": passiveSkillSchema(
                description="흐르는 허와 실 상태에 진입 후 2초 동안 만약 주변에 적이 존재하면 자동으로 허영을 하나 만들어낸다. 이러한 방식으로 생성된 허영은 2초 동안 지속되며 터지면서 가하는 피해는 수중 환원 피해의 50%이다.",
                unlockLevel=1,
            ),
            "「운명에 맡겨!」": passiveSkillSchema(description="모나의 물 원소 피해 보너스가 추가로 모나 원소 충전 효율의 20%만큼 상승한다.", unlockLevel=4),
            "마녀의 전야제·천체 운행론": passiveSkillSchema(
                description="마녀의 과제 · 갈망를 완료하면, 모나가 마도 캐릭터가 된다. 파티에 마도 캐릭터를 2명 이상 편성하면 마도 · 비밀 의식 효과를 획득해 마도 캐릭터가 강화된다."
                "마도 · 비밀 의식"
                "모나의 일반 공격 또는 강공격이 적에게 명중 시, 「수성천의 빛」을 1스택 획득한다. 지속 시간: 8초, 최대 중첩수: 3스택. 0.1초마다 해당 방식으로 「수성천의 빛」을 최대 1스택 획득할 수 있다."
                "파티 내 자신의 다른 캐릭터가 적에게 증발 반응 발동 시, 모든 「수성천의 빛」이 소모되고, 소모된 1스택당 이번 증발 반응으로 주는 피해가 5% 증가한다."
                "또한 모나의 일반 공격 또는 강공격이 적에게 명중 시, 적의 성이 상태가 2초 연장된다. 해당 효과는 0.5초마다 최대 1회 발동되며, 해당 방식으로 적의 성이 상태를 최대 8초 연장할 수 있다",
                unlockLevel=0,
            ),
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
                options=[
                    skillConstellationOptionSchema(type=skillConstellationType.toggle, label="성이 상태 적 공격"),
                    skillConstellationOptionSchema(type=skillConstellationType.toggle, label="대기 상태"),
                ],
            ),
            contellationSchema(
                name="성월의 연주",
                description="일반 공격 명중 시 20%의 확률로 강공격을 1회 추가 발동한다."
                "모나의 강공격이 적에게 명중 시 주변에 있는 파티 내 모든 캐릭터의 원소 마스터리가 80pt 증가한다. 지속시간: 12초",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="강공격 명중")],
            ),
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
    "바르카": characterDataSchema(
        passiveSkill={
            "새벽 바람의 행군": passiveSkillSchema(
                description="파티에 불 원소, 물 원소, 번개 원소 또는 얼음 원소 캐릭터가 존재할 시,"
                "바르카의 공격력에 기반해 공격력 1000pt마다 바르카가 10%의 바람 원소 피해 보너스와 상응하는 원소 피해 보너스를 획득한다."
                "(해당 방식으로 상술한 원소 타입 중 최대 한 가지 원소 타입의 피해 보너스만 획득 가능)"
                "해당 방식으로 최대 25%의 보너스를 획득할 수 있다."
                "또한 파티에 바람 원소 캐릭터가 2명 이상 존재하거나, 원소 타입이 동일한 불 원소, 물 원소, 번개 원소 또는 얼음 원소 캐릭터가 2명 이상 존재할 경우,"
                "바르카가 광풍 모드에서 일반 공격, 강공격, 특수 강공격 푸른 포식 및 특수 원소전투 스킬 사풍의 도래 발동 시 기존의 140%에 해당하는 피해를 준다."
                "파티에 바람 원소 캐릭터가 2명 이상 존재하는 동시에 원소 타입이 동일한 불 원소, 물 원소, 번개 원소 또는 얼음 원소 캐릭터가 2명 이상 존재할 경우, 상술한 효과가 220%까지 증가한다.",
                unlockLevel=1,
                options=[
                    skillConstellationOptionSchema(type=skillConstellationType.stack, selectList=["불", "물", "번개", "얼음"], label="원소"),
                    skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=2, label="바람 원소 수"),
                    skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=2, label="동일 4대 원소 수"),
                ],
            ),
            "선봉의 바람 깃털": passiveSkillSchema(
                description="주변에 있는 파티 내 캐릭터가 확산 반응 발동 시, 바르카가 「푸른 송곳니」를 1스택 획득하고,"
                "바르카가 광풍 모드에서 일반 공격, 강공격, 특수 강공격 푸른 포식 및 특수 원소전투 스킬 사풍의 도래로 주는 피해가 7.5% 증가한다. 지속 시간: 8초, 최대 중첩수: 4스택."
                "해당 방식을 통해 캐릭터마다 바르카에게 1초에 최대 1스택의 「푸른 송곳니」 효과를 부여할 수 있다",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=4, label="푸른 송곳니")],
            ),
            "바람의 승전가": passiveSkillSchema(
                description="파티 내 몬드 캐릭터 1명당 원소전투 스킬 열풍의 추락의 재사용 대기시간이 5% 감소한다. 해당 효과는 비경, 영역 토벌, 나선 비경에서 적용되지 않는다",
                unlockLevel=0,
            ),
            "마녀의 전야제·돌아온 여명": passiveSkillSchema(
                description="마녀의 과제 · 무제 완료 후, 바르카는 마도 캐릭터가 된다. 파티에 마도 캐릭터를 2명 이상 편성하면 마도 · 비밀 의식 효과를 획득해 마도 캐릭터가 강화된다."
                "마도 · 비밀 의식"
                "특수 원소전투 스킬 사풍의 도래 강화: 바르카가 광풍 모드에서 일반 공격으로 적 명중 시, 사풍의 도래의 재사용 대기시간이 1초 감소한다",
                unlockLevel=0,
            ),
        },
        activeSkill={},
        constellation=[],
    ),
}
