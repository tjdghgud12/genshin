from schemas.weapon import weaponOptionSchema, weaponOptionType

weaponInfo = {
    "떠오르는 천일 밤의 꿈": [
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=3, description="동일 원소 타입 파티원 당 원소 마스터리 증가", label="동일 원소 파티원"),
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=3, description="다른 원소 타입 파티원 당 원소 피해 증가", label="다른 원소 파티원"),
    ],
    "별지기의 시선": [
        weaponOptionSchema(description="원소 마스터리 증가"),
        weaponOptionSchema(type=weaponOptionType.toggle, description="파티 내에 있는 필드 위 캐릭터가 자신과 가까운 범위 내의 적에게 주는 피해 증가", label="보호막"),
    ],
    "영원히 샘솟는 법전": [
        weaponOptionSchema(description="hp 증가"),
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=3, description="현재 hp 변화 시 강공격 피해 증가", label="hp 변화 횟수"),
    ],
    "학도의 노트": [],
    "카구라의 진의": [weaponOptionSchema(type=weaponOptionType.stack, maxStack=3, label="카구라의 춤")],
    "음유시인의 악장": [weaponOptionSchema(type=weaponOptionType.select, selectList=[None, "서장(공격력)", "영탄곡(모든 원소 피해)", "간주곡(원소 마스터리)"], label="테마송")],
    "사풍 원서": [weaponOptionSchema(type=weaponOptionType.stack, maxStack=4, label="원소 피해 보너스")],
    "제사의 옥": [weaponOptionSchema(type=weaponOptionType.toggle, label="대기 상태 5초 초과")],
    "드래곤 슬레이어 영웅담": [],
    "제례의 악장": [],
    "진실의 함": [
        weaponOptionSchema(description="치명타 확률 증가"),
        weaponOptionSchema(
            type=weaponOptionType.toggle,
            description=" 원소전투 스킬 발동 시, 장착 캐릭터가 「거짓의 비밀」 효과를 획득한다: 원소 마스터리가 80/100/120/140/160pt 증가한다",
            label="거짓의 비밀",
        ),
        weaponOptionSchema(
            type=weaponOptionType.toggle,
            description="착 캐릭터가 적에게 달 개화 반응 피해를 줄 시, 장착 캐릭터가 「진실의 달」 효과를 획득한다: 치명타 피해가 24%/30%/36%/42%/48% 증가한다",
            label="진실의 달",
        ),
    ],
}
