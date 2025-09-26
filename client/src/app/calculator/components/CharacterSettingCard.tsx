"use Client";

import { ArtifactPartCard, ArtifactSetOptionCard } from "@/app/calculator/components/ArtifactCard";
import CharacterOptionControlCircle from "@/app/calculator/components/CharacterOptionControlCircle";
import WeaponSettingCard from "@/app/calculator/components/WeaponSettingCard";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { calculatorCharacterInfoSchema, calculatorFormSchema as formSchema } from "@/lib/calculator";
import { inputNumberWithSpace } from "@/lib/utils";
import { useCalculatorStore } from "@/store/useCalculatorStore";
import { IArtifactOptionInfo } from "@/types/artifactType";
import Image from "next/image";
import React from "react";
import { UseFormReturn } from "react-hook-form";
import { z } from "zod";

type TArtifactSetInfo = z.infer<typeof calculatorCharacterInfoSchema>["artifact"]["setInfo"][number];
type TArtifactPartInfo = z.infer<typeof calculatorCharacterInfoSchema>["artifact"]["parts"][number];

const CharacterSettingCard = ({
  form,
  item,
  index,
}: {
  form: UseFormReturn<z.infer<typeof formSchema>>;
  item: z.infer<typeof calculatorCharacterInfoSchema>;
  index: number;
}): React.ReactElement => {
  const artifactSets = useCalculatorStore((store) => store.artifactSets);
  const elementColors: Record<string, Record<string, string>> = {
    Fire: { bg: `bg-Fire`, shadow: "shadow-shadow-Fire" },
    Water: { bg: `bg-Water`, shadow: "shadow-shadow-Water" },
    Wind: { bg: `bg-Wind`, shadow: "shadow-shadow-Wind" },
    Electric: { bg: `bg-Electric`, shadow: "shadow-shadow-Electric" },
    Ice: { bg: `bg-Ice`, shadow: "shadow-shadow-Ice" },
    Rock: { bg: `bg-Rock`, shadow: "shadow-shadow-Rock" },
    Grass: { bg: `bg-Grass`, shadow: "shadow-shadow-Grass" },
  };

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

  return (
    <Card className={`aspect-[2/1.1] p-0 ${elementColors[item.raw.element].bg} shadow-lg ${elementColors[item.raw.element].shadow} border-none pb-6`}>
      <CardContent className={`h-full flex ${elementColors[item.raw.element].bg} rounded-2xl text-gray-700 pl-0 relative`}>
        <div className="w-[70%] h-full absolute z-0">
          <Image src={item.raw.icon.gacha} className={`object-cover object-[83%_center] opacity-90`} alt="" fill sizes="(max-width: 1200px) 7vw" />
        </div>
        <div className="w-full flex z-10">
          <div className={`w-[45%] flex flex-col pl-8 pt-3 z-10`}>
            <FormField
              control={form.control}
              name={`data.${index}.level`}
              render={({ field }) => (
                <FormItem className="w-fit h-fit mb-auto justify-start flex-1">
                  <div className="flex pt-[10%] mb-auto">
                    <FormLabel className="w-fit h-fit text-3xl font-bold mr-3">Lv: </FormLabel>
                    <FormControl>
                      <Input
                        className="h-fit border-b-2 border-t-0 border-x-0 rounded-none !text-3xl text-center font-bold shadow-none focus-visible:ring-0 input-removeArrow my-auto p-0"
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

            <div className="w-full h-auto flex">
              {/* 패시브 스킬 */}
              <div className="w-[18%] h-full flex flex-col justify-end mr-auto">
                {item.passiveSkill.map((_passive, j) => {
                  const passiveInfo = item.raw.passiveSkill[j];
                  return (
                    <FormField
                      key={`passive-${index}-${j}`}
                      control={form.control}
                      name={`data.${index}.passiveSkill.${j}`}
                      render={({ field }) => (
                        <FormItem className="w-full mt-3 flex flex-col">
                          <FormControl>
                            <CharacterOptionControlCircle
                              name={passiveInfo.name}
                              description={passiveInfo.description}
                              unlocked={field.value.unlocked}
                              options={field.value.options.map((o, k) => ({ ...passiveInfo.options[k], ...o, inputLabel: passiveInfo.options[k].label }))}
                              icon={passiveInfo.icon}
                              onClick={() => {
                                field.value.unlocked = !field.value.unlocked;
                                field.onChange(field.value);
                              }}
                              onChange={(newValue, k) => {
                                const option = field.value.options[k];
                                if (typeof newValue === "boolean") {
                                  option.active = newValue;
                                }
                                if (typeof newValue === "string") {
                                  const maxStack = passiveInfo.options[k].maxStack;
                                  const value = inputNumberWithSpace(newValue);
                                  option.stack = value > maxStack ? maxStack : value;
                                }
                                field.onChange(field.value);
                              }}
                            />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  );
                })}
              </div>

              {/* 액티브 스킬 */}
              <div className="w-[18%] h-full flex flex-col justify-end mr-0.5">
                {item.activeSkill.map((_active, j) => {
                  const activeInfo = item.raw.activeSkill[j];

                  return (
                    <FormField
                      key={`activeSkill-${index}-${j}`}
                      control={form.control}
                      name={`data.${index}.activeSkill.${j}`}
                      render={({ field }) => (
                        <FormItem className="w-full h-fit mt-3 flex flex-col">
                          <FormControl>
                            <CharacterOptionControlCircle
                              name={activeInfo.name}
                              description={activeInfo.description}
                              unlocked
                              options={field.value.options.map((o, k) => ({ ...activeInfo.options[k], ...o, inputLabel: activeInfo.options[k].label }))}
                              icon={activeInfo.icon}
                              useLevel
                              level={field.value.level}
                              onChange={(newValue, k) => {
                                const option = field.value.options[k];
                                if (typeof newValue === "boolean") {
                                  option.active = newValue;
                                }
                                if (typeof newValue === "string") {
                                  const maxStack = activeInfo.options[k].maxStack;
                                  const value = inputNumberWithSpace(newValue);
                                  option.stack = value > maxStack ? maxStack : value;
                                }
                                field.onChange(field.value);
                              }}
                              onLevelChange={(level) => {
                                field.value.level = level;
                                field.onChange(field.value);
                              }}
                            />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  );
                })}
              </div>

              {/* 운명의 자리 */}
              <div className="w-[18%] h-full flex flex-col mt-auto">
                {item.constellations.map((constellation, j) => {
                  const constellationInfo = item.raw.constellations[j];

                  return (
                    <FormField
                      key={`constellations-${index}-${j}`}
                      control={form.control}
                      name={`data.${index}.constellations.${j}`}
                      render={({ field }) => (
                        <FormItem className="w-full mt-3 flex flex-col justify-end">
                          <FormControl>
                            <CharacterOptionControlCircle
                              name={constellationInfo.name}
                              description={constellationInfo.description}
                              unlocked={field.value.unlocked}
                              options={field.value.options.map((o, k) => ({ ...constellationInfo.options[k], ...o, inputLabel: constellationInfo.options[k].label }))}
                              icon={constellationInfo.icon}
                              onClick={() => {
                                field.value.unlocked = !field.value.unlocked;
                                field.onChange(field.value);
                              }}
                              onChange={(newValue, k) => {
                                const option = field.value.options[k];
                                if (typeof newValue === "boolean") {
                                  option.active = newValue;
                                }
                                if (typeof newValue === "string") {
                                  const maxStack = constellationInfo.options[k].maxStack;
                                  const value = inputNumberWithSpace(newValue);
                                  option.stack = value > maxStack ? maxStack : value;
                                }
                                field.onChange(field.value);
                              }}
                            />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  );
                })}
              </div>
            </div>
          </div>

          <div className="w-3/5 h-auto flex pt-3 gap-3">
            <div className="w-[40%] flex flex-col gap-2">
              {/* 무기 */}
              <div className="flex justify-start mb-auto">
                <FormField
                  control={form.control}
                  name={`data.${index}.weapon`}
                  render={({ field }) => (
                    <FormItem className="w-full h-fit mb-auto">
                      <FormControl>
                        <WeaponSettingCard
                          className={`${elementColors[item.raw.element].bg} ${elementColors[item.raw.element].shadow}`}
                          type={item.raw.weaponType}
                          weapon={field.value}
                          onChange={(weapon) => {
                            if (weapon) {
                              field.onChange({
                                id: weapon.id,
                                name: weapon.name,
                                level: 90,
                                refinement: 1,
                                options: weapon.options.map((_o) => ({ active: false, stack: 0, select: null })),
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
                            if (typeof val !== "boolean" && Number(val) > item.raw.weapon.options[i].maxStack) {
                              val = item.raw.weapon.options[i].maxStack;
                            }
                            field.value.options[i] = { ...option, [key]: val };
                            field.onChange(field.value);
                          })}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              {/* 성유물 세트 옵션*/}
              <div className="flex flex-col justify-end">
                <FormField
                  control={form.control}
                  name={`data.${index}.artifact.setInfo`}
                  render={({ field }) => (
                    <FormItem className="w-full h-fit mb-auto">
                      {field.value.map((set, i) => {
                        const parts = form.getValues(`data.${index}.artifact.parts`);
                        const rawInfo = artifactSets[set.name];
                        const numberOfParts = parts.filter((p) => p.setName === set.name).length;
                        if (rawInfo) {
                          const options = rawInfo.options.map((o, j) => ({ ...o, ...field.value[i].options[j] }));
                          return (
                            <FormControl key={`${set.name}-${i}`}>
                              <ArtifactSetOptionCard
                                className={`${elementColors[item.raw.element].bg} ${elementColors[item.raw.element].shadow}`}
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
            </div>
            <div className="flex flex-col flex-1">
              <Button type="submit" className="h-[8%] bg-gray-800 hover:bg-gray-600 mb-3" data-index={index}>
                Submit
              </Button>
              {/* 성유물 파츠 영역 */}
              <div className="flex flex-col flex-1 gap-1">
                {item.artifact.parts.map((artifact, i) => {
                  return (
                    <FormField
                      key={`data.${index}.artifact.parts.${i}`}
                      control={form.control}
                      name={`data.${index}.artifact.parts.${i}`}
                      render={({ field }) => {
                        const [mainKey, mainValue] = Object.entries(field.value.mainStat)[0];
                        const subOptions: IArtifactOptionInfo[] = field.value.subStat.map((o) => {
                          const [key, val] = Object.entries(o)[0];
                          return { key, value: val };
                        });

                        return (
                          <FormItem className="w-full flex-1">
                            <ArtifactPartCard
                              key={`artifact-part-${i}`}
                              className={`${elementColors[item.raw.element].shadow}`}
                              artifact={artifact}
                              main={{ key: mainKey, value: mainValue }}
                              sub={subOptions}
                              onSetChange={(value) => {
                                field.value.setName = value;
                                field.onChange(field.value);
                                const parts = form.getValues(`data.${index}.artifact.parts`);
                                form.setValue(`data.${index}.artifact.setInfo`, getArtifactSetInfo(parts));
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
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default CharacterSettingCard;
