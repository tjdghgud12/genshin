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
    "시틀라리": characterDataSchema(
        passiveSkill={
            "다섯 번째 하늘의 서리비": passiveSkillSchema(
                description="융해 반응 발동 시 반응에 영향을 받은 적의 물 원소 및 불 원소 내성 감소",
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            "하얀 불나비의 별옷": passiveSkillSchema(
                description="원소 마스터리의 일정 비율 만큼 원소 전투 스킬 및 원소 폭발 피해 계수 추가",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
        },
        activeSkill={
            "영혼 포착": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["ice"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["ice"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["ice"]),
                )
            ),
            "검은 서리별": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalSkill=damageBaseFightPropSchema(ATTACK=1, element=["ice"]))),
            "반짝이는 칙령": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(ATTACK=1, element=["ice"]))),
        },
        constellation=[
            contellationSchema(
                name="사백 개의 별빛",
                description="파티 내 캐릭터가 공격 시 소모되는 별빛 검 스텍을 10개 획득. 별빛 검은 시틀라리의 원소 마스터리의 200%만큼 피해 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            contellationSchema(
                name="심장을 삼키는 자의 순행",
                description="원소 전투 스킬 사용 시 원소 마스터리 증가 및 다섯 번째 하늘의 서리비 강화(물, 불 원소 내성 감소 각각 20% 추가 감소)",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            contellationSchema(
                name="구름뱀의 깃털 왕관",
                description="원소 전투 스킬 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="죽음을 거부하는 자의 영혼 해골",
                description="서리 운석 폭풍 명중 시 시틀라리의 원소 마스터리의 1800%만큼의 추가 피해. 재사용 대기시간 8초",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
                additionalAttack=[
                    additionalAttackSchema(
                        name="죽음을 거부하는 자의 영혼 해골 추가 피해", type="ice", baseFightProp=damageBaseFightPropSchema(ELEMENT_MASTERY=18, element=["ice"])
                    )
                ],
            ),
            contellationSchema(
                name="불길한 닷새의 저주",
                description="원소 폭발 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="아홉 번째 하늘의 계약",
                description="원소 전투 스킬이 밤혼이 없어도 유지 또한 원소 전투 스킬 발동 시 모든 밤혼 소모하며 이후 소모되는 밤혼 당 신비의 수 스텍 1pt 적립. 신비의 수 스텍 당 파티원 불 원소, 물 원소 피해 증가 + 시틀라리의 피해 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=40, label="밤혼 소모")],
            ),
        ],
    ),
    "마비카": characterDataSchema(
        passiveSkill={
            "타오르는 꽃의 선물": passiveSkillSchema(
                description="파티 내 캐릭터가 밤혼 발산 발동 시 마비카의 공격력 증가",
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            "「키온고지」": passiveSkillSchema(
                description="원소 폭발 발동 후 발동 당시 전의 스텍 1pt당 피해 증가 및 지속 시간 동안 점차 감소",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=200, label="전의")],
            ),
        },
        activeSkill={
            "불로 엮은 삶": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["physical", "fire"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["physical", "fire"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["physical", "fire"]),
                )
            ),
            "해방의 순간": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalSkill=damageBaseFightPropSchema(ATTACK=1, element=["fire"]))),
            "불타는 하늘": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(ATTACK=1, element=["fire"]))),
        },
        constellation=[
            contellationSchema(
                name="밤 주인의 계시",
                description="전의 획득 후 공력력 40% 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            contellationSchema(
                name="잿더미의 대가",
                description="기초 공격력 200pt 증가. 일반공격, 강공격, 원소폭발의 석양 베기로 주는 피해 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="타오르는 태양",
                description="원소 폭발 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="「지도자」의 각오",
                description="키온고지 효과 강화",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="진정한 의미",
                description="원소 전투 스킬 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="「인간의 이름」 해방",
                description="불볕 고리: 공격 적중 시 공격력의 200%에 해당하는 밤혼 성질의 불 원소 피해 추가. 바이크 : 주변 적 방어력 20% 감소 및 3초마다 공격력의 500%에 해당하는 밤혼 성질의 불 원소 피해 추가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
                additionalAttack=[
                    additionalAttackSchema(name="불볕 고리 추가 피해", type="fire", baseFightProp=damageBaseFightPropSchema(ATTACK=2, element=["fire"])),
                    additionalAttackSchema(name="바이크 추가 피해", type="fire", baseFightProp=damageBaseFightPropSchema(ATTACK=5, element=["fire"])),
                ],
            ),
        ],
    ),
}
