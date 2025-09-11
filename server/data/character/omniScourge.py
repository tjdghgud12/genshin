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
    "스커크": characterDataSchema(
        passiveSkill={
            "이치 너머의 이치": passiveSkillSchema(
                description="빙결, 초전도, 얼음 확산, 얼음 결정 반응 발동 시 허계 균열 1개 생성. 허계 균열은 흡수 가능하며 흡수 시 원소 전투 스킬 및 원소 폭발 계수 증가",
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=3, label="흡수 허계 균열 수")],
            ),
            "흐름의 적멸": passiveSkillSchema(
                description="파티 내 주변에 있는 물 원소 또는 얼음 원소 캐릭터가 각각 물 원소 또는 얼음 원소 공격으로 적 명중 시 최종 데미지 증가(마지막 곱연산)",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=3, label="죽음의 강")],
            ),
        },
        activeSkill={
            "극악기·단": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                )
            ),
            "극악기·섬": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(),
                additionalAttack=[
                    additionalAttackSchema(name="극악기·섬(일반공격)", type="nomal", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["ice"])),
                    additionalAttackSchema(name="극악기·섬(강공격)", type="charge", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["ice"])),
                    additionalAttackSchema(name="극악기·섬(낙하공격)", type="falling", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["ice"])),
                ],
            ),
            "극악기·멸": activeSkillSchema(
                description="일곱빛 섬광 모드에서 발동 가능. 주변 일정 범위 내의 허계 균열을 흡수하며, 흡수한 허계 균열 개수 당 일반 공격 피해 증가",
                options=[
                    skillConstellationOptionSchema(
                        type=skillConstellationType.stack,
                        maxStack=3,
                        label="허계 균열 흡수",
                    )
                ],
                baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(ATTACK=1, element=["ice"])),
            ),
        },
        constellation=[
            contellationSchema(
                name="요원",
                description="허계 균열 1개 흡수할 때 마다 스커크 공격력의 500%에 해당하는 얼음 원소 피해 추가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
                additionalAttack=[additionalAttackSchema(name="수정 칼날", type="charge", baseFightProp=damageBaseFightPropSchema(ATTACK=5, element=["ice"]))],
            ),
            contellationSchema(
                name="심연",
                description="원소 전투 스킬 발동 시 뱀의 계략 10pt 획득. 원소 폭발 사용 시 뱀의 계략 최대치 10pt 증가. 극악기 · 진 발동 후 공격력 70% 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            contellationSchema(
                name="악연",
                description="원소 폭발 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="멸류",
                description="죽음의 강 효과 스텍마다 공격력 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="소망",
                description="원소 전투 스킬 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="근원",
                description="흡수한 허계 균열 수 당 극악기 · 참 스택 획득. 극악기 · 참 스택 마다 원소 폭발 발동 시 공격력의 750%에 해당하는 얼음 원소 피해 추가. 일곱빛 섬광 모드에서는 일반공격 또는 피격 시 협동 공격",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
                additionalAttack=[
                    additionalAttackSchema(name="극악기·참(원소 폭발)", type="elementalBurst", baseFightProp=damageBaseFightPropSchema(ATTACK=7.5, element=["ice"])),
                    additionalAttackSchema(name="극악기·참(일반 공격)", type="nomal", baseFightProp=damageBaseFightPropSchema(ATTACK=1.8, element=["ice"])),
                    additionalAttackSchema(name="극악기·참(피격)", type="charge", baseFightProp=damageBaseFightPropSchema(ATTACK=1.8, element=["ice"])),
                ],
            ),
        ],
    ),
}
