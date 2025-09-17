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
    "푸리나": characterDataSchema(
        passiveSkill={
            "끝없는 왈츠": passiveSkillSchema(
                description="필드 위 캐릭터가 치유 받을 시 푸리나의 치유가 아닌 동시에 회복량이 초과된 경우 주변 파티 내 캐릭터 hp 회복",
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            "고독한 독백": passiveSkillSchema(
                description="푸리나의 최대 hp 1000pt 당 원소 전투 스킬 피해 증가",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
        },
        activeSkill={
            "독무자의 초대": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["physical", "water"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["physical", "water"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["physical", "water"]),
                )
            ),
            "고고한 살롱": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalSkill=damageBaseFightPropSchema(HP=1, element=["water"]))),
            "성대한 카니발": activeSkillSchema(
                description="무대 열기 당 피해 증가 및 치유 보너스 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=300, label="무대 열기")],
            ),
        },
        constellation=[
            contellationSchema(
                name="「사랑은 애걸해도 길들일 수 없는 새」",
                description="원소 폭발 발동 시 무대 열기 +150pt 및 무대 열기 최대치 +100pt",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="「여자의 마음은 흔들리는 부평초」",
                description="원소 폭발 발동 시 지속 시간 동인 무대 열기 당 hp최대치 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="「내 이름은 그 누구도 모르리라」",
                description="원소 폭발 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="「저승에서 느낀 삶의 소중함!」",
                description="원소 전투 스킬이 적 명중 또는 파티원 회복 시 원소 에너지 획득",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="「난 알았노라, 그대의 이름은…!」",
                description="원소 전투 스킬 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="「모두 사랑의 축배를 들렴!」",
                description="원소 전투 스킬 발동 시 일반공격, 강공격, 낙하공격이 물 원소 피해로 변경되며 hp최대치의 18%만큼 증가. 프뉴마 상태일 때 일반공격, 강공격, 낙하공격의 추락충격으로 주는 피해가 hp최대치의 25%만큼 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
        ],
    ),
    "느비예트": characterDataSchema(
        passiveSkill={
            "생존한 고대바다의 계승자": passiveSkillSchema(
                description="물 원소 관련 반응 발동 시 강공격 피해 증가",
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=3, label="생존한 용의 영광")],
            ),
            "드높은 중재의 규율": passiveSkillSchema(
                description="현재 hp 중 hp 최대치의 30%를 초과하는 부분을 기반으로 1% 당 물 원소 피해 증가",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=50, label="hp 최대치 초과분(%)")],
            ),
        },
        activeSkill={
            "공평한 물처럼": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["water"]),
                    charge=damageBaseFightPropSchema(HP=1, element=["water"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["water"]),
                )
            ),
            "눈물이여, 반드시 갚으리라": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalSkill=damageBaseFightPropSchema(HP=1, element=["water"]))),
            "밀물이여, 내가 돌아왔노라": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(HP=1, element=["water"]))),
        },
        constellation=[
            contellationSchema(
                name="위대한 제정",
                description="생존한 용의 영광을 1 스택 획득 및 강공격 시 경직 저항력 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="법의 계율",
                description="생존한 용의 영광 1스텍 당 강공격 치명타 피해 14% 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="고대의 의제",
                description="일반공격 스킬 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="연민의 왕관",
                description="치유 받을 시 원천의 방울 1개 생성",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="정의의 판결",
                description="원소 폭발 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="분노의 보상",
                description="강공격 명중 시 hp최대치의 10% 물 원소 피해를 주는 격류 2개 소환",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
                additionalAttack=[additionalAttackSchema(name="격류", type="charge", baseFightProp=damageBaseFightPropSchema(HP=0.1, element=["water"]))],
            ),
        ],
    ),
    "에스코피에": characterDataSchema(
        passiveSkill={
            "밥이 보약": passiveSkillSchema(
                description="원소 폭발 발동 후 파티 내 모든 캐릭터 hp 회복",
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            "영감의 조미료": passiveSkillSchema(
                description="원소 전투 스킬 또는 원소 폭발 명중 시 파티 내 물 원소 캐릭터 또는 얼음 원소 캐릭터 수 마다 명중한 적 물 원소 내성 및 얼음 원소 내성 감소",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=4, label="물 또는 얼음 원소 파티원 수")],
            ),
        },
        activeSkill={
            "셰프의 비결": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                )
            ),
            "저온 조리법": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalSkill=damageBaseFightPropSchema(ATTACK=1, element=["ice"]))),
            "현란한 칼솜씨": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(ATTACK=1, element=["ice"]))),
        },
        constellation=[
            contellationSchema(
                name="미각을 깨우는 식전 공연",
                description="파티 내 캐릭터의 원소 타입이 모두 물 또는 얼음인 경우, 원소 전투 스킬 또는 원소 폭발 발동 후 얼음 원소 피해를 줄 시 치명타 피해 60% 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            contellationSchema(
                name="예술의 경지에 이른 스튜",
                description="원소 전투 스킬 발동 시 피해를 에스코피에의 공격력의 240%만큼 증가시키는 즉석 요리 스텍 획득",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            contellationSchema(
                name="캐러멜화의 마법",
                description="원소 전투 스킬 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="로즈마리 비밀 레시피",
                description="식이 요법 지속시간 증가 및 식이 요법으로 치유 시 원소 에너지 획득",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="다채로운 소스의 교향곡",
                description="원소 폭발 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="무지갯빛 티타임",
                description="현재 필드 위에 있는 파티 내 자신의 캐릭터의 일반공격, 강공격, 낙하공격이 명중 시 에스코피에의 공격력의 500%에 해당하는 얼음 원소 추가 피해",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
                additionalAttack=[
                    additionalAttackSchema(name="무지갯빛 티타임 추가 피해", type="elementalSkill", baseFightProp=damageBaseFightPropSchema(ATTACK=5, element=["ice"]))
                ],
            ),
        ],
    ),
    "클로린드": characterDataSchema(
        passiveSkill={
            "밤을 가르는 불꽃": passiveSkillSchema(
                description="번개 원소 관련 반응 발동 시 일반 공격 및 원소 폭발의 번개 원소 피해 증가",
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=3, label="번개 원소 관련 반응")],
            ),
            "계약의 보상": passiveSkillSchema(
                description="생명의 계약 수치가 증가 또는 감소 시 치명타 확률 10%씩 증가(2중첩)",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=2, label="생명의 계약 변화")],
            ),
        },
        activeSkill={
            "그림자 사냥의 맹세": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                )
            ),
            "밤 사냥": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(),
                additionalAttack=[
                    additionalAttackSchema(name="수렵", type="nomal", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["elec"])),
                    additionalAttackSchema(name="밤 꿰뚫기", type="elementalSkill", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["elec"])),
                    additionalAttackSchema(name="솟구치는 칼날", type="elec", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["elec"])),
                ],
            ),
            "곧 꺼질 여광": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(ATTACK=1, element=["elec"]))),
        },
        constellation=[
            contellationSchema(
                name="「지금부터 촛불의 장막을 지나」",
                description="밤 사냥 상태의 일반 공격 적중 시 합동 공격 2회 진행",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
                additionalAttack=[additionalAttackSchema(name="협동 공격", type="nomal", baseFightProp=damageBaseFightPropSchema(ATTACK=0.3, element=["elec"]))],
            ),
            contellationSchema(
                name="「지금부터 긴 밤의 위험에 맞선다」",
                description="밤을 가르는 불꽃의 효과 강화",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="「난 낮의 맹세를 명심하고」",
                description="원소 전투 스킬 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="「눈물, 생명, 사랑을 간직하며」",
                description="생명의 계약 백분율에 따라 원소 폭발 피해 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=100, label="생명의 계약(%)")],
            ),
            contellationSchema(
                name="「언젠가 찾아올 여명을 믿겠다」",
                description="원소 폭발 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="「절대 희망을 버리지 않으리라」",
                description="원소 전투 스킬 발동 시 치명타 피해 및 치명타 확률 증가. 특정 조건마다 일반 공격 판정의 추가 번개 원소 피해 타격",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
                additionalAttack=[additionalAttackSchema(name="촛불의 그림자", type="nomal", baseFightProp=damageBaseFightPropSchema(ATTACK=2, element=["elec"]))],
            ),
        ],
    ),
    "나비아": characterDataSchema(
        passiveSkill={
            "비밀 유통 경로": passiveSkillSchema(
                description="결정 축포 발동 후 4초 동안 나비아의 일반 공격, 강공격, 낙하 공격이 주는 피해가 다른 원소 부여 효과로 대체될 수 없는 바위 원소 피해로 전환되고 나비아의 일반 공격, 강공격, 낙하 공격이 주는 피해가 40% 증가한다",
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="")],
            ),
            "상호 협력망": passiveSkillSchema(
                description="파티 내 불 원소/번개 원소/얼음 원소/물 원소 캐릭터가 1명 존재할 때마다 나비아의 공격력이 20% 증가한다.(2중첩)",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=2, label="캐릭터 수")],
            ),
        },
        activeSkill={
            "솔직한 거절": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["physical", "rock"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["physical", "rock"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["physical", "rock"]),
                )
            ),
            "결정 축포": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(elementalSkill=damageBaseFightPropSchema(ATTACK=1, element=["rock"])),
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=6, label="소모 결정 파편")],
                additionalAttack=[additionalAttackSchema(name="솟구치는 칼날", type="rock", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["rock"]))],
            ),
            "창공을 울리는 포성": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(ATTACK=1, element=["rock"])),
                additionalAttack=[additionalAttackSchema(name="지원 포격", type="elementalBurst", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["rock"]))],
            ),
        },
        constellation=[
            contellationSchema(
                name="숙녀의 거리감 수칙",
                description="결정 파편 소모할 때 소모 갯수 당 원소 에너지 회복 및 원소 폭발 쿨타임 감소",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="통솔자의 승승장구",
                description="결정 축포 발동 시, 「결정 파편」을 1개 소모할 때마다 이번 결정 축포의 치명타 확률이 12% 증가한다. 해당 방식으로 결정 축포의 치명타 확률은 최대 36% 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=3, label="소모 결정 파편")],
            ),
            contellationSchema(
                name="경영자의 넓은 시야",
                description="원소 전투 스킬 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="맹세자의 엄격함",
                description="원소 폭발 명중 적 바위 원소 내성 감소",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, maxStack=1, label="원소 폭발 명중")],
            ),
            contellationSchema(
                name="협상가의 단호함",
                description="원소 폭발 레벨 +3",
                options=[skillConstellationOptionSchema(type=skillConstellationType.always, maxStack=1, label="")],
            ),
            contellationSchema(
                name="보스의 기민한 수완",
                description="결정 축포 발동 시, 「결정 파편」을 3개 넘게 소모하면 3개를 초과한 「결정 파편」 1개당 이번 결정 축포의 치명타 피해가 45% 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=3, label="소모 결정 파편")],
            ),
        ],
    ),
}
