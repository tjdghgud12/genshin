import { calculatorFormSchema } from "@/app/calculator/page";
import { z } from "zod";

type TCalculatorData = z.infer<typeof calculatorFormSchema>;

interface IuserSelectoptions {
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

const parseCalculatorData = <T extends { info: Record<string, any> }>(rawCalculatorData: T): TCalculatorData => {
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
      level: skill.level,
      options: skill.options.map((option) => ({ active: option.active, stack: option.stack })),
    })),
    passiveSkill: data.passiveSkill.map((skill: IuserSelectoptions) => ({
      unlocked: skill.unlocked,
      options: skill.options.map((option) => ({ active: option.active, stack: option.stack })),
    })),
    weapon: {
      name: data.weapon.name,
      level: data.weapon.level,
      refinement: data.weapon.refinement,
      options: data.weapon.option.map((o: IuserSelectoptions) => ({
        active: o.active,
        stack: o.stack,
      })),
    },
    artifact: {
      parts: data.artifact.parts.map((part: { name: string; setName: string; type: string; mainStat: { [key: string]: number }; subStat: { [key: string]: number }[] }) => ({
        name: part.name,
        setName: part.setName,
        type: part.type,
        mainStat: part.mainStat,
        subStat: part.subStat.map((s: { [key: string]: number }) => s),
      })),
      setInfo: data.artifact.setInfo.map((s: IuserSelectoptions) => ({
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

export { parseCalculatorData };
