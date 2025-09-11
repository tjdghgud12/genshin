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
    "감우": characterDataSchema(
        passiveSkill={
            "단 하나의 마음": passiveSkillSchema(
                description="강공격 후 강공격 치명타 확률 증가", unlockLevel=1, options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")]
            ),
            "천지교태": passiveSkillSchema(
                description="원소 폭발 내부에 존재 시 얼음 원소 피해 증가",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
        },
        activeSkill={
            "유천 사격술": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["ice"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                ),
            ),
            "산과 강의 기린 흔적": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalSkill=damageBaseFightPropSchema(ATTACK=1, element=["ice"]))),
            "쏟아지는 천화": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(ATTACK=1, element=["ice"]))),
        },
        constellation=[
            contellationSchema(
                name="이슬 먹는 신수",
                description="2단 차지 강공격 또는 서리꽃에 명중된 적의 얼음 원소 내성 감소 15%",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            contellationSchema(
                name="획린(獲麟)",
                description="원소 전투 스킬 사용 가능 횟수 1회 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="구름 여행",
                description="원고 폭발 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="서수(西狩)",
                description="원소 폭발 영역 내에서 적이 받는 피해 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=5, label="피해 증가 중첩")],
            ),
            contellationSchema(
                name="잡초 근절",
                description="원소 전투 스킬 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="살생의 발걸음",
                description="원소 전투 스킬 발동 시 첫 번째 서리꽃 화살은 차징 없이 발동",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
        ],
    ),
    "각청": characterDataSchema(
        passiveSkill={
            "하늘에 닿은 뇌벌": passiveSkillSchema(
                description="원소 전투 스킬 발동 후 번개 원소 인챈트",
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            "옥형의 품격": passiveSkillSchema(
                description="원소 폭발 발동 후 치명타 확률 및 원소 충전 효율 증가",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
        },
        activeSkill={
            "운래 검법": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["physical", "elec"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["physical", "elec"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["physical", "elec"]),
                )
            ),
            "성신 회귀": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalSkill=damageBaseFightPropSchema(ATTACK=1, element=["elec"]))),
            "천가 순유": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(ATTACK=1, element=["elec"]))),
        },
        constellation=[
            contellationSchema(
                name="계뢰",
                description="뇌설이 존재하는 동안 다시 원소 전투 스킬 발동 시 공격력의 50%의 번개 원소 피해 추가. 붙어서 사용할 경우, 사라질 때와 나타날 때 한번 씩 공격",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
                additionalAttack=[additionalAttackSchema(name="계뢰", type="elec", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["elec"]))],
            ),
            contellationSchema(
                name="가연",
                description="일반 공격 또는 강공격이 번개 원소 영향을 받은 적 공격 시 50% 확률로 원소 입자 생성",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="등루",
                description="원소 폭발 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="조율",
                description="각청이 번개 원소 관련 반응 발동 뒤 10초간 공격력 25% 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            contellationSchema(
                name="이등",
                description="원소 전투 스킬 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="염정",
                description="일반 공격, 강공격, 원소 전투 스킬 혹은 원소폭발 사용 시, 각청은 번개 원소 피해 보너스를 6% 획득",
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=3, label="번개 원소 피해 보너스")],
            ),
        ],
    ),
    "호두": characterDataSchema(
        passiveSkill={
            "모습을 감춘 나비": passiveSkillSchema(
                description="피안접무 상태가 끝난 후 호두를 제외한 파티 내 모든 캐릭터의 치명타 확률 증가",
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            "핏빛 분장": passiveSkillSchema(
                description="현재 hp가 50% 이하일 때 불 원소 피해 증가",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
        },
        activeSkill={
            "왕생 비법 창술": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["physical", "fire"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["physical", "fire"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["physical", "fire"]),
                )
            ),
            "나비의 서": activeSkillSchema(
                description="현재 hp의 30%를 소비하여 hp 최대치 기반 공격력 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
                baseFightProp=skillBaseFightPropSchema(),
                additionalAttack=[additionalAttackSchema(name="혈매향", type="elementalSkill", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["fire"]))],
            ),
            "평안의 서": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(ATTACK=1, element=["fire"]))),
        },
        constellation=[
            contellationSchema(
                name="진홍의 꽃다발",
                description="피안접무 상태일 때 강공격에 스테미너를 사용하지 않는다",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="비처럼 내리는 불안",
                description="혈매향의 피해가 hp최대치의 10%만큼 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="적색 피의 의식",
                description="원소 전투 스킬 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="영원한 안식의 정원",
                description="혈매향 상태 적 처치 시, 호두를 제외한 파티내 캐릭터의 치명타 확률 12% 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            contellationSchema(
                name="꽃잎 향초의 기도",
                description="원소 폭발 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="나비 잔향",
                description="hp가 25%이하로 떨어지거나 전투 불능이 될 정도의 피해를 입으면 치명타 확률 100%, 모든 내성 200%, 경직 저항력이 대폭 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
        ],
    ),
    "야란": characterDataSchema(
        passiveSkill={
            "선공의 묘수": passiveSkillSchema(
                description="파티 내 캐릭터의 원소 타입 종류 마다 야란의 최대 hp 증가",
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=4, label="원소 타입 종류 수")],
            ),
            "마음 가는 대로": passiveSkillSchema(
                description="원소 폭발 발동 시 필드 위 캐릭터가 가하는 피해가 1초마다 증가",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=14, label="경과 시간(초)")],
            ),
        },
        activeSkill={
            "빛을 감춘 활": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["physical", "water"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                ),
                additionalAttack=[additionalAttackSchema(name="타파의 화살", type="charge", baseFightProp=damageBaseFightPropSchema(HP=1, element=["water"]))],
            ),  # 6돌파 효과로 평타가 타파의 화살로 전환되는 것은 여기서 커버 못침
            "뒤얽힌 생명줄": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalSkill=damageBaseFightPropSchema(HP=1, element=["water"]))),
            "심오하고 영롱한 주사위": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(HP=1, element=["water"]))),
        },
        constellation=[
            contellationSchema(
                name="승부에 뛰어든 공모자",
                description="원소 전투 스킬 사용 가능 횟수 +1",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="올가미에 걸린 적",
                description="원소 폭발의 협동 공격 시 야란 hp 최대치의 14%의 추가 데미지. 쿨타임 1.8초",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
                additionalAttack=[additionalAttackSchema(name="올가미에 걸린 적 추가 피해", type="water", baseFightProp=damageBaseFightPropSchema(HP=0.14, element=["water"]))],
            ),
            contellationSchema(
                name="노름꾼의 주사위",
                description="원소 폭발 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="이화접목의 현혹술",
                description="원소 전투 스킬에 명중한 적 당 hp최대치 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=4, label="명중 적 수")],
            ),
            contellationSchema(
                name="눈보다 빠른 손",
                description="원소 전투 스킬 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="승자의 독식",
                description="원소 폭발 발동 시 일반공격 피해 증가 및 일반공격을 강공격으로 취급",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
        ],
    ),
}
