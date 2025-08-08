"use client";
import { parseCalculatorData } from "@/lib/parseCalculatorData";
import { useCalculatorStore } from "@/store/useCalculatorStore";
import { zodResolver } from "@hookform/resolvers/zod";
import { useSearchParams } from "next/navigation";
import { useEffect } from "react";
import { useFieldArray, useForm } from "react-hook-form";
import { z } from "zod";

const calculatorFormSchema = z.object({
  level: z.number().min(1, { error: "캐릭터 레벨을 확인해주세요." }).max(90, {
    error: "캐릭터 레벨을 확인해주세요.",
  }),
  constellations: z.array(
    z.object({
      unlocked: z.boolean(),
      active: z.boolean(),
      stack: z.number(),
    }),
  ),
  activeSkill: z.array(
    z.object({
      level: z.number().max(10, { error: "스킬 레벨을 확인해주세요." }).min(1, { error: "스킬 레벨을 확인해주세요." }),
      active: z.boolean(),
      stack: z.number(),
    }),
  ),
  passiveSkill: z.array(
    z.object({
      unlocked: z.boolean(),
      active: z.boolean(),
      stack: z.number(),
    }),
  ),
  weapon: z.object({
    level: z.number().max(90, { error: "스킬 레벨을 확인해주세요." }).min(1, { error: "스킬 레벨을 확인해주세요." }),
    refinement: z.number().max(5, { error: "스킬 레벨을 확인해주세요." }).min(0, { error: "스킬 레벨을 확인해주세요." }),
    option: z.array(
      z.object({
        active: z.boolean(),
        stack: z.number(),
      }),
    ),
  }),
  artifact: z.object({
    parts: z.array(
      z.object({
        name: z.string(),
        setName: z.string(),
        type: z.string(),
        mainStat: z.record(z.string(), z.number()),
        subStat: z.array(z.record(z.string(), z.number())),
      }),
    ),
    setInfo: z.array(
      z.object({
        name: z.string(),
        option: z.array(
          z.object({
            active: z.boolean(),
            stack: z.number(),
          }),
        ),
      }),
    ),
  }),
});

const formSchema = z.object({
  data: z.array(calculatorFormSchema),
});

const CalculatorPage = (): React.ReactElement => {
  const { calculatorData, setCalculateData, setCharacterInfo } = useCalculatorStore();
  const searchParams = useSearchParams();
  searchParams.get("uid");

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      data: [],
    },
    mode: "onBlur",
  });
  const { fields, append, remove } = useFieldArray({
    name: "data",
    control: form.control,
  });

  useEffect(() => {
    const calculatorDataRaw = window.sessionStorage.getItem(`calculatorData`);
    if (calculatorDataRaw) {
      const resData = JSON.parse(calculatorDataRaw);
      resData.map((data: { info: object; result: object }) => append(parseCalculatorData<typeof data>(data)));

      return () => {
        form.reset();
      };
    }
  }, []);

  return (
    <div>
      <div>{searchParams.get("uid")}</div>
      {fields.map((field, index) => {
        // 캐릭터 카드 제작 부
        return <div key={`calculator-${index}`}>{JSON.stringify(field)}</div>;
      })}

      <p>여기가 경계서어언</p>
      {JSON.stringify(calculatorData)}
    </div>
  );
};

export default CalculatorPage;
export { calculatorFormSchema, formSchema };
