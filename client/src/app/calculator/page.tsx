"use client";
import AdditionalFightProp from "@/app/calculator/components/AdditionalFightProp";
import CharacterSettingCard from "@/app/calculator/components/CharacterSettingCard";
import { Form } from "@/components/ui/form";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import api from "@/lib/axios";
import { calculatorCharacterInfoSchema, calculatorFormSchema as formSchema } from "@/lib/calculatorSchema";
import { fightPropLabels } from "@/lib/fightProps";
import { parseCharacterInfo } from "@/lib/parseCharacterInfo";
import { deepMergeAddOnly } from "@/lib/utils";
import { IdamageCalculationResult } from "@/types/globalType";
import { zodResolver } from "@hookform/resolvers/zod";
import Image from "next/image";
import React, { useEffect, useState } from "react";
import { SubmitHandler, useFieldArray, useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

const CalculatorPage = (): React.ReactElement => {
  const [selectedCharacter, setSelectedCharacter] = useState<string>("");
  const [totalCalculatorData, setTotalCalculatorData] = useState<{ info: z.infer<typeof calculatorCharacterInfoSchema>; result: IdamageCalculationResult }[]>([]);

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
      additionalFightProp: Object.fromEntries(Object.keys(fightPropLabels).map((key) => [key, 0])),
    },
    mode: "onBlur",
  });
  const { fields, append } = useFieldArray({
    name: "data",
    control: form.control,
  });

  const onSubmit: SubmitHandler<z.infer<typeof formSchema>> = (value, e): void => {
    const index: string | undefined = e ? (e.nativeEvent as SubmitEvent).submitter?.dataset.index : undefined;

    if (index) {
      const raw = value.data[Number(index)].raw;
      const additionalFightProp = Object.fromEntries(
        Object.entries(value.additionalFightProp).map(([key, value]) => [key, fightPropLabels[key].includes("%") ? Number(value) / 100 : value]),
      );
      const characterInfo = deepMergeAddOnly(value.data[Number(index)], raw);

      characterInfo.artifact.parts = characterInfo.artifact.parts.map((part) => {
        const [mainKey, mainValue] = Object.entries(part.mainStat)[0];
        const mainStatValue = fightPropLabels[mainKey].includes("%") ? Number(mainValue) / 100 : mainValue;

        const subStats = part.subStat.map((sub) => {
          const [subKey, subValue] = Object.entries(sub)[0];
          return { [subKey]: fightPropLabels[subKey].includes("%") ? Number(subValue) / 100 : subValue };
        });

        return { ...part, mainStat: { [mainKey]: mainStatValue }, subStat: subStats };
      });

      toast.promise(api.post(`/calculation`, { characterInfo: characterInfo, additionalFightProp }), {
        loading: "로딩 중",
        success: (res) => {
          console.log(res.data);
          return "데미지 연산을 완료하였습니다.";
        },
        error: (err) => {
          console.log(err);
          return "데미지 연산에 실패하였습니다.";
        },
      });
    }
  };

  useEffect(() => {
    const calculatorDataRaw = window.sessionStorage.getItem(`calculatorData`);
    if (calculatorDataRaw) {
      const parseData = JSON.parse(calculatorDataRaw);
      parseData.map((data: { info: object; result: object }) => append(parseCharacterInfo<typeof data>(data)));
      setTotalCalculatorData(parseData);
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
          <AdditionalFightProp form={form} />
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
                    <Image src={iconUrl} alt="" priority fill sizes="(max-width: 1200px) 5vw" />
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
