from dataclasses import dataclass
from enum import Enum


class weaponOptionType(Enum):
    always = "always"
    toggle = "toggle"
    stack = "stack"


@dataclass
class weaponDataType:
    type: weaponOptionType = weaponOptionType.always
    maxStack: int = 1
    description: str = ""
    label: str = ""


ambrWeaponCurve: dict[str, dict] = {}

weaponInfo = {
    "아모스의 활": [
        weaponDataType(description="일반공격 및 강공격 피해 증가"),
        weaponDataType(type=weaponOptionType.stack, maxStack=5, description="일반공격과 강공격 화살이 발사된 후 0.1초가 지날 때마다 피해 증가", label="경과 시간(0.1초)"),
    ],
    "안개를 가르는 회광": [
        weaponDataType(description="원소 피해 증가"),
        weaponDataType(type=weaponOptionType.stack, maxStack=3, description="무절의 문장 보유 개수 당 원소 피해 증가", label="무절의 문장"),
    ],
    "용의 포효": [
        weaponDataType(type=weaponOptionType.toggle, description="불, 번개 원소 피해 증가", label="불 또는 번개 원소 부착"),
    ],
    "떠오르는 천일 밤의 꿈": [
        weaponDataType(type=weaponOptionType.stack, maxStack=3, description="동일 원소 타입 파티원 당 원소 마스터리 증가", label="동일 원소 파티원"),
        weaponDataType(type=weaponOptionType.stack, maxStack=3, description="다른 원소 타입 파티원 당 원소 피해 증가", label="다른 원소 파티원"),
    ],
    "예초의 번개": [
        weaponDataType(type=weaponOptionType.toggle, description="원소폭발 발동 후 12초 동안 원소 충전 효율 증가", label="원소 폭발"),
        weaponDataType(description="원소 충전 효율이 100%를 초과할 경우, 초과된 부분의 28/35/42/49/56%만큼 공격력이 증가"),
    ],
    "호마의 지팡이": [
        weaponDataType(description="hp 20% 증가"),
        weaponDataType(description="hp 최대치에 따라 공격력 증가"),
        weaponDataType(type=weaponOptionType.toggle, description="체력 50% 미만 시 효과 강화", label="체력 50% 미만"),
    ],
    "창백한 섬광": [
        weaponDataType(type=weaponOptionType.toggle, description="원소 전투 스킬 발동 시 공격력 증가", label="원소 전투 스킬 발동"),
        weaponDataType(type=weaponOptionType.toggle, description="원소 에너지가 0이면, 공격력 및 치명타 피해 증가", label="원소 에너지 0"),
    ],
    "맛의 지휘자": [
        weaponDataType(description="공격력 증가"),
        weaponDataType(type=weaponOptionType.toggle, description="대기 상태 시 공격력 증가", label="대기 상태"),
        weaponDataType(type=weaponOptionType.toggle, description="치유 진행 시 공격력 증가", label="치유 진행"),
    ],
    "고요히 샘솟는 빛": [
        weaponDataType(type=weaponOptionType.stack, maxStack=3, description="현재 hp 변화 시 원소 전투 스킬 피해 증가", label="hp 변화 횟수"),
        weaponDataType(type=weaponOptionType.stack, maxStack=2, description="파티 내 다른 캐릭터의 현재 hp 변화 시 장착 캐릭터 hp 최대치 증가", label="hp 변화 횟수"),
    ],
    "별지기의 시선": [
        weaponDataType(description="원소 마스터리 증가"),
        weaponDataType(type=weaponOptionType.toggle, description="파티 내에 있는 필드 위 캐릭터가 자신과 가까운 범위 내의 적에게 주는 피해 증가", label="보호막"),
    ],
    "영원히 샘솟는 법전": [
        weaponDataType(description="hp 증가"),
        weaponDataType(type=weaponOptionType.stack, maxStack=3, description="현재 hp 변화 시 강공격 피해 증가", label="hp 변화 횟수"),
    ],
    "타오르는 천 개의 태양": [
        weaponDataType(type=weaponOptionType.toggle, description="원소 전투 스킬 또는 원소 폭발 발동 시 공격력 및 치명타 피해 증가(불빛)", label="불빛"),
        weaponDataType(type=weaponOptionType.toggle, description="밤혼 가호 상태에서는 불빛 효과 강화"),
    ],
    "학도의 노트": [],
}
