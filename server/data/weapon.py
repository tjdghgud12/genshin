from schemas.weapon import weaponOptionSchema, weaponOptionType


ambrWeaponCurve: dict[str, dict] = {}

weaponInfo = {
    "아모스의 활": [
        weaponOptionSchema(description="일반공격 및 강공격 피해 증가"),
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=5, description="일반공격과 강공격 화살이 발사된 후 0.1초가 지날 때마다 피해 증가", label="경과 시간(0.1초)"),
    ],
    "안개를 가르는 회광": [
        weaponOptionSchema(description="원소 피해 증가"),
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=3, description="무절의 문장 보유 개수 당 원소 피해 증가", label="무절의 문장"),
    ],
    "용의 포효": [
        weaponOptionSchema(type=weaponOptionType.toggle, description="불, 번개 원소 피해 증가", label="불 또는 번개 원소 부착"),
    ],
    "떠오르는 천일 밤의 꿈": [
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=3, description="동일 원소 타입 파티원 당 원소 마스터리 증가", label="동일 원소 파티원"),
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=3, description="다른 원소 타입 파티원 당 원소 피해 증가", label="다른 원소 파티원"),
    ],
    "예초의 번개": [
        weaponOptionSchema(type=weaponOptionType.toggle, description="원소폭발 발동 후 12초 동안 원소 충전 효율 증가", label="원소 폭발"),
        weaponOptionSchema(description="원소 충전 효율이 100%를 초과할 경우, 초과된 부분의 28/35/42/49/56%만큼 공격력이 증가"),
    ],
    "호마의 지팡이": [
        weaponOptionSchema(description="hp 20% 증가"),
        weaponOptionSchema(description="hp 최대치에 따라 공격력 증가"),
        weaponOptionSchema(type=weaponOptionType.toggle, description="체력 50% 미만 시 효과 강화", label="체력 50% 미만"),
    ],
    "창백한 섬광": [
        weaponOptionSchema(type=weaponOptionType.toggle, description="원소 전투 스킬 발동 시 공격력 증가", label="원소 전투 스킬 발동"),
        weaponOptionSchema(type=weaponOptionType.toggle, description="원소 에너지가 0이면, 공격력 및 치명타 피해 증가", label="원소 에너지 0"),
    ],
    "맛의 지휘자": [
        weaponOptionSchema(description="공격력 증가"),
        weaponOptionSchema(type=weaponOptionType.toggle, description="대기 상태 시 공격력 증가", label="대기 상태"),
        weaponOptionSchema(type=weaponOptionType.toggle, description="치유 진행 시 공격력 증가", label="치유 진행"),
    ],
    "고요히 샘솟는 빛": [
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=3, description="현재 hp 변화 시 원소 전투 스킬 피해 증가", label="hp 변화 횟수(피해 증가)"),
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=2, description="파티 내 다른 캐릭터의 현재 hp 변화 시 장착 캐릭터 hp 최대치 증가", label="hp 변화 횟수(hp 증가)"),
    ],
    "별지기의 시선": [
        weaponOptionSchema(description="원소 마스터리 증가"),
        weaponOptionSchema(type=weaponOptionType.toggle, description="파티 내에 있는 필드 위 캐릭터가 자신과 가까운 범위 내의 적에게 주는 피해 증가", label="보호막"),
    ],
    "영원히 샘솟는 법전": [
        weaponOptionSchema(description="hp 증가"),
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=3, description="현재 hp 변화 시 강공격 피해 증가", label="hp 변화 횟수"),
    ],
    "타오르는 천 개의 태양": [
        weaponOptionSchema(type=weaponOptionType.toggle, description="원소 전투 스킬 또는 원소 폭발 발동 시 공격력 및 치명타 피해 증가(불빛)", label="불빛"),
        weaponOptionSchema(type=weaponOptionType.toggle, description="밤혼 가호 상태에서는 불빛 효과 강화", label="밤혼 가호"),
    ],
    "사면": [
        weaponOptionSchema(description="치명타 피해가 증가한다."),
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=3, description="생명의 계약 증가 시 캐릭터가 주는 피해가 증가한다", label="생명의 계약 증가"),
    ],
    "붉은 달의 형상": [
        weaponOptionSchema(type=weaponOptionType.toggle, maxStack=3, description="생명의 계약 보유 시 캐릭터가 주는 피해가 증가한다", label="생명의 계약 보유"),
        weaponOptionSchema(
            type=weaponOptionType.toggle, maxStack=3, description="생명의 계약이 HP최대치의 30% 이상일 시 캐릭터가 주는 피해가 증가한다", label="생명의 계약 최대 HP 30% 이상"
        ),
    ],
    "무공의 검": [
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=5, description="공격 명중 시 공격력 증가", label="공격 명중"),
        weaponOptionSchema(type=weaponOptionType.toggle, maxStack=1, description="보호막 존재 시 공격력 증가 효과가 100%증가", label="보호막"),
    ],
    "판정": [
        weaponOptionSchema(description="공격력 증가"),
        weaponOptionSchema(
            type=weaponOptionType.stack, maxStack=2, description="결정 반응으로 생성된 결정 조각 획득 시 약인 1스텍 획득. 약인 당 원소 전투 스킬 피해 증가", label="약인"
        ),
    ],
    "학도의 노트": [],
}
