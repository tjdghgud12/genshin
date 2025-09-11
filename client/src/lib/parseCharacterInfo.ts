import { calculatorCharacterInfoSchema } from "@/lib/calculator";
import { z } from "zod";
import { fightPropLabels } from "./fightProps";

type TCalculatorData = z.infer<typeof calculatorCharacterInfoSchema>;

interface IuserSelectoptions {
  id: number;
  level?: number;
  unlocked?: boolean;
  options: {
    level?: number;
    unlocked?: boolean;
    stack: number;
    active: boolean;
  }[];
  [key: string]: unknown;
}

const parseCharacterInfo = <T extends { info: Record<string, any> }>(rawCalculatorData: T): TCalculatorData => {
  const data = rawCalculatorData.info;
  return {
    raw: data,
    level: data.level,
    constellations: data.constellations.map((constellation: IuserSelectoptions) => ({
      unlocked: constellation.unlocked,
      options: constellation.options.map((o) => ({
        stack: o.stack,
        active: o.active,
      })),
    })),
    activeSkill: data.activeSkill.map((skill: IuserSelectoptions) => ({
      level: (skill.level as number) > 10 ? 10 : skill.level, // 돌파에 따른 스킬렙 증가는 별도로 back에서 연산하기 위해 최대값을 10으로 제한
      options: skill.options.map((option) => ({ active: option.active, stack: option.stack })),
    })),
    passiveSkill: data.passiveSkill.map((skill: IuserSelectoptions) => ({
      unlocked: skill.unlocked,
      options: skill.options.map((option) => ({ active: option.active, stack: option.stack })),
    })),
    weapon: {
      id: data.weapon.id,
      name: data.weapon.name,
      level: data.weapon.level,
      refinement: data.weapon.refinement,
      options: data.weapon.options.map((o: IuserSelectoptions) => ({
        active: o.active,
        stack: o.stack,
      })),
    },
    artifact: {
      parts: data.artifact.parts.map((part: { setName: string; type: string; mainStat: { [key: string]: number }; subStat: { [key: string]: number }[] }) => ({
        setName: part.setName,
        type: part.type,
        mainStat: Object.fromEntries(Object.entries(part.mainStat).map(([k, v]) => [k, fightPropLabels[k].includes("%") ? (v * 100).toFixed(2) : v])),
        subStat: part.subStat.map((s: { [key: string]: number }) =>
          Object.fromEntries(Object.entries(s).map(([k, v]) => [k, fightPropLabels[k].includes("%") ? (v * 100).toFixed(2) : v])),
        ),
      })),
      setInfo: data.artifact.setInfo.map((s: IuserSelectoptions) => ({
        id: s.id,
        name: s.name,
        options: s.options
          ? s.options.map((o: { active: boolean; stack: number }) => {
              return {
                active: o.active,
                stack: o.stack,
              };
            })
          : [],
      })),
    },
  };
};

export { parseCharacterInfo };
