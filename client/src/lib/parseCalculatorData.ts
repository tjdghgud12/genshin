import { calculatorFormSchema } from "@/app/calculator/page";
import { z } from "zod";

type TCalculatorData = z.infer<typeof calculatorFormSchema>;

interface IuserSelectOption {
  level?: number;
  unlocked?: boolean;
  stack: number;
  active: boolean;
  option?: {
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
    level: data.level,
    constellations: data.constellations.map((constellation: IuserSelectOption) => ({
      unlocked: constellation.unlocked,
      stack: constellation.stack,
      active: constellation.active,
    })),
    activeSkill: data.activeSkill.map((skill: IuserSelectOption) => ({
      level: skill.level,
      active: skill.active,
      stack: skill.stack,
    })),
    passiveSkill: data.passiveSkill.map((skill: IuserSelectOption) => ({
      unlocked: skill.unlocked,
      active: skill.active,
      stack: skill.stack,
    })),
    weapon: {
      level: data.weapon.level,
      refinement: data.weapon.refinement,
      option: data.weapon.option.map((o: IuserSelectOption) => ({
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
      setInfo: data.artifact.setInfo.map((s: IuserSelectOption) => ({
        name: s.name,
        option: s.option
          ? s.option.map((o: { active: boolean; stack: number }) => {
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

// function parseCalculatorData<T extends object>(rawCalculatorData: T): ICalculatorData {
//   return calculatorFormSchema.parse(rawCalculatorData);
// }
