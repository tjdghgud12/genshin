from schemas.artifact import artifactSetOptionSchema, artifactSetOptionType


artifactSetOptions = {
    "그림자 사냥꾼": [
        artifactSetOptionSchema(description="일반공격 및 강공격 피해 증가", requiredParts=2),
        artifactSetOptionSchema(type=artifactSetOptionType.stack, maxStack=3, description="현재 체력 변화 시 치명타 확률 증가", label="체력 변화", requiredParts=4),
    ],
    "얼음바람 속에서 길잃은 용사": [
        artifactSetOptionSchema(description="얼음 원소 피해 증가", requiredParts=2),
        artifactSetOptionSchema(
            type=artifactSetOptionType.toggle,
            description="얼음 원소 부착 적 공격 시 치명타 확률 증가",
            requiredParts=4,
            label="얼음 원소 부착",
        ),
        artifactSetOptionSchema(
            type=artifactSetOptionType.toggle,
            description="빙결 상태 적 공격 시 치명타 확률 추가 증가",
            requiredParts=4,
            label="빙결",
        ),
    ],
    "번개 같은 분노": [
        artifactSetOptionSchema(description="번개 원소 피해 증가", requiredParts=2),
        artifactSetOptionSchema(description="번개 관련 피해 계수 증가 및 번개 관련 반응 발동 시 원소 전투 스킬 재사용 대기시간 1초 감소", requiredParts=4),
    ],
    "숲의 기억": [
        artifactSetOptionSchema(description="풀 원소 피해 증가", requiredParts=2),
        artifactSetOptionSchema(
            type=artifactSetOptionType.toggle,
            description="원소 전투 스킬 또는 원소 폭발에 명중된 적은 풀 원소 내성 감소",
            label="풀 원소 내성 감소",
            requiredParts=4,
        ),
    ],
    "절연의 기치": [
        artifactSetOptionSchema(description="원소 충전 효율 증가", requiredParts=2),
        artifactSetOptionSchema(description="원소 충전 효율의 25%만큼 원소 폭발 피해 증가", requiredParts=4),
    ],
    "불타오르는 화염의 마녀": [
        artifactSetOptionSchema(description="불 원소 피해 증가", requiredParts=2),
        artifactSetOptionSchema(
            type=artifactSetOptionType.stack,
            maxStack=3,
            description="과부하, 연소, 발화 반응 피해 40% 증가 + 융해 반응 보너스 계수 15%증가. 원소 전투 스킬 사용 시 2세트 옵션 50%씩 상승",
            requiredParts=4,
            label="원소 전투 스킬 사용",
        ),
    ],
    "황금 극단": [
        artifactSetOptionSchema(description="원소 전투 스킬 피해 증가", requiredParts=2),
        artifactSetOptionSchema(description="원소 전투 스킬 피해 증가", requiredParts=4),
        artifactSetOptionSchema(type=artifactSetOptionType.toggle, description="대기 상태일 때 원소 전투 스킬 피해 추가 증가", requiredParts=4, label="대기 상태"),
    ],
    "깊은 회랑의 피날레": [
        artifactSetOptionSchema(description="얼음 원소 피해 증가", requiredParts=2),
        artifactSetOptionSchema(
            type=artifactSetOptionType.toggle, description="원소 게이지가 0pt일 시 일반 공격 또는 원소 폭발로 주는 피해 증가", requiredParts=4, label="원소 게이지 0pt"
        ),
    ],
    "잿더미성 용사의 두루마리": [
        artifactSetOptionSchema(description="주변 파티 내 캐릭터가 밤혼 발산 발동 시, 장착 캐릭터 원소 에너지 회복", requiredParts=2),
        artifactSetOptionSchema(
            type=artifactSetOptionType.toggle,
            description="장착캐릭터가 원소 반응 발동 시 파티 내 모든 캐릭터의 해당 원소 반응과 관련된 피해 12% 증가",
            requiredParts=4,
            label="원소 반응",
        ),
        artifactSetOptionSchema(
            type=artifactSetOptionType.toggle,
            description="장착캐릭터가 원소 반응 발동 시 장착 캐릭터가 밤혼 가호 상태인 경우 파티 내 모든 캐릭터의 해당 원소 반응과 관련된 피해 28% 증가",
            requiredParts=4,
            label="밤혼",
        ),
    ],
    "흑요석 비전": [
        artifactSetOptionSchema(
            type=artifactSetOptionType.toggle, description="밤혼 가호 상태의 장착 캐릭터가 필드 위에 있을 시 주는 피해 15% 증가", requiredParts=2, label="밤혼"
        ),
        artifactSetOptionSchema(
            type=artifactSetOptionType.toggle, description="장착 캐릭터가 필드 위에서 밤혼을 1pt 소모한 후 치명타 확률이 40% 증가", requiredParts=4, label="밤혼 소모"
        ),
    ],
}
