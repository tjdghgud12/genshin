from enum import Enum


class artifactSetOptionType(Enum):
    always = "always"
    toggle = "toggle"
    stack = "stack"


artifactSetOptions = {
    "그림자 사냥꾼": [
        {"type": artifactSetOptionType.always, "maxStack": 1, "description": "일반공격 및 강공격 피해 증가"},
        {
            "type": artifactSetOptionType.stack,
            "maxStack": 3,
            "description": "현재 체력 변화 시 치명타 확률 증가",
        },
    ],
    "얼음바람 속에서 길잃은 용사": [
        {"type": artifactSetOptionType.always, "maxStack": 1, "description": "얼음 원소 피해 증가"},
        {
            "type": artifactSetOptionType.stack,
            "maxStack": 2,
            "description": "얼음 원소 부착 적 공격 시 치명타 확률 증가. 빙결 상태 적 공격 시 치명타 확률 추가 증가",
        },
    ],
    "번개 같은 분노": [
        {"type": artifactSetOptionType.always, "maxStack": 1, "description": "번개 원소 피해 증가"},
        {
            "type": artifactSetOptionType.stack,
            "maxStack": 1,
            "description": "번개 관련 피해 계수 증가 및 번개 관련 반응 발동 시 원소 전투 스킬 재사용 대기시간 1초 감소",
        },
    ],
}
