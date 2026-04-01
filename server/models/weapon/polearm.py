from schemas.weapon import weaponOptionSchema, weaponOptionType

weaponInfo = {
    "예초의 번개": [
        weaponOptionSchema(type=weaponOptionType.toggle, description="원소폭발 발동 후 12초 동안 원소 충전 효율 증가", label="원소 폭발"),
        weaponOptionSchema(description="원소 충전 효율이 100%를 초과할 경우, 초과된 부분의 28/35/42/49/56%만큼 공격력이 증가"),
    ],
    "호마의 지팡이": [
        weaponOptionSchema(description="hp 20% 증가"),
        weaponOptionSchema(description="hp 최대치에 따라 공격력 증가"),
        weaponOptionSchema(type=weaponOptionType.toggle, description="체력 50% 미만 시 효과 강화", label="체력 50% 미만"),
    ],
    "맛의 지휘자": [
        weaponOptionSchema(description="공격력 증가"),
        weaponOptionSchema(type=weaponOptionType.toggle, description="대기 상태 시 공격력 증가", label="대기 상태"),
        weaponOptionSchema(type=weaponOptionType.toggle, description="치유 진행 시 공격력 증가", label="치유 진행"),
    ],
    "붉은 달의 형상": [
        weaponOptionSchema(type=weaponOptionType.toggle, maxStack=3, description="생명의 계약 보유 시 캐릭터가 주는 피해가 증가한다", label="생명의 계약 보유"),
        weaponOptionSchema(
            type=weaponOptionType.toggle, maxStack=3, description="생명의 계약이 HP최대치의 30% 이상일 시 캐릭터가 주는 피해가 증가한다", label="생명의 계약 최대 HP 30% 이상"
        ),
    ],
    "식재": [
        weaponOptionSchema(description="모든 원소 피해 증가"),
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=6, label="원돈"),
        weaponOptionSchema(type=weaponOptionType.toggle, label="대기 상태"),
    ],
    "화박연": [weaponOptionSchema(type=weaponOptionType.stack, maxStack=7, label="적 명중")],
    "결투의 창": [weaponOptionSchema(type=weaponOptionType.toggle, label="적 2기 이상")],
    "페보니우스 장창": [weaponOptionSchema(description="치명타 시 원소 입자 발생")],
    "「어획」": [weaponOptionSchema(description="원소폭발로 주는 피해가 16/20/24/28/32% 증가하고, 원소폭발의 치명타 확률이 6/7.5/9/10.5/12% 증가한다")],
}
