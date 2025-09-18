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
    "카미사토 아야카": characterDataSchema(
        passiveSkill={
            "천죄국죄 진사": passiveSkillSchema(
                description="원소 전투 스킬 발동 후 일반공격 및 강공격 피해 증가",
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            "한천선명 축사": passiveSkillSchema(
                description="싸락눈 걸음 명중 후 얼음 원소 피해 증가",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
        },
        activeSkill={
            "카미사토류·경(傾)": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["physical", "ice"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["physical", "ice"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["physical", "ice"]),
                )
            ),
            "카미사토류·얼음꽃": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalSkill=damageBaseFightPropSchema(ATTACK=1, element=["ice"]))),
            "카미사토류·멸망의 서리": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(ATTACK=1, element=["ice"]))),
        },
        constellation=[
            contellationSchema(
                name="서리에 검게 물든 벚꽃",
                description="일반 공격 또는 강공격으로 얼음 원소 피해를 주면, 50% 확률로 원소 전투 스킬의 재사용 대기시간이 0.3초 감소",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="삼중 서리 관문",
                description="원소 폭발 발동 시 기존 공격력의 20%의 피해를 주는 소형 서리 관문 2개 추가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="흩날리는 카미후부키",
                description="원소 폭발 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="영고성쇠",
                description="원소 폭발의 피해를 받은 적의 방어력 30% 감소",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            contellationSchema(
                name="화운종월경",
                description="원소 전투 스킬 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="물에 비친 달",
                description="10초마다 강공격 피해를 0.5초간 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
        ],
    ),
    "라이덴 쇼군": characterDataSchema(
        passiveSkill={
            "수천수만의 염원": passiveSkillSchema(
                description="원소 입자 획득 시 원력 스텍 추가", unlockLevel=1, options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")]
            ),
            "비범한 옥체": passiveSkillSchema(
                description="원소 충전 효율이 100%초과 시 초과 분 1% 당 번개 원소 피해 증가",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
        },
        activeSkill={
            "원류": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                )
            ),
            "초월·악요개안": activeSkillSchema(
                description="원소 폭발의 원소 에너지 당 원소 폭발 피해 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
                baseFightProp=skillBaseFightPropSchema(elementalSkill=damageBaseFightPropSchema(ATTACK=1, element=["elec"])),
            ),
            "오의·몽상진설": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(ATTACK=1, element=["elec"]))),
        },
        constellation=[
            contellationSchema(
                name="악요 명문(銘文)",
                description="염원이 깃든 백안지륜이 더욱 빠르게 원력을 축적",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="강철 절단",
                description="원소 폭발 상태 시 적의 방여력 60%를 무시한다",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            contellationSchema(
                name="진영의 과거",
                description="원소 폭발 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="진리의 맹세",
                description="원소 폭발 종료 후 라이덴 쇼군을 제외한 파티원의 공력력 30% 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            contellationSchema(
                name="쇼군의 현형",
                description="원소 전투 스킬 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="염원의 대행인",
                description="원소 폭발 상태에서 적 명중 시 라이덴 쇼군을 제외한 파티원의 원소 폭발 재사용 대기시간 감소",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
        ],
    ),
    "요이미야": characterDataSchema(
        passiveSkill={
            "소매불 백경도": passiveSkillSchema(
                description="염초 정화(庭火)의 춤 지속 시간 동안 요이미야의 일반 공격이 명중되면 요이미야에게 불 원소 피해 보너스를 2% 제공",
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=10, label="일반 공격 명중")],
            ),
            "한낮의 풍물시": passiveSkillSchema(
                description="유금 운간초를 발동하면 고유 특성 「소매불 백경도」의 중첩 스택에 따라 1스택마다 추가로 공격력이 1% 증가",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
        },
        activeSkill={
            "쏘아 올린 불꽃": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["physical", "fire"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["physical", "fire"]),
                ),
                additionalAttack=[additionalAttackSchema(name="염초 화살(강공격)", type="fire", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["fire"]))],
            ),
            "염초 정화(庭火)의 춤": activeSkillSchema(
                description="일반 공격이 염초 화살로 전환되며, 일반공격 피해가 최종 연산으로 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            "유금 운간초": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(ATTACK=1, element=["fire"])),
                additionalAttack=[additionalAttackSchema(name="유금화광", type="fire", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["fire"]))],
            ),
        },
        constellation=[
            contellationSchema(
                name="적옥의 유금",
                description="유금 운간초의 유금화광 지속 시간이 4초 증가. 요이미야의 유금화광 상태의 적이 효과 지속 시간 내에 처치되면, 요이미야의 공격력이 20% 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            contellationSchema(
                name="만등 점화",
                description="요이미야의 불 원소 피해가 치명타를 입힌 후, 요이미야는 6초 동안 25%의 불 원소 피해 보너스를 획득. 요이미야가 대기 상태일 때도 해당 효과를 획득",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            contellationSchema(
                name="쥐불놀이",
                description="원소 전투 스킬 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="폭죽장인의 깨달음",
                description="요이미야 자신의 유금화광이 폭발할 때 염초 정화(庭火)의 춤의 재사용 대기시간이 1.2초 감소한다.",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            contellationSchema(
                name="한여름의 전야제",
                description="원소 폭발 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="나가노하라 유성군",
                description="염초 정화(庭火)의 춤 지속 시간 동안 요이미야가 일반 공격을 사용하면, 50%의 확률로 염초 화살을 추가로 1발 더 발사해 기존 피해의 60%에 해당하는 피해를 준다. 해당 피해는 일반 공격 피해로 간주한다.",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
                additionalAttack=[additionalAttackSchema(name="염초 화살(6돌)", type="nomal", baseFightProp=damageBaseFightPropSchema(ATTACK=0.6, element=["fire"]))],
            ),
        ],
    ),
}
