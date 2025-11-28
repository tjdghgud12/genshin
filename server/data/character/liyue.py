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
                description="강공격 후 강공격 치명타 확률 증가",
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="서리꽃 화살 발사")],
            ),
            "천지교태": passiveSkillSchema(
                description="원소 폭발 내부에 존재 시 얼음 원소 피해 증가",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="원소 폭발 영역 내 위치")],
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
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="서리꽃 화살 명중")],
            ),
            contellationSchema(name="획린(獲麟)", description="원소 전투 스킬 사용 가능 횟수 1회 증가"),
            contellationSchema(name="구름 여행", description="원고 폭발 레벨 +3"),
            contellationSchema(
                name="서수(西狩)",
                description="원소 폭발 영역 내에서 적이 받는 피해 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=5, label="피해 증가 중첩")],
            ),
            contellationSchema(name="잡초 근절", description="원소 전투 스킬 레벨 +3"),
            contellationSchema(
                name="살생의 발걸음",
                description="원소 전투 스킬 발동 시 첫 번째 서리꽃 화살은 차징 없이 발동",
            ),
        ],
    ),
    "각청": characterDataSchema(
        passiveSkill={
            "하늘에 닿은 뇌벌": passiveSkillSchema(description="원소 전투 스킬 발동 후 번개 원소 인챈트", unlockLevel=1),
            "옥형의 품격": passiveSkillSchema(
                description="원소 폭발 발동 후 치명타 확률 및 원소 충전 효율 증가",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="원소 폭발 발동")],
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
                additionalAttack=[additionalAttackSchema(name="계뢰", type="elec", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["elec"]))],
            ),
            contellationSchema(name="가연", description="일반 공격 또는 강공격이 번개 원소 영향을 받은 적 공격 시 50% 확률로 원소 입자 생성"),
            contellationSchema(name="등루", description="원소 폭발 레벨 +3"),
            contellationSchema(
                name="조율",
                description="각청이 번개 원소 관련 반응 발동 뒤 10초간 공격력 25% 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="번개 원소 관련 반응")],
            ),
            contellationSchema(name="이등", description="원소 전투 스킬 레벨 +3"),
            contellationSchema(
                name="염정",
                description="일반 공격, 강공격, 원소 전투 스킬 혹은 원소폭발 사용 시, 각청은 번개 원소 피해 보너스를 6% 획득",
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=3, label="번개 원소 피해 보너스")],
            ),
        ],
    ),
    "호두": characterDataSchema(
        passiveSkill={
            "모습을 감춘 나비": passiveSkillSchema(description="피안접무 상태가 끝난 후 호두를 제외한 파티 내 모든 캐릭터의 치명타 확률 증가", unlockLevel=1),
            "핏빛 분장": passiveSkillSchema(
                description="현재 hp가 50% 이하일 때 불 원소 피해 증가",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="hp 50% 이하")],
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
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="피안접무")],
                additionalAttack=[additionalAttackSchema(name="혈매향", type="elementalSkill", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["fire"]))],
            ),
            "평안의 서": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(ATTACK=1, element=["fire"]))),
        },
        constellation=[
            contellationSchema(name="진홍의 꽃다발", description="피안접무 상태일 때 강공격에 스테미너를 사용하지 않는다"),
            contellationSchema(name="비처럼 내리는 불안", description="혈매향의 피해가 hp최대치의 10%만큼 증가"),
            contellationSchema(name="적색 피의 의식", description="원소 전투 스킬 레벨 +3"),
            contellationSchema(name="영원한 안식의 정원", description="혈매향 상태 적 처치 시, 호두를 제외한 파티내 캐릭터의 치명타 확률 12% 증가"),
            contellationSchema(name="꽃잎 향초의 기도", description="원소 폭발 레벨 +3"),
            contellationSchema(
                name="나비 잔향",
                description="hp가 25%이하로 떨어지거나 전투 불능이 될 정도의 피해를 입으면 치명타 확률 100%, 모든 내성 200%, 경직 저항력이 대폭 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="hp 25%이하 또는 전투 불능")],
            ),
        ],
    ),
    "야란": characterDataSchema(
        passiveSkill={
            "선공의 묘수": passiveSkillSchema(
                description="파티 내 캐릭터의 원소 타입 종류 마다 야란의 최대 hp 증가",
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=4, label="원소 타입 종류")],
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
            contellationSchema(name="승부에 뛰어든 공모자", description="원소 전투 스킬 사용 가능 횟수 +1"),
            contellationSchema(
                name="올가미에 걸린 적",
                description="원소 폭발의 협동 공격 시 야란 hp 최대치의 14%의 추가 데미지. 쿨타임 1.8초",
                additionalAttack=[additionalAttackSchema(name="올가미에 걸린 적 추가 공격", type="water", baseFightProp=damageBaseFightPropSchema(HP=0.14, element=["water"]))],
            ),
            contellationSchema(name="노름꾼의 주사위", description="원소 폭발 레벨 +3"),
            contellationSchema(
                name="이화접목의 현혹술",
                description="원소 전투 스킬에 명중한 적 당 hp최대치 증가",
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=4, label="원소 전투 스킬 명중")],
            ),
            contellationSchema(name="눈보다 빠른 손", description="원소 전투 스킬 레벨 +3"),
            contellationSchema(
                name="승자의 독식",
                description="원소 폭발 발동 시 일반공격 피해 증가 및 일반공격을 강공격으로 취급",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="전략 설계")],
                additionalAttack=[additionalAttackSchema(name="특수한 타파의 화살", type="charge", baseFightProp=damageBaseFightPropSchema(HP=1, element=["water"]))],
            ),
        ],
    ),
    "신학": characterDataSchema(
        passiveSkill={
            "대동미라존법법": passiveSkillSchema(
                description="선녀 강령 비결 영역 내에 있는 필드 위 캐릭터의 얼음 원소 피해 보너스가 15% 증가한다.",
                unlockLevel=1,
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="선녀 강령 비결 영역 내 위치")],
            ),
            "박령통진법인": passiveSkillSchema(
                description="신학이 위령 소환 구사술 발동 시, 주변의 파티 내 모든 캐릭터가 아래의 효과를 획득한다. · 짧은 터치: 원소전투 스킬과 원소폭발로 가하는 피해가 15% 증가한다. 지속 시간: 10초. · 홀드: 일반 공격, 강공격, 낙하 공격으로 가하는 피해가 15% 증가한다. 지속 시간: 15초.",
                unlockLevel=4,
                options=[skillConstellationOptionSchema(type=skillConstellationType.select, selectList=["짧은 터치", "홀드"], label="조작")],
            ),
        },
        activeSkill={
            "별의 포획자": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                )
            ),
            "위령 소환 구사술": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(elementalSkill=damageBaseFightPropSchema(ATTACK=1, element=["ice"])),
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="얼음의 깃")],
            ),
            "신녀 강령 비결": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(ATTACK=1, element=["ice"])),
                description="선녀 강령 비결 영역 내 적의 얼음 원소 내성과 물리 내성을 감소",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="선녀 강령 비결 영역 내 위치")],
            ),
        },
        constellation=[
            contellationSchema(name="심재", description="위령 소환 구사술의 사용 가능 횟수가 1회 증가한다."),
            contellationSchema(
                name="정몽",
                description="신녀 강령 비결의 지속 시간이 6초 증가한다. 영역 내에 있는 필드 위 캐릭터의 얼음 원소 피해의 치명타 피해가 15% 증가한다.",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="신녀 강령 비결 영역 내 위치")],
            ),
            contellationSchema(name="잠허", description="원소 전투 스킬 레벨 +3"),
            contellationSchema(
                name="통관",
                description=(
                    "신학이 부여한 「얼음의 깃」 상태인 캐릭터가 「얼음의 깃」의 피해 증가 효과 발동 시, 신학이 「서리의 주문」을 1스택 획득한다."
                    "· 신학이 위령 소환 구사술 발동 시 모든 「서리의 주문」이 사라지고, 사라진 스택에 따라 1스택당 위령 소환 구사술이 가하는 피해가 5% 증가한다. "
                    "최대 중첩수: 50회."
                ),
                options=[skillConstellationOptionSchema(type=skillConstellationType.stack, maxStack=50, label="서리의 주문")],
            ),
            contellationSchema(name="화신", description="원소 폭발 레벨 +3"),
            contellationSchema(
                name="망현", description="캐릭터가 일반 공격 피해와 강공격 피해로 「얼음의 깃」의 피해 증가 효과를 발동하면, 「얼음의 깃」의 효과 발동 횟수가 차감되지 않는다."
            ),
        ],
    ),
    "향릉": characterDataSchema(
        passiveSkill={
            "교차 화력": passiveSkillSchema(description="누룽지가 불을 뿜는 거리가 20% 증가한다.", unlockLevel=1),
            "절운차오톈자오": passiveSkillSchema(
                description="누룽지 출격 효과 종료 후 누룽지는 사라진 위치에 고추를 하나 남긴다. 고추를 주우면 공격력이 10% 증가한다.", unlockLevel=4
            ),
        },
        activeSkill={
            "밀가루 음식 솜씨": activeSkillSchema(
                baseFightProp=skillBaseFightPropSchema(
                    nomal=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                    charge=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                    falling=damageBaseFightPropSchema(ATTACK=1, element=["physical"]),
                )
            ),
            "누룽지 출격": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalSkill=damageBaseFightPropSchema(ATTACK=1, element=["fire"]))),
            "화륜": activeSkillSchema(baseFightProp=skillBaseFightPropSchema(elementalBurst=damageBaseFightPropSchema(ATTACK=1, element=["fire"]))),
        },
        constellation=[
            contellationSchema(
                name="겉은 바삭, 속은 촉촉",
                description="누룽지의 공격에 피격된 적은 불 원소 내성이 15% 감소한다. 지속 시간: 6초",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="누룽지 공격")],
            ),
            contellationSchema(
                name="큰불에 기름 붓기",
                description="일반 공격의 최후의 일격은 적에게 2초 동안 지속적인 내폭 효과를 부여한다. 효과 종료 시 폭발하여 주변의 적에게 공격력 75%의 불 원소 범위 피해를 준다.",
                additionalAttack=[additionalAttackSchema(name="내폭(2돌파)", type="nomal", baseFightProp=damageBaseFightPropSchema(ATTACK=0.75, element=["fire"]))],
            ),
            contellationSchema(name="센 불로 조리하기", description="원소 폭발 레벨 +3"),
            contellationSchema(name="약불로 천천히 삶기", description="화륜의 지속 시간을 40% 연장한다."),
            contellationSchema(name="흉포한 누룽지", description="원소 전투 스킬 레벨 +3"),
            contellationSchema(
                name="토네이도 화륜",
                description="화륜이 지속되는 동안 파티 내 모든 캐릭터는 불 원소 피해 보너스를 15% 획득한다.",
                options=[skillConstellationOptionSchema(type=skillConstellationType.toggle, label="화륜 지속")],
            ),
        ],
    ),
}
