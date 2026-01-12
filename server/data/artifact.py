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
    "조화로운 공상의 단편": [
        artifactSetOptionSchema(type=artifactSetOptionType.always, description="공격력 18% 증가", requiredParts=2),
        artifactSetOptionSchema(
            type=artifactSetOptionType.stack,
            description="생명의 계약의 수치가 증가 또는 감소 시, 캐릭터가 주는 피해가 18% 증가한다. 지속 시간: 6초, 최대 중첩수: 3회",
            maxStack=3,
            requiredParts=4,
            label="생명의 계약 변화",
        ),
    ],
    "지난날의 노래": [
        artifactSetOptionSchema(type=artifactSetOptionType.always, description="치유 보너스 15% 증가", requiredParts=2),
        artifactSetOptionSchema(
            type=artifactSetOptionType.stack,
            description="회복량에 비례하여 일반 공격, 강 공격, 낙하 공격, 원소 전투 스킬, 원소 폭발에 계수 추가. 최대 15000pt",
            maxStack=15000,
            requiredParts=4,
            label="회복량(pt)",
        ),
    ],
    "메아리숲의 야화": [
        artifactSetOptionSchema(type=artifactSetOptionType.always, description="공격력 18% 증가", requiredParts=2),
        artifactSetOptionSchema(
            type=artifactSetOptionType.toggle, description="원소 전투 스킬 발동 후 바위 원소 피해 보너스 20% 획득.", requiredParts=4, label="원소 전투 스킬 발동"
        ),
        artifactSetOptionSchema(
            type=artifactSetOptionType.toggle, description="결정 보호막 보유 시 바위 원소 피해 보너스 증가 효과 150% 증가", requiredParts=4, label="결정 보호막"
        ),
    ],
    "추억의 시메나와": [
        artifactSetOptionSchema(type=artifactSetOptionType.always, description="공격력 18% 증가", requiredParts=2),
        artifactSetOptionSchema(
            type=artifactSetOptionType.toggle, description="원소 전투 스킬 발동 후 일반 공격, 강공격, 낙하 공격으로 주는 피해가 증가", requiredParts=4, label="원소 전투 스킬 발동"
        ),
    ],
    "창백의 화염": [
        artifactSetOptionSchema(type=artifactSetOptionType.always, description="가하는 물리 피해+25%", requiredParts=2),
        artifactSetOptionSchema(
            type=artifactSetOptionType.stack,
            description="원소전투 스킬로 적을 명중하면 공격력이 9% 증가한다. 지속 시간: 7초, 최대 중첩수: 2회. 해당 효과는 0.3초마다 1회 발동되며, 2회 중첩 시 2세트의 효과가 100% 증가한다",
            requiredParts=4,
            maxStack=2,
            label="원소 전투 스킬 발동",
        ),
    ],
    "검투사의 피날레": [
        artifactSetOptionSchema(type=artifactSetOptionType.always, description="공격력 +18%", requiredParts=2),
        artifactSetOptionSchema(description="해당 성유물 세트를 장착한 캐릭터가 한손검, 양손검, 장병기를 사용 시 캐릭터의 일반 공격으로 주는 피해가 35% 증가한다", requiredParts=4),
    ],
    "도금된 꿈": [
        artifactSetOptionSchema(type=artifactSetOptionType.always, description="원소 마스터리 +80", requiredParts=2),
        artifactSetOptionSchema(
            type=artifactSetOptionType.stack,
            description="원소 반응 발동 후 8초 동안 파티 내 다른 캐릭터의 원소 유형에 따라 장착 캐릭터가 강화 효과를 받는다. 동일한 원소 타입의 캐릭터가 1명 존재할 때마다 공격력이 14% 증가",
            maxStack=3,
            requiredParts=4,
            label="동일 원소 파티원",
        ),
        artifactSetOptionSchema(
            type=artifactSetOptionType.stack,
            description="원소 반응 발동 후 8초 동안 파티 내 다른 캐릭터의 원소 유형에 따라 장착 캐릭터가 강화 효과를 받는다. 다른 원소 타입의 캐릭터가 1명 존재할 때마다 원소 마스터리가 50pt 증가",
            maxStack=3,
            requiredParts=4,
            label="다른 원소 파티원",
        ),
    ],
    "님프의 꿈": [
        artifactSetOptionSchema(type=artifactSetOptionType.always, description="물 원소 피해 보너스 15%", requiredParts=2),
        artifactSetOptionSchema(
            type=artifactSetOptionType.stack,
            description="일반 공격, 강공격, 낙하 공격, 원소전투 스킬 또는 원소폭발이 적에게 명중한 후, 8초 동안 지속되는 「거울 속 님프」 효과가 1스택 생성된다.  효과가 1/2/3스택 이상일 시, 공격력이 7%/16%/25% 증가하고 물 원소 피해 보너스가 4%/9%/15% 증가한다.",
            maxStack=3,
            requiredParts=4,
            label="거울 속 님프",
        ),
    ],
    "긴 밤의 맹세": [
        artifactSetOptionSchema(description="낙하 공격 피해 25% 증가", requiredParts=2),
        artifactSetOptionSchema(
            type=artifactSetOptionType.stack,
            description="장착 캐릭터의 낙하 공격/강공격/원소전투 스킬이 적에게 명중 후, 「영원한 광휘」를 1/2/2스택 획득한다. 해당 효과는 낙하 공격, 강공격 또는 원소전투 스킬로 1초마다 각각 최대 1회 발동된다. 「영원한 광휘」: 낙하공격으로 주는 피해가 15% 증가한다. 지속 시간: 6초, 최대 중첩수: 5스택, 스택마다 지속 시간은 독립적으로 계산한다",
            maxStack=5,
            requiredParts=4,
            label="영원한 광휘",
        ),
    ],
    "옛 왕실의 의식": [
        artifactSetOptionSchema(description="원소 폭발로 주는 피해 +20%", requiredParts=2),
        artifactSetOptionSchema(
            type=artifactSetOptionType.toggle,
            description="원소폭발 발동 후 파티 내 모든 캐릭터의 공격력이 20% 증가한다. 지속 시간: 12초. 해당 효과는 중첩되지 않는다",
            requiredParts=4,
            label="원소폭발 발동",
        ),
    ],
    "유구한 반암": [
        artifactSetOptionSchema(description="바위 원소 피해 보너스 +15%", requiredParts=2),
        artifactSetOptionSchema(
            type=artifactSetOptionType.toggle,
            description=(
                "결정 반응으로 만들어진 결정을 획득 시 파티 내 모든 캐릭터는 해당 원소 피해 보너스를 35% 획득한다. 지속 시간: 10초. "
                "이러한 효과로 1가지의 원소 피해 보너스만 획득할 수 있다"
            ),
            requiredParts=4,
            label="결정 획득",
        ),
    ],
    "달을 엮는 밤노래": [
        artifactSetOptionSchema(description="원소 충전 효율 20% 증가", requiredParts=2),
        artifactSetOptionSchema(
            type=artifactSetOptionType.select,
            selectList=["보름", "초승"],
            description="원소 피해를 줄 시, 8초 동안 지속되는 「월광·신앙」 효과를 획득한다: 파티의 달빛 징조가 초승/보름인 경우, 파티 내 모든 캐릭터의 원소 마스터리가 60pt/120pt 증가한다",
            requiredParts=4,
            label="월광·신앙",
        ),
        artifactSetOptionSchema(
            type=artifactSetOptionType.stack,
            maxStack=10,
            description="달빛 반응 피해 증가",
            requiredParts=4,
            label="월광 효과 수",
        ),
    ],
}
