from schemas.weapon import weaponOptionSchema, weaponOptionType

weaponInfo = {
    "아모스의 활": [
        weaponOptionSchema(description="일반공격 및 강공격 피해 증가"),
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=5, description="일반공격과 강공격 화살이 발사된 후 0.1초가 지날 때마다 피해 증가", label="경과 시간(0.1초)"),
    ],
    "녹슨 활": [
        weaponOptionSchema(description="일반 공격으로 주는 피해가 40/50/60/70/80% 증가"),
        weaponOptionSchema(description="강공격 피해 10%감소"),
    ],
    "비뢰의 고동": [
        weaponOptionSchema(description="공격력 증가"),
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=3, label="비뢰의 문장"),
    ],
    "페보니우스 활": [
        weaponOptionSchema(description="치명타 시 원소 입자 발생"),
    ],
    "약수": [
        weaponOptionSchema(description="HP 증가"),
        weaponOptionSchema(type=weaponOptionType.toggle, label="주변 적 존재"),
    ],
}
