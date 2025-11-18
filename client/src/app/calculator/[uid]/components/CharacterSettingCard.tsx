"use client";

import AdditionalFightProp from "@/app/calculator/[uid]/components/AdditionalFightProp";
import { ArtifactPartCard, ArtifactSetOptionCard } from "@/app/calculator/[uid]/components/ArtifactCard";
import DamageResultCard from "@/app/calculator/[uid]/components/DamageResultCard";
import WeaponSettingCard from "@/app/calculator/[uid]/components/WeaponSettingCard";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Card, CardContent } from "@/components/ui/card";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import api from "@/lib/axios";
import { calculatorCharacterInfoSchema, calculatorFormSchema } from "@/lib/calculator";
import { fightPropLabels } from "@/lib/fightProps";
import { parseCharacterInfo } from "@/lib/parseCharacterInfo";
import { deepMergeAddOnly, inputNumberWithSpace } from "@/lib/utils";
import { IArtifactSetsInfoStore, useArtifactSetsInfoStore } from "@/store/artifactStore";
import { IdamageCalculationResult, IUidSearchResult } from "@/types/calculatorType";
import { zodResolver } from "@hookform/resolvers/zod";
import { AxiosResponse } from "axios";
import { motion } from "framer-motion";
import { Calculator } from "lucide-react";
import Image from "next/image";
import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

type TArtifactSetInfo = z.infer<typeof calculatorCharacterInfoSchema>["artifact"]["setInfo"][number];
type TArtifactPartInfo = z.infer<typeof calculatorCharacterInfoSchema>["artifact"]["parts"][number];

