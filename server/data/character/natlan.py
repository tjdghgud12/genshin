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
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="융해 발동")],
            ),
            "하얀 불나비의 별옷": passiveSkillSchema(description="원소 마스터리의 일정 비율 만큼 원소 전투 스킬 및 원소 폭발 피해 계수 추가", unlockLevel=4),
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
                description="원소 전투 스킬 발동 시 파티 내 캐릭터가 공격 시 소모되는 별빛 검 스텍을 10개 획득. 별빛 검은 시틀라리의 원소 마스터리의 200%만큼 피해 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="별빛 검")],
            ),
            contellationSchema(
                name="심장을 삼키는 자의 순행",
                description="하얀빛 보호막의 보호를 받고 있거나 이즈파파가 따라다니고 있을 시 원소 마스터리 증가하고, 다섯 번째 하늘의 서리비 강화(물, 불 원소 내성 감소 각각 20% 추가 감소)",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="하얀빛 보호막 또는 이즈파파 소환")],
            ),
            contellationSchema(name="구름뱀의 깃털 왕관", description="원소 전투 스킬 레벨 +3"),
            contellationSchema(
                name="죽음을 거부하는 자의 영혼 해골",
                description="서리 운석 폭풍 명중 시 시틀라리의 원소 마스터리의 1800%만큼의 추가 피해. 재사용 대기시간 8초",
                additionalAttack=[additionalAttackSchema(name="영혼 해골·검은별", type="ice", baseFightProp=damageBaseFightPropSchema(ELEMENT_MASTERY=18, element=["ice"]))],
            ),
            contellationSchema(name="불길한 닷새의 저주", description="원소 폭발 레벨 +3"),
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
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="밤혼 발산")],
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
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="전의 획득")],
            ),
            contellationSchema(name="잿더미의 대가", description="기초 공격력 200pt 증가. 일반공격, 강공격, 원소폭발의 석양 베기로 주는 피해 증가"),
            contellationSchema(name="타오르는 태양", description="원소 폭발 레벨 +3"),
            contellationSchema(name="「지도자」의 각오", description="키온고지 효과 강화"),
            contellationSchema(name="진정한 의미", description="원소 전투 스킬 레벨 +3"),
            contellationSchema(
                name="「인간의 이름」 해방",
                description="불볕 고리: 공격 적중 시 공격력의 200%에 해당하는 밤혼 성질의 불 원소 피해 추가. 바이크 : 주변 적 방어력 20% 감소 및 3초마다 공격력의 500%에 해당하는 밤혼 성질의 불 원소 피해 추가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="불볕 고리·빛 소환")],
                additionalAttack=[
                    additionalAttackSchema(name="불볕 고리·빛", type="fire", baseFightProp=damageBaseFightPropSchema(ATTACK=2, element=["fire"])),
                    additionalAttackSchema(name="바이크", type="fire", baseFightProp=damageBaseFightPropSchema(ATTACK=5, element=["fire"])),
                ],
            ),
        ],
    ),
    "바레사": characterDataSchema(
        passiveSkill={
            "연속! 세 번의 도약": passiveSkillSchema(
                description="원소전투 스킬 밤무지개 도약 발동 후, 바레사가 「무지개 낙하」를 획득한다. 지속 시간 동안 바레사가 낙하 공격 시, 추락 충격이 추가로 공격력의 50%에 해당하는 피해를 준다. 만약 바레사가 열혈 상태인 경우, 추락 충격이 추가로 공격력의 180%에 해당하는 피해를 주도록 변경된다.",
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="무지개 낙하")],
            ),
            "영웅! 두 번의 귀환": passiveSkillSchema(
                description="주변에 있는 파티 내 캐릭터가 「밤혼 발산」 발동 시, 바레사의 공격력이 35% 증가한다. 지속 시간: 12초. 최대 중첩수: 2스택. 스택마다 지속 시간은 독립적으로 계산된다",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=2, label="밤혼 발산")],
            ),
        },
        activeSkill={
            "레슬링 격투술": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["elec"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["elec"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["elec"]),
                )
            ),
            "밤무지개 도약": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalSkill=damageBaseFightPropSchema(ATTACK=1, element=["elec"]))),
            "벼락불 강림!": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(ATTACK=1, element=["elec"])),
                additionalAttack=[
                    additionalAttackSchema(name="벼락불 강림!·대화산 떨구기", type="falling", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["elec"])),
                ],
            ),
        },
        constellation=[
            contellationSchema(
                name="꺼지지 않는 열정",
                description="연속! 세 번의 도약 강화. 특수 낙하 공격·대화산 폭발 진행 시에도 바레사가 「무지개 낙하」를 획득. 바레사의 열혈 상태 여부와 상관없이 「무지개 낙하」 지속 시간 동안 낙하 공격 시, 추락 충격이 추가로 공격력의 180%에 해당하는 피해를 주도록 변경",
            ),
            contellationSchema(
                name="빛의 한계 돌파",
                description="열혈 상태 여부와 상관없이 바레사가 낙하 공격 후, 한계 돌파 상태에 진입한다. 한계 돌파 상태에서 바레사의 경직 저항력이 더 증가한다. 또한 바레사 낙하 공격의 추락 충격이 적에게 명중 시, 바레사의 원소 에너지가 11.5pt 회복된다",
            ),
            contellationSchema(name="불굴의 결심", description="원소 폭발 레벨 +3"),
            contellationSchema(
                name="돌진할 용기",
                description=(
                    "원소폭발 벼락불 강림! 발동 시, 바레사의 상태에 따라 각각 다른 강화 효과가 생성된다: "
                    "·열혈 상태 또는 한계 돌파 상태가 아닐 경우: 바레사가 「용맹한 돌진」 효과를 획득한다. 지속 시간 15초. "
                    "바레사가 낙하 공격 시, 추락 충격으로 적에게 주는 피해가 바레사 공격력의 500%에 기반해 최대 20000pt 증가한다. "
                    "해당 효과는 추락 충격이 적에게 명중하거나 지속 시간이 종료되면 사라진다. "
                    "·열혈 또는 한계 돌파 상태일 경우: 이번 원소폭발 벼락불 강림!으로 주는 피해가 100% 증가한다 "
                ),
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="열혈 또는 한계 돌파")],
            ),
            contellationSchema(name="부드러운 바람의 신념", description="일반 공격 레벨 +3"),
            contellationSchema(name="히어로의 승리", description="바레사의 낙하 공격과 원소폭발 벼락불 강림!의 치명타 확률이 10%, 치명타 피해가 100% 증가한다."),
        ],
    ),
}
