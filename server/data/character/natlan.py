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
    "실로닌": characterDataSchema(
        passiveSkill={
            "네토틸리즈틀리": passiveSkillSchema(
                description=(
                    "실로닌이 밤혼 가호 상태에서 「음원 샘플」 타입에 따라 실로닌의 일반 공격과 낙하 공격이 상응하는 강화 효과를 받는다"
                    "·원소 전환이 발생한 「음원 샘플」 최소 2개 이상 보유: 적에게 명중 시, 밤혼을 35pt 획득한다. 해당 효과는 0.1초마다 최대 1회 발동된다."
                    "·원소 전환이 발생한 「음원 샘플」 2개 미만 보유: 주는 피해가 30% 증가한다"
                ),
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="원소 전환 가능 음원 샘플 2개 이상")],
            ),
            "휴대용 갑옷": passiveSkillSchema(
                description=(
                    "밤혼 가호 상태에서 실로닌의 밤혼이 최대치 도달 시, 「밤혼 발산」과 동일한 효과를 1회 발동한다. 해당 효과는 14초마다 최대 1회 발동된다."
                    "또한 파티 내 주변에 있는 캐릭터가 「밤혼 발산」 발동 시, 실로닌의 방어력이 20% 증가한다. 지속 시간: 15초"
                ),
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="밤혼 발산")],
            ),
        },
        activeSkill={
            "예리한 사냥": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                    falling=damageBaseFightPropSchema(DEFENSE=1, element=["physical", "rock"]),
                ),
                additionalAttack=[additionalAttackSchema(name="칼날바퀴 수렵", type="nomal", baseFightProp=damageBaseFightPropSchema(DEFENSE=1, element=["rock"]))],
            ),
            "음악 단조": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(elementalSkill=damageBaseFightPropSchema(DEFENSE=1, element=["rock"])),
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="음원 샘플 활성화")],
            ),
            "야생의 리듬!": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(DEFENSE=1, element=["rock"]))),
        },
        constellation=[
            contellationSchema(
                name="잠에 바치는 휴일",
                description="실로닌의 밤혼 가호 상태가 소모하는 밤혼과 열소가 30% 감소하고 밤혼의 제한 시간이 45% 연장된다."
                "또한 실로닌의 「음원 샘플」이 활성화 시, 주변에 있는 파티 내 현재 필드 위 캐릭터의 경직 저항력이 증가한다",
            ),
            contellationSchema(
                name="불타는 들판에 바치는 오중주",
                description="실로닌이 휴대한 바위 원소 「음원 샘플」이 활성화 상태를 계속 유지한다. 또한 실로닌의 「음원 샘플」 활성화 시, 「음원 샘플」의 원소 타입에 따라 주변에 있는 파티 내 모든 동일 원소 타입의 캐릭터가 상응하는 효과를 획득한다:"
                "·바위 원소: 주는 피해 50% 증가."
                "·불 원소: 공격력 45% 증가."
                "·물 원소: HP 최대치 45% 증가."
                "·얼음 원소: 치명타 피해 60% 증가."
                "·번개 원소: 원소 에너지 25pt 회복 및 원소폭발의 재사용 대기시간 6초 감소",
                options=[
                    skillConstellationOptionSchema(type=skillConstellationType.toggle, label="바위 원소 음원 샘플"),
                    # skillConstellationOptionSchema(type=skillConstellationType.toggle, label="불 원소 음원 샘플"),
                    # skillConstellationOptionSchema(type=skillConstellationType.toggle, label="물 원소 음원 샘플"),
                    # skillConstellationOptionSchema(type=skillConstellationType.toggle, label="얼음 원소 음원 샘플"),
                    # skillConstellationOptionSchema(type=skillConstellationType.toggle, label="번개 원소 음원 샘플"),
                ],
            ),
            contellationSchema(name="태양에 바치는 순환", description="원소 전투 스킬 레벨 +3"),
            contellationSchema(
                name="오후에 바치는 꽃의 꿈",
                description="실로닌이 음악 단조 발동 후, 주변에 있는 파티 내 모든 캐릭터에게 「영광의 꽃 축복」 효과를 부여한다. 지속 시간: 15초."
                "「영광의 꽃 축복」을 보유한 캐릭터가 일반 공격, 강공격, 낙하 공격으로 주는 피해가 실로닌의 방어력의 65%만큼 증가한다. 해당 효과는 6회 발동 또는 지속 시간 종료 시 사라진다."
                "동시에 여러 기의 적에게 명중 시, 명중한 적의 수에 따라 적용 횟수가 소모된다. 파티 내에 「영광의 꽃 축복」을 보유한 캐릭터가 있으면, 해당 캐릭터의 적용 횟수는 단독으로 계산한다",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="영광의 꽃 축복")],
            ),
            contellationSchema(name="석양에 바치는 변화", description="원소 폭발 레벨 +3"),
            contellationSchema(
                name="영원한 밤에 바치는 춤",
                description=(
                    "밤혼 가호 상태에서 실로닌이 대시, 도약, 일반 공격, 낙하 공격 시, 「영원한 밤 축복」을 획득한다. 밤혼 가호 상태의 제한을 무시하고 일반 공격과 낙하 공격으로 주는 피해가 증가한다. 지속 시간: 5초."
                    "지속 시간 동안 실로닌의 밤혼 제한 시간 카운트가 멈추고, 실로닌의 밤혼, 열소, 스테미너가 감소하지 않는다. 또한 밤혼이 최대치에 도달해도 실로닌의 밤혼 가호 상태가 종료되지 않는다."
                    "실로닌이 밤혼 가호 상태에서 일반 공격과 낙하 공격으로 주는 피해가 실로닌의 방어력의 300%만큼 증가한다. 1.5초마다 주변에 있는 파티 내 모든 캐릭터의 HP를 회복한다."
                    "회복량은 실로닌 방어력의 120%에 해당한다."
                    "「영원한 밤 축복」 효과는 15초마다 최대 1회 획득할 수 있다."
                ),
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="영원한 밤 축복")],
            ),
        ],
    ),
}
