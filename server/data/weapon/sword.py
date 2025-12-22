from schemas.weapon import weaponOptionSchema, weaponOptionType

weaponInfo = {
    "안개를 가르는 회광": [
        weaponOptionSchema(description="원소 피해 증가"),
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=3, description="무절의 문장 보유 개수 당 원소 피해 증가", label="무절의 문장"),
    ],
    "용의 포효": [
        weaponOptionSchema(type=weaponOptionType.toggle, description="불, 번개 원소 피해 증가", label="불 또는 번개 원소 부착"),
    ],
    "고요히 샘솟는 빛": [
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=3, description="현재 hp 변화 시 원소 전투 스킬 피해 증가", label="hp 변화 횟수(피해 증가)"),
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=2, description="파티 내 다른 캐릭터의 현재 hp 변화 시 장착 캐릭터 hp 최대치 증가", label="hp 변화 횟수(hp 증가)"),
    ],
    "창백한 섬광": [
        weaponOptionSchema(type=weaponOptionType.toggle, description="원소 전투 스킬 발동 시 공격력 증가", label="원소 전투 스킬 발동"),
        weaponOptionSchema(type=weaponOptionType.toggle, description="원소 에너지가 0이면, 공격력 및 치명타 피해 증가", label="원소 에너지 0"),
    ],
    "사면": [
        weaponOptionSchema(description="치명타 피해가 증가한다."),
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=3, description="생명의 계약 증가 시 캐릭터가 주는 피해 증가", label="생명의 계약 증가"),
    ],
    "아메노마 카게우치가타나": [
        weaponOptionSchema(
            description="원소전투 스킬 발동 후 계승의 씨앗을 1개 획득하고, 원소폭발 발동 후 보유 중인 계승의 씨앗이 모두 소모되며, 2초 후 소모된 계승의 씨앗의 개수에 따라 하나당 해당 캐릭터의 원소 에너지 회복"
        )
    ],
    "늑대 송곳니": [
        weaponOptionSchema(description="원소전투 스킬과 원소폭발로 주는 피해 증가"),
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=4, label="원소 전투 스킬 명중"),
        weaponOptionSchema(type=weaponOptionType.stack, maxStack=4, label="원소 폭발 명중"),
    ],
    "잎을 가르는 빛": [
        weaponOptionSchema(description="치명타 확률 증가"),
        weaponOptionSchema(type=weaponOptionType.toggle, label="가지치기"),
    ],
    "페보니우스 검": [weaponOptionSchema(description="치명타 시 원소 입자 발생")],
    "바위산을 맴도는 노래": [
        weaponOptionSchema(
            description=(
                "일반 공격 또는 낙하 공격으로 적 명중 후, 「영광의 꽃노래」를 획득한다: 방어력이 8/10/12/14/16% 증가하고,"
                "모든 원소 피해 보너스가 10/12.5/15/17.5/20% 증가한다."
                "지속 시간: 6초, 최대 중첩수: 2회"
                "해당 효과 2스택 중첩 또는 2스택의 지속 시간 갱신 시,"
                "장착 캐릭터의 방어력에 기반해 1000pt마다 파티 내 주변에 있는 모든 캐릭터의 모든 원소 피해 보너스가 8/10/12/14/16% 증가하고,"
                "최대 25.6/32/38.4/44.8/51.2%까지 증가한다. 지속 시간: 15초"
            ),
            type=weaponOptionType.stack,
            maxStack=2,
            label="영광의 꽃노래",
        )
    ],
    "칠흑검": [
        weaponOptionSchema(
            description=(
                "일반 공격과 강공격으로 주는 피해가 20/25/30/35/40% 증가한다."
                "또한 일반 공격과 강공격이 치명타 시 공격력의 60/70/80/90/100%에 해당하는 HP를 회복한다."
                "해당 효과는 5초마다 1번 발동한다"
            )
        )
    ],
}
