"use client";

const ArtifactSetOptionCard = ({ val }: { val: any }): React.ReactElement => {
  // 여기서 모든 성유물 설정값을 받아온 다음에 setoption 처리를 시작하자.

  return <div className="bg-Fire">{val.name}</div>;
};

export default ArtifactSetOptionCard;
