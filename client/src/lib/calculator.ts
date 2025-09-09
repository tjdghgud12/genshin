import { fightPropLabels } from "@/lib/fightProps";
import { IdamageCalculationResult } from "@/types/calculatorType";
import { z } from "zod";

const createFloatSchema = (min?: number, max?: number, errorMessage?: string) => {
  return z.union([z.string(), z.number()]).pipe(
    z.transform((val, ctx): string | number => {
      if (typeof val === "string") {
        let errorFlag = false;
        const cleaned = val.replace(/\s/g, "").trim();
        if (!cleaned) errorFlag = true;
        if (!/^[0-9]*\.?[0-9]*$/.test(cleaned)) errorFlag = true;
        if (cleaned.split(".").length > 2) errorFlag = true;

        if (errorFlag && errorMessage !== undefined) {
          ctx.issues.push({
            code: "custom",
            message: errorMessage,
            input: val,
          });
          return min || 0;
        }

        return parseFloat(cleaned);
      }
      if (typeof val === "number") return val;
      return min || 0;
    }),
  );
};

const calculatorCharacterInfoSchema = z.object({
  raw: z.record(z.string(), z.any()),
  level: createFloatSchema(1, 90, "캐릭터 레벨을 확인해주세요."),
  constellations: z.array(
    z.object({
      unlocked: z.boolean(),
      options: z.array(
        z.object({
          active: z.boolean(),
          stack: createFloatSchema(1, 10, "스킬 레벨을 확인해주세요."),
        }),
      ),
    }),
  ),
  activeSkill: z.array(
    z.object({
      level: createFloatSchema(),
      options: z.array(
        z.object({
          active: z.boolean(),
          stack: createFloatSchema(),
        }),
      ),
    }),
  ),
  passiveSkill: z.array(
    z.object({
      unlocked: z.boolean(),
      options: z.array(
        z.object({
          active: z.boolean(),
          stack: createFloatSchema(),
        }),
      ),
    }),
  ),
  weapon: z.object({
    id: z.number(),
    name: z.string(),
    level: createFloatSchema(1, 90, "무기 레벨을 확인해주세요."),
    refinement: createFloatSchema(1, 5, "재련을 확인해주세요."),
    options: z.array(
      z.object({
        active: z.boolean(),
        stack: createFloatSchema(),
      }),
    ),
  }),
  artifact: z.object({
    parts: z.array(
      z.object({
        name: z.string(),
        setName: z.string(),
        type: z.string(),
        mainStat: z.record(z.string(), createFloatSchema()),
        subStat: z.array(z.record(z.string(), createFloatSchema())),
      }),
    ),
    setInfo: z.array(
      z.object({
        name: z.string(),
        options: z.array(
          z.object({
            active: z.boolean(),
            stack: createFloatSchema(),
          }),
        ),
      }),
    ),
  }),
});

const calculatorFormSchema = z.object({
  data: z.array(calculatorCharacterInfoSchema),
  additionalFightProp: z.object(Object.fromEntries(Object.keys(fightPropLabels).map((key) => [key, createFloatSchema()]))),
});

const calculatorLabel = {
  nomal: "일반 공격",
  charge: "강 공격",
  falling: "낙하 공격",
  elementalSkill: "원소 전투 스킬",
  elementalBurst: "원소 폭발",

  physical: "물리 피해",
  elemental: "원소 피해",

  Critical: "치명",
  NonCritical: "비치명",
  Additional: "추가 계수",

  melt: "융해",
  reverseMelt: "융해(역)",
  vaporize: "증발",
  reverseVaporize: "증발(역)",
  aggravate: "촉진",
  spread: "발산",
  overloaded: "과부하", // 과부하
  electroCharged: "감전", // 감전
  superconduct: "초전도", // 초전도
  shatter: "쇄빙", // 쇄빙
  bloom: "개화", // 개화 기대값
  hyperBloom: "만개", // 만개 기대값
  burgeon: "발화", // 발화 기대값
  burning: "연소", // 연소 기대값
  fireSwirl: "확산(불)", // 불확산
  waterSwirl: "확산(물)", // 물확산
  iceSwirl: "확산(얼음)", // 얼음확산
  elecSwirl: "확산(번개)", // 번개확산

  lunarCharged: "달감전", // 달감전 기대값
};

const getCalculationResultData = <T extends keyof IdamageCalculationResult>(obj: IdamageCalculationResult, key: T): IdamageCalculationResult[T] => obj[key];

export { calculatorCharacterInfoSchema, calculatorFormSchema, calculatorLabel, createFloatSchema, getCalculationResultData };
