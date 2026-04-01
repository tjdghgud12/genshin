from schemas.weapon import weaponOptionSchema, weaponOptionType

weaponInfo = {
    "타오르는 천 개의 태양": [
        weaponOptionSchema(type=weaponOptionType.toggle, description="원소 전투 스킬 또는 원소 폭발 발동 시 공격력 및 치명타 피해 증가(불빛)", label="불빛"),
        weaponOptionSchema(type=weaponOptionType.toggle, description="밤혼 가호 상태에서는 불빛 효과 강화", label="밤혼 가호"),
    ],
    "무공의 검": [
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=5, description="공격 명중 시 공격력 증가", label="공격 명중"),
        weaponOptionSchema(type=weaponOptionType.toggle, maxStack=1, description="보호막 존재 시 공격력 증가 효과가 100%증가", label="보호막"),
    ],
    "송뢰가 울릴 무렵": [weaponOptionSchema(description="공격력 증가"), weaponOptionSchema(type=weaponOptionType.toggle, label="천년의 대악장·깃발의 노래")],
    "늑대의 말로": [weaponOptionSchema(description="공격력 증가"), weaponOptionSchema(type=weaponOptionType.toggle, label="HP 30% 미만 적 명중")],
    "판정": [
        weaponOptionSchema(description="공격력 증가"),
        weaponOptionSchema(
            type=weaponOptionType.stack, maxStack=2, description="결정 반응으로 생성된 결정 조각 획득 시 약인 1스텍 획득. 약인 당 원소 전투 스킬 피해 증가", label="약인"
        ),
    ],
}
