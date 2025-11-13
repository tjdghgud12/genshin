import { calculatorCharacterInfoSchema } from "@/lib/calculator";
import { IUidSearchResult } from "@/types/calculatorType";
import { z } from "zod";
import { fightPropLabels } from "./fightProps";

export type TCalculatorData = z.infer<typeof calculatorCharacterInfoSchema>;

const parseCharacterInfo = (rawCalculatorData: IUidSearchResult): TCalculatorData => {
  const data = rawCalculatorData.characterInfo;
  return {
    level: data.level,
    constellations: data.constellations.map((constellation) => ({
      unlocked: constellation.unlocked ?? false,
      options: constellation.options.map((o) => ({
        stack: o.stack,
        active: o.active,
      })),
    })),
    activeSkill: data.activeSkill.map((skill) => ({
      level: (skill.level as number) > 10 ? 10 : skill.level, // 돌파에 따른 스킬렙 증가는 별도로 back에서 연산하기 위해 최대값을 10으로 제한
      options: skill.options.map((option) => ({ active: option.active, stack: option.stack })),
    })),
    passiveSkill: data.passiveSkill.map((skill) => ({
      unlocked: skill.unlocked,
      options: skill.options.map((option) => ({ active: option.active, stack: option.stack })),
    })),

    weapon: {
      id: data.weapon.id,
      name: data.weapon.name,
      type: data.weapon.type,
      level: data.weapon.level,
      refinement: data.weapon.refinement,
      options: data.weapon.options.map((o) => ({
        active: o.active,
        stack: o.stack,
        select: o.select,
        maxStack: o.maxStack,
        type: o.type,
        selectList: o.selectList,
        description: o.description,
        label: o.label,
      })),
    },
    artifact: {
      parts: data.artifact.parts.map((part) => ({
        setName: part.setName,
        type: part.type,
        mainStat: Object.fromEntries(Object.entries(part.mainStat).map(([k, v]) => [k, fightPropLabels[k].includes("%") ? (v * 100).toFixed(2) : v])),
        subStat: part.subStat.map((s) => Object.fromEntries(Object.entries(s).map(([k, v]) => [k, fightPropLabels[k].includes("%") ? (v * 100).toFixed(2) : v]))),
      })),
      setInfo: data.artifact.setInfo.map((s) => ({
        id: s.id,
        name: s.name,
        numberOfParts: s.numberOfParts,
        options: s.options.map((o) => {
          return {
            requiredParts: o.requiredParts,
            active: o.active,
            stack: o.stack,
            maxStack: o.maxStack,
            type: o.type,
            selectList: o.selectList,
            description: o.description,
            label: o.label,
          };
        }),
      })),
    },
  };
};

export { parseCharacterInfo };
