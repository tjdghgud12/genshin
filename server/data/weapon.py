# type = stack or toggle or aways, maxStack

weaponType = {
    "아모스의 활": [
        {"type": "always", "maxStack": 1, "description": "일반공격 및 강공격 피해 증가"},
        {
            "type": "stack",
            "maxStack": 5,
            "description": "일반공격과 강공격 화살이 발사된 후 0.1초가 지날 때마다 피해 증가",
        },
    ],
    "안개를 가르는 회광": [
        {"type": "always", "maxStack": 1, "description": "원소 피해 증가"},
        {"type": "stack", "maxStack": 3, "description": "무절의 문장 보유 개수 당 원소 피해 증가"},
    ],
    "용의 포효": [{"type": "toggle", "maxStack": 1, "description": "불, 번개 원소 피해 증가"}],
    "떠오르는 천일 밤의 꿈": [
        {"type": "stack", "maxStack": 3, "description": "동일 원소 타입 파티원 당 원소 마스터리 증가"},
        {"type": "stack", "maxStack": 3, "description": "다른 원소 타입 파티원 당 원소 피해 증가"},
    ],
    "예초의 번개": [
        {
            "type": "always",
            "maxStack": 1,
            "description": "원소 충전 효율이 100%를 초과할 경우, 초과된 부분의 28/35/42/49/56%만큼 공격력이 증가",
        },
        {"type": "toggle", "maxStack": 1, "description": "원소폭발 발동 후 12초 동안 원소 충전 효율 증가"},
    ],
    "호마의 지팡이": [
        {"type": "always", "maxStack": 1, "description": "HP 증가"},
        {"type": "always", "maxStack": 1, "description": "HP 최대치에 따라 공격력 증가"},
        {"type": "toggle", "maxStack": 1, "description": "체력 50% 미만 시 효과 강화"},
    ],
    "창백한 섬광": [
        {"type": "toggle", "maxStack": 1, "description": "원소 전투 스킬 발동 시 공격력 증가"},
        {"type": "toggle", "maxStack": 1, "description": "원소 에너지가 0이면, 공격력 및 치명타 피해 증가"},
    ],
    "맛의 지휘자": [
        {"type": "always", "maxStack": 1, "description": "공격력 증가"},
        {"type": "toggle", "maxStack": 1, "description": "대기 상태 시 공격력 증가"},
        {"type": "toggle", "maxStack": 1, "description": "치유 진행 시 공격력 증가"},
    ],
    "고요히 샘솟는 빛": [
        {"type": "stack", "maxStack": 3, "description": "현재 HP 변화 시 원소 전투 스킬 피해 증가"},
        {
            "type": "stack",
            "maxStack": 2,
            "description": "파티 내 다른 캐릭터의 현재 HP 변화 시 장착 캐릭터 HP 최대치 증가",
        },
    ],
    "별지기의 시선": [
        {"type": "always", "maxStack": 1, "description": "원소 마스터리 증가"},
        {
            "type": "toggle",
            "maxStack": 1,
            "description": "파티 내에 있는 필드 위 캐릭터가 자신과 가까운 범위 내의 적에게 주는 피해 증가",
        },
    ],
    "영원히 샘솟는 법전": [
        {"type": "always", "maxStack": 1, "description": "HP 증가"},
        {"type": "stack", "maxStack": 3, "description": "현재 HP 변화 시 강공격 피해 증가"},
    ],
    "타오르는 천 개의 태양": [
        {
            "type": "toggle",
            "maxStack": 1,
            "description": "원소 전투 스킬 또는 원소 폭발 발동 시 공격력 및 치명타 피해 증가",
        },
        {"type": "toggle", "maxStack": 1, "description": "밤혼 가호 상태에서는 효과 증가"},
    ],
}
