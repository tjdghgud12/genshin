import { fightPropLabels } from "@/lib/fightProps";
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

export { calculatorCharacterInfoSchema, calculatorFormSchema, createFloatSchema };
