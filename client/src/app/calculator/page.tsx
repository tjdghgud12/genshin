"use client";
import AdditionalFightProp from "@/app/calculator/components/AdditionalFightProp";
import CharacterSettingCard from "@/app/calculator/components/CharacterSettingCard";
import { Form } from "@/components/ui/form";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { parseCalculatorData } from "@/lib/parseCalculatorData";
import { zodResolver } from "@hookform/resolvers/zod";
// import Image from "next/image";
import React, { useEffect, useState } from "react";
import { useFieldArray, useForm } from "react-hook-form";
import { toast } from "sonner";
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

const calculatorFormSchema = z.object({
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

const formSchema = z.object({
  data: z.array(calculatorFormSchema),
});

const CalculatorPage = (): React.ReactElement => {
  const [selectedCharacter, setSelectedCharacter] = useState<string>("");

  const elementBgColors: Record<string, string> = {
    Fire: `bg-Fire`,
    Water: `bg-Water`,
    Wind: `bg-Wind`,
    Electric: `bg-Electric`,
    Ice: `bg-Ice`,
    Rock: `bg-Rock`,
    Grass: `bg-Grass`,
  };

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      data: [],
    },
    mode: "onBlur",
  });
  const { fields, append } = useFieldArray({
    name: "data",
    control: form.control,
  });

  const onSubmit = (value: z.infer<typeof formSchema>): void => {
    console.log(value);
  };

  useEffect(() => {
    const calculatorDataRaw = window.sessionStorage.getItem(`calculatorData`);
    if (calculatorDataRaw) {
      const parseData = JSON.parse(calculatorDataRaw);
      parseData.map((data: { info: object; result: object }) => append(parseCalculatorData<typeof data>(data)));
      setSelectedCharacter(parseData[0].info.name);
    }

    return (): void => {
      form.reset();
    };
  }, [append, form]);

  return (
    <div>
      <Form {...form}>
        <form id="page form" onSubmit={form.handleSubmit(onSubmit, (err) => toast.error(JSON.stringify(err)))} className="w-full mx-auto">
          <AdditionalFightProp />
          <Tabs value={selectedCharacter} onValueChange={setSelectedCharacter} className="w-[90%] mx-auto gap-0">
            <TabsList className="w-full h-fit justify-around pt-3 px-3 rounded-2xl mx-auto">
              {fields.map((item, i) => {
                const rawInfo = item.raw;
                const iconUrl = rawInfo.icon.front;
                const name = rawInfo.name;

                return (
                  <TabsTrigger
                    key={`calculator-tab-trigger-${i}`}
                    className={`w-[5vw] h-[5vw] min-w-20 min-h-20 relative overflow-hidden flex-none border-[3px] border-stone-300 ${elementBgColors[rawInfo.element]} rounded-full mx-1 data-[state=active]:border-lime-400 hover:border-lime-400 data-[state=active]:${elementBgColors[rawInfo.element]}`}
                    value={name}
                  >
                    {/* <Image src={iconUrl} alt="" priority fill sizes="(max-width: 1200px) 5vw" /> */}
                    <p>{name.slice(0, 1)}</p>
                  </TabsTrigger>
                );
              })}
            </TabsList>
            {fields.map((item, index) => {
              const rawInfo = item.raw;
              const name = rawInfo.name;
              return (
                <TabsContent key={`calculator-tab-content-${index}`} className={`w-full h-fit`} value={name}>
                  <CharacterSettingCard form={form} item={item} index={index} />
                </TabsContent>
              );
            })}
          </Tabs>
        </form>
      </Form>
    </div>
  );
};

export default CalculatorPage;
export { calculatorFormSchema, formSchema };