const CharacterSettingCard = ({ character }: { character: IUidSearchResult }): React.ReactElement => {
  const [infoTab, setInfoTab] = useState<string>("overView");
  const [damageResult, setDamageResult] = useState<IdamageCalculationResult>(character.damage);
  const artifactSets = useArtifactSetsInfoStore((state: IArtifactSetsInfoStore) => state.artifactSets);
  const info = character.characterInfo;
  const element = character.characterInfo.element;
  const elementColors: Record<string, Record<string, string>> = {
    Fire: { bg: `bg-Fire`, shadow: "shadow-shadow-Fire", gradient: "from-Fire to-Fire/0" },
    Water: { bg: `bg-Water`, shadow: "shadow-shadow-Water", gradient: "from-Water to-Water/0" },
    Wind: { bg: `bg-Wind`, shadow: "shadow-shadow-Wind", gradient: "from-Wind to-Wind/0" },
    Electric: { bg: `bg-Electric`, shadow: "shadow-shadow-Electric", gradient: "from-Electric to-Electric/0" },
    Ice: { bg: `bg-Ice`, shadow: "shadow-shadow-Ice", gradient: "from-Ice to-Ice/0" },
    Rock: { bg: `bg-Rock`, shadow: "shadow-shadow-Rock", gradient: "from-Rock to-Rock/0" },
    Grass: { bg: `bg-Grass`, shadow: "shadow-shadow-Grass", gradient: "from-Grass to-Grass/0" },
  };
  const elementAddHurtKey: Record<string, Record<string, string>> = {
    Fire: { label: "불", key: "FIGHT_PROP_FIRE_ADD_HURT" },
    Water: { label: "물", key: "FIGHT_PROP_WATER_ADD_HURT" },
    Wind: { label: "바람", key: "FIGHT_PROP_WIND_ADD_HURT" },
    Electric: { label: "번개", key: "FIGHT_PROP_ELEC_ADD_HURT" },
    Ice: { label: "얼음", key: "FIGHT_PROP_ICE_ADD_HURT" },
    Rock: { label: "바위", key: "FIGHT_PROP_ROCK_ADD_HURT" },
    Grass: { label: "풀", key: "FIGHT_PROP_GRASS_ADD_HURT" },
  };

  const form = useForm<z.infer<typeof calculatorFormSchema>>({
    resolver: zodResolver(calculatorFormSchema),
    defaultValues: {
      data: parseCharacterInfo(character),
      additionalFightProp: Object.fromEntries(Object.keys(fightPropLabels).map((key) => [key, 0])),
    },
  });

  const getArtifactSetInfo = (parts: TArtifactPartInfo[]): TArtifactSetInfo[] => {
    const setList = new Set(parts.map((part) => part.setName));
    return [...setList]
      .filter((setName: string) => {
        const numberOfParts = parts.filter((part) => part.setName === setName).length;
        return numberOfParts >= 2;
      })
      .map((setName) => {
        const numberOfParts = parts.filter((part) => part.setName === setName).length;
        const options = artifactSets[setName].options.map((o) => ({ ...o, active: true, stack: o.maxStack }));
        return { name: setName, options: options.filter((o) => o.requiredParts <= numberOfParts), numberOfParts: numberOfParts };
      });
  };

  const formatterTotalFightProp = (v: number, isPercent = false, useFix: boolean): string => {
    const data = isPercent ? v * 100 : v;
    return useFix ? data.toFixed(2) : Math.round(data).toString();
  };

  const onSubmit = (value: z.infer<typeof calculatorFormSchema>): void => {
    const raw = character.characterInfo;
    const additionalFightProp = Object.fromEntries(
      Object.entries(value.additionalFightProp).map(([key, value]) => [key, fightPropLabels[key].includes("%") ? Number(value) / 100 : value]),
    );
    const characterInfo = deepMergeAddOnly(value.data, raw);

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
      success: (res: AxiosResponse<IUidSearchResult>) => {
        form.reset({ data: parseCharacterInfo(res.data), additionalFightProp: form.getValues("additionalFightProp") });
        setDamageResult(res.data.damage);
        return "데미지 연산을 완료하였습니다.";
      },
      error: (_err) => {
        return "데미지 연산에 실패하였습니다.";
      },
    });
  };

  return (
    <Tabs className="flex-row gap-0" orientation="vertical" defaultValue={"overView"} onValueChange={(val) => setInfoTab(val)}>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className={`w-full flex overflow-hidden`}>
          <AdditionalFightProp form={form} />
          <motion.button
            className="fixed bottom-24 right-6 w-14 h-14 rounded-full bg-gray-700 flex items-center justify-center text-white shadow-xl overflow-hidden z-50 group hover:gap-3"
            whileHover={{ width: 250 }}
            transition={{ type: "spring", stiffness: 300, damping: 20 }}
            type="submit"
          >
            <Calculator className="w-6 h-6 text-white flex-shrink-0" />
            <span className="text-lg whitespace-nowrap overflow-hidden max-w-0 opacity-0 group-hover:max-w-[200px] group-hover:opacity-100 transition-all duration-300">
              피해량 계산
            </span>
          </motion.button>
          <div className="w-full">
            <TabsContent value="overView">
              <Card className={`${elementColors[element].bg} shadow-lg ${elementColors[element].shadow} border-none pb-6 rounded-tr-none`}>
                <CardContent className={`w-full h-full flex relative ${elementColors[element].bg} rounded-2xl rounded-tr-none`}>
                  <div className="absolute z-0 flex gap-10 inset-6">
                    <div className="w-[40%] relative">
                      <div className={`w-[10%] pointer-events-none absolute inset-y-0 left-0 z-20 bg-gradient-to-r ${elementColors[element].gradient}`} />
                      <div className={`w-[10%] pointer-events-none absolute inset-y-0 right-0 z-20 bg-gradient-to-l ${elementColors[element].gradient}`} />
                      <div className={`h-[15%] pointer-events-none absolute inset-x-0 top-0 z-20 bg-gradient-to-b ${elementColors[element].gradient}`} />
                      <div className={`h-[15%] pointer-events-none absolute inset-x-0 bottom-0 z-20 bg-gradient-to-t ${elementColors[element].gradient}`} />
                      <Image src={info.icon.gacha} className={`object-cover object-[center] opacity-90`} alt="" fill priority sizes="(max-width: 1200px) 7vw" />
                    </div>
                    <div className="flex-1 relative opacity-35">
                      <Image src={`/img/Element_${element}_White.svg`} alt="" fill priority sizes="(max-width: 1200px) 7vw" />
                    </div>
                  </div>
                  <div className="w-full flex gap-10 z-10 text-white drop-shadow-[0_1px_3px_rgba(0,0,0,1)]">
                    <div className={`w-[40%] flex flex-col pl-8 pt-3 z-10`}>
                      <Label className="text-5xl font-bold ">{info.name}</Label>
                      <FormField
                        control={form.control}
                        name={`data.level`}
                        render={({ field }) => (
                          <FormItem className="w-fit h-fit mb-auto justify-start flex-1">
                            <div className="flex pt-[10%] mb-auto">
                              <FormLabel className="w-fit h-fit text-3xl font-bold mr-3">Lv: </FormLabel>
                              <FormControl>
                                <Input
                                  className="h-fit border-b-3 border-t-0 border-x-0 rounded-none !text-3xl text-center font-bold shadow-none focus-visible:ring-0 input-removeArrow my-auto p-0"
                                  value={field.value}
                                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => field.onChange(inputNumberWithSpace(e.target.value))}
                                  type="number"
                                  min={1}
                                  max={90}
                                  placeholder="Lv"
                                />
                              </FormControl>
                            </div>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>
                    <div className="flex-1 mt-auto">
                      <div className="w-[70%] grid grid-cols-[1fr_auto] gap-y-5 gap-x-10 bg-gray-700/10 rounded-2xl p-8 mx-auto">
                        {[
                          { label: "체력", value: info.totalStat.FIGHT_PROP_HP_FINAL },
                          { label: "공격력", value: info.totalStat.FIGHT_PROP_ATTACK_FINAL },
                          { label: "방어력", value: info.totalStat.FIGHT_PROP_DEFENSE_FINAL },
                          { label: "원소마스터리", value: info.totalStat.FIGHT_PROP_ELEMENT_MASTERY },
                          { label: "원소충전효율(%)", value: info.totalStat.FIGHT_PROP_CHARGE_EFFICIENCY },
                          { label: "치명타 확률(%)", value: info.totalStat.FIGHT_PROP_CRITICAL },
                          { label: "치명타 피해량(%)", value: info.totalStat.FIGHT_PROP_CRITICAL_HURT },
                          { label: "물리 피해증가(%)", value: info.totalStat.FIGHT_PROP_PHYSICAL_ADD_HURT },
                          {
                            label: `${elementAddHurtKey[element].label} 원소 피해증가(%)`,
                            value: info.totalStat[elementAddHurtKey[element].key],
                          },
                          { label: "피해증가(%)", value: info.totalStat.FIGHT_PROP_ATTACK_ADD_HURT },
                        ].map(({ label, value }, i) => (
                          <React.Fragment key={i}>
                            <Label className="w-fit h-fit text-2xl font-bold">{label}</Label>
                            <Label className="w-fit h-fit text-2xl font-bold">{formatterTotalFightProp(value, label.includes("%"), label !== "원소마스터리")}</Label>
                          </React.Fragment>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="skill-constellation-weapon">
              <Card className={`${elementColors[element].bg} shadow-lg ${elementColors[element].shadow} border-none pb-6 rounded-tr-none`}>
                <CardContent className={`w-full h-full flex gap-6 ${elementColors[element].bg}`}>
                  <Tabs className="flex-1 h-[90%]" defaultValue={`passiveSkill-0`}>
                    <Label className="text-3xl font-bold text-gray-700">특성 & 운명의 자리</Label>
                    <TabsList className="w-full h-auto flex flex-col bg-gray-700 border-2 rounded-2xl">
                      {/* 특성 */}
                      <div className="w-full flex justify-around p-2">
                        {Object.entries({ passiveSkill: info.passiveSkill, activeSkill: info.activeSkill }).map(([key, skills]) => {
                          return skills.map((_skill, j) => {
                            const skillInfo = info[key as "passiveSkill" | "activeSkill"][j];
                            const tabValue = `${key}-${j}`;
                            return (
                              <TabsTrigger
                                className="size-20 relative border-2 bg-gray-500 border-white rounded-full flex-none data-[state=active]:bg-gray-500 data-[state=active]:border-lime-400"
                                key={tabValue}
                                value={tabValue}
                              >
                                <Image src={skillInfo.icon} alt="" fill sizes="(max-width: 1200px) 7vw" />
                              </TabsTrigger>
                            );
                          });
                        })}
                      </div>
                      {/* 운명의 자리 */}
                      <div className="w-full flex justify-around p-2">
                        {info.constellations.map((constellation, j) => {
                          const tabValue = `constellations-${j}`;
                          return (
                            <TabsTrigger
                              className="size-20 relative border-2 bg-gray-500 border-white rounded-full flex-none data-[state=active]:bg-gray-500 data-[state=active]:border-lime-400"
                              key={tabValue}
                              value={tabValue}
                            >
                              <Image src={constellation.icon} alt="" fill sizes="(max-width: 1200px) 7vw" />
                            </TabsTrigger>
                          );
                        })}
                      </div>
                    </TabsList>
                    {Object.entries({ passiveSkill: info.passiveSkill, activeSkill: info.activeSkill, constellations: info.constellations }).map(([key, skillConstellation]) => {
                      return skillConstellation.map((dataInfo, j) => {
                        const tabValue = `${key}-${j}`;
                        return (
                          <TabsContent
                            className="w-full max-h-[90%] border-2 bg-gray-700 rounded-2xl text-white overflow-y-auto overflow-x-hidden scrollbar-custom"
                            style={{ scrollbarGutter: "stable" }}
                            key={tabValue}
                            value={tabValue}
                          >
                            <FormField
                              control={form.control}
                              name={`data.${key as "passiveSkill" | "activeSkill" | "constellations"}.${j}`}
                              render={({ field }) => (
                                <FormItem className="w-full flex flex-col">
                                  <FormControl>
                                    <div className="w-full h-full p-3">
                                      <div className="w-full flex gap-1">
                                        <h1 className="text-2xl font-bold">{dataInfo.name}</h1>
                                        {"unlocked" in field.value && (
                                          <>
                                            <p className="text-xl font-bold my-auto ml-2">해금</p>
                                            <Switch
                                              className="w-[50px] h-[25px] my-auto"
                                              thumbClassName="size-[18px] data-[state=checked]:translate-x-[calc(50px-(100%+4px))] data-[state=unchecked]:translate-x-0" // translate-x의 값은 내부 원 크기 +2(즉, 기본 기준 18px)만큼 -연산 후 들어가야함
                                              checked={field.value.unlocked}
                                              onCheckedChange={(value) => field.onChange({ ...field.value, unlocked: value })}
                                            />
                                          </>
                                        )}

                                        {"level" in field.value && (
                                          <>
                                            <p className="text-2xl font-bold ml-2">Lv:</p>
                                            <Input
                                              className="w-auto !text-lg border-b-2 border-t-0 border-x-0 rounded-none text-center font-bold focus-visible:ring-0 input-removeArrow p-0 mx-0 mt-auto mb-2"
                                              placeholder="Lv"
                                              type="number"
                                              value={field.value.level}
                                              max={10}
                                              min={0}
                                              onChange={(e) => {
                                                const value = inputNumberWithSpace(e.target.value);
                                                field.onChange({ ...field.value, level: Number(value) > 10 ? 10 : value });
                                              }}
                                            />
                                          </>
                                        )}
                                      </div>
                                      <Accordion className="w-full mb-3" type="single" collapsible defaultValue="description">
                                        <AccordionItem className="h-auto" value="description">
                                          <AccordionTrigger className="font-bold">Description</AccordionTrigger>
                                          <AccordionContent className="flex flex-col gap-4 text-base whitespace-pre-wrap">{dataInfo.description}</AccordionContent>
                                        </AccordionItem>
                                      </Accordion>

                                      {field.value.options.length ? (
                                        <>
                                          <Label className="text-2xl font-bold mb-1">옵션</Label>
                                          <div className="w-full flex gap-7">
                                            {field.value.options.map((option, i) => {
                                              const optionInfo = dataInfo.options[i];
                                              return (
                                                <div key={`${tabValue}-option-${i}`} className="flex">
                                                  <p className="text-xl mr-2 my-auto">{optionInfo.label}:</p>
                                                  {optionInfo.type === "toggle" && (
                                                    <Switch
                                                      className="w-[50px] h-[22px] my-auto"
                                                      thumbClassName="data-[state=checked]:translate-x-[calc(50px-(100%+4px))] data-[state=unchecked]:translate-x-0" // translate-x의 값은 내부 원 크기 +2(즉, 기본 기준 18px)만큼 -연산 후 들어가야함
                                                      checked={option.active}
                                                      onCheckedChange={(value) => {
                                                        field.value.options[i].active = value;
                                                        field.onChange(field.value);
                                                      }}
                                                    />
                                                  )}
                                                  {optionInfo.type === "stack" && (
                                                    <Input
                                                      className="w-auto !text-lg border-b-2 border-t-0 border-x-0 rounded-none text-center font-bold focus-visible:ring-0 input-removeArrow p-0 mx-0 mt-auto mb-2"
                                                      placeholder="Lv"
                                                      type="number"
                                                      value={field.value.options[i].stack}
                                                      max={optionInfo.maxStack}
                                                      min={0}
                                                      onChange={(e) => {
                                                        const value = Number(inputNumberWithSpace(e.target.value));
                                                        field.value.options[i].stack = value > optionInfo.maxStack ? optionInfo.maxStack : value;
                                                        field.onChange(field.value);
                                                      }}
                                                    />
                                                  )}
                                                </div>
                                              );
                                            })}
                                          </div>
                                        </>
                                      ) : (
                                        <></>
                                      )}
                                    </div>
                                  </FormControl>
                                </FormItem>
                              )}
                            />
                          </TabsContent>
                        );
                      });
                    })}
                  </Tabs>

                  {/* 무기 */}
                  <FormField
                    control={form.control}
                    name={`data.weapon`}
                    render={({ field }) => (
                      <FormItem className="w-[30%] h-[90%] flex">
                        <FormControl>
                          <div className="h-full flex flex-col">
                            <Label className="text-3xl font-bold text-gray-700 mb-2">무기</Label>
                            <WeaponSettingCard
                              weapon={field.value}
                              onChange={(weapon) => {
                                if (weapon) {
                                  field.onChange({
                                    ...weapon,
                                    id: weapon.id,
                                    name: weapon.name,
                                    level: 90,
                                    refinement: 1,
                                    options: weapon.options.map((o) => ({ ...o, active: true, stack: o.maxStack, select: null })),
                                  });
                                }
                              }}
                              onLevelChange={(level) => {
                                field.onChange({ ...field.value, level });
                              }}
                              onRefinementChange={(refinement) => {
                                field.onChange({ ...field.value, refinement });
                              }}
                              onOptionsChange={field.value.options.map((option, i) => (val, key) => {
                                if (typeof val !== "boolean" && Number(val) > option.maxStack) {
                                  val = option.maxStack;
                                }
                                field.value.options[i] = { ...option, [key]: val };
                                field.onChange(field.value);
                              })}
                            />
                          </div>
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="artifact">
              <Card className={`${elementColors[element].bg} shadow-lg ${elementColors[element].shadow} border-none pb-6 rounded-tr-none`}>
                <CardContent className={`h-full min-h-[650px] flex flex-col gap-6 ${elementColors[element].bg} text-white `}>
                  {/* 성유물 파츠 영역 */}
                  <div className="w-full flex-1 flex flex-col gap-2">
                    <Label className="text-3xl font-bold text-gray-700">성유물</Label>
                    <div className="w-full flex-1 grid gap-1 grid-cols-[repeat(auto-fit,minmax(230px,1fr))]">
                      {info.artifact.parts.map((artifact, i) => {
                        return (
                          <FormField
                            key={`data.artifact.parts.${i}`}
                            control={form.control}
                            name={`data.artifact.parts.${i}`}
                            render={({ field }) => {
                              const [mainKey, mainValue] = Object.entries(field.value.mainStat)[0];
                              const subOptions = field.value.subStat.map((o) => {
                                const [key, val] = Object.entries(o)[0];
                                return { key, value: val };
                              });

                              return (
                                <FormItem>
                                  <ArtifactPartCard
                                    key={`artifact-part-${i}`}
                                    className={`bg-gray-700`}
                                    artifact={artifact}
                                    main={{ key: mainKey, value: mainValue }}
                                    sub={subOptions}
                                    onSetChange={(value) => {
                                      field.value.setName = value;
                                      field.onChange(field.value);
                                      const parts = form.getValues(`data.artifact.parts`);
                                      form.setValue(`data.artifact.setInfo`, getArtifactSetInfo(parts));
                                    }}
                                    onMainChange={(mainValue) => {
                                      field.value.mainStat = mainValue;
                                      field.onChange(field.value);
                                    }}
                                    onSubChange={subOptions.map((_o, j) => (subValue) => {
                                      field.value.subStat[j] = subValue;
                                      field.onChange(field.value);
                                    })}
                                  />
                                </FormItem>
                              );
                            }}
                          />
                        );
                      })}
                    </div>
                  </div>

                  {/* 성유물 세트 옵션*/}
                  <div className="flex flex-col gap-2">
                    <Label className="text-3xl font-bold text-gray-700">성유물 세트</Label>
                    <FormField
                      control={form.control}
                      name={`data.artifact.setInfo`}
                      render={({ field }) => (
                        <FormItem className="w-full flex gap-1">
                          {field.value.map((set, i) => {
                            const parts = form.getValues(`data.artifact.parts`);
                            const rawInfo = artifactSets[set.name];
                            const numberOfParts = parts.filter((p) => p.setName === set.name).length;
                            if (rawInfo) {
                              const options = rawInfo.options.map((o, j) => ({ ...o, ...field.value[i].options[j] }));
                              return (
                                <FormControl key={`${set.name}-${i}`}>
                                  <ArtifactSetOptionCard
                                    className={`w-[35%] bg-gray-700`}
                                    setInfo={{ ...rawInfo, ...set, options: options, numberOfParts: numberOfParts }}
                                    onChnage={field.value[i].options.map((option, j) => (val) => {
                                      if (typeof val !== "boolean" && Number(val) > options[j].maxStack) val = options[j].maxStack;
                                      field.value[i].options[j] = { ...option, [typeof val === "boolean" ? "active" : "stack"]: val };
                                      field.onChange(field.value);
                                    })}
                                  />
                                </FormControl>
                              );
                            }
                          })}
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            <DamageResultCard damageResult={damageResult} element={element} />
          </div>
          <TabsList className={`h-fit justify-around pt-3 rounded-l-none ${elementColors[element].bg} mx-auto flex-col`}>
            <TabsTrigger className="w-full data-[state=active]:bg-transparent" value="overView">
              <div className={`size-10 relative ${infoTab === "overView" ? "bg-white" : ""}  rounded-full`}>
                <Image className="opacity-80" src={"/img/Icon_Inventory_Character_Development_Items.webp"} alt="" fill sizes="(max-width: 1200px) 7vw" />
              </div>
            </TabsTrigger>
            <TabsTrigger className="w-full bg-transparent data-[state=active]:bg-transparent" value="skill-constellation-weapon">
              <div className={`size-10 relative ${infoTab === "skill-constellation-weapon" ? "bg-white" : ""}  rounded-full`}>
                <Image className="opacity-80" src={"/img/Icon_Inventory_Weapons.png"} alt="" fill sizes="(max-width: 1200px) 7vw" />
              </div>
            </TabsTrigger>
            <TabsTrigger className="w-full bg-transparent data-[state=active]:bg-transparent" value="artifact">
              <div className={`size-10 relative ${infoTab === "artifact" ? "bg-white" : ""}  rounded-full`}>
                <Image className="opacity-80" src={"/img/Icon_Inventory_Artifacts.png"} alt="" fill sizes="(max-width: 1200px) 7vw" />
              </div>
            </TabsTrigger>
          </TabsList>
        </form>
      </Form>
    </Tabs>
  );
};

export default CharacterSettingCard;
