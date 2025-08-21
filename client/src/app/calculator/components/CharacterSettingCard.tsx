"use Client";

import { ArtifactPartCard, ArtifactSetOptionCard } from "@/app/calculator/components/ArtifactCard";
import CharacterOptionControlCircle from "@/app/calculator/components/CharacterOptionControlCircle";
import WeaponSettingCard from "@/app/calculator/components/WeaponSettingCard";
import { calculatorFormSchema, formSchema } from "@/app/calculator/page";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { inputNumberWithSpace } from "@/lib/utils";
import { useCalculatorStore } from "@/store/useCalculatorStore";
import { IArtifactOptionInfo } from "@/types/artifactType";
import React from "react";
import { UseFormReturn } from "react-hook-form";
import { z } from "zod";

const CharacterSettingCard = ({
  form,
  item,
  index,
}: {
  form: UseFormReturn<z.infer<typeof formSchema>>;
  item: z.infer<typeof calculatorFormSchema>;
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

  return (
    <Card className={`p-0 shadow-lg shadow-gray-400`}>
      <CardContent className={`flex ${elementColors[item.raw.element].bg} rounded-2xl text-stone-600`}>
        <div className={`w-[45%] h-fit min-h-[500px] bg-center bg-cover bg-no-repeat opacity-90 flex flex-col pl-8 py-3`}>
          {/* <div
          className={`w-[45%] h-full min-h-[500px] bg-[54%_center] bg-cover bg-no-repeat opacity-90 flex flex-col pl-1 py-3 mt-auto`}
          style={{ backgroundImage: `url('${item.raw.icon.gacha}')` }}
        > */}
          <FormField
            control={form.control}
            name={`data.${index}.level`}
            render={({ field }) => (
              <FormItem className="w-fit mb-auto justify-start">
                <div className="flex">
                  <FormLabel className="w-fit text-xl font-bold my-auto">Lv: </FormLabel>
                  <FormControl>
                    <Input
                      className="w-full border-none text-xl font-bold shadow-none focus-visible:ring-0 input-removeArrow"
                      {...field}
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

          {/* 패시브 스킬 */}
          <div className="w-full h-auto flex">
            <div className="flex-1 flex flex-col mt-auto">
              {item.passiveSkill.map((_passive, j) => {
                const passiveInfo = item.raw.passiveSkill[j];
                return (
                  <FormField
                    key={`passive-${index}-${j}`}
                    control={form.control}
                    name={`data.${index}.passiveSkill.${j}`}
                    render={({ field }) => (
                      <FormItem className="w-fit mt-3 justify-start">
                        <div className="flex">
                          <FormControl className="w-fit h-fit flex flex-col">
                            <CharacterOptionControlCircle
                              name={passiveInfo.name}
                              description={passiveInfo.description}
                              unlocked={field.value.unlocked}
                              options={field.value.options.map((o, k) => ({ ...passiveInfo.options[k], ...o, inputLabel: passiveInfo.options[k].label }))}
                              icon={passiveInfo.icon}
                              onClick={() => {
                                field.value.options = field.value.options.map((o) => ({ ...o, active: !o.active }));
                                field.onChange(field.value);
                              }}
                              onChange={(e, k) => {
                                const maxStack = passiveInfo.options[k].maxStack;
                                const value = inputNumberWithSpace(e.target.value);
                                field.value.options[k].stack = value > maxStack ? maxStack : value;
                                field.onChange(field.value);
                              }}
                            />
                          </FormControl>
                        </div>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                );
              })}
            </div>

            {/* 액티브 스킬 */}
            <div className="w-[22%] h-full flex flex-col mt-auto mr-0.5">
              {item.activeSkill.map((active, j) => {
                const activeInfo = item.raw.activeSkill[j];

                return (
                  <FormField
                    key={`activeSkill-${index}-${j}`}
                    control={form.control}
                    name={`data.${index}.activeSkill.${j}`}
                    render={({ field }) => (
                      <FormItem className="w-fit mt-3">
                        <div className="flex">
                          <FormControl className="w-fit h-fit flex flex-col">
                            <CharacterOptionControlCircle
                              name={activeInfo.name}
                              description={activeInfo.description}
                              unlocked
                              options={field.value.options.map((o, k) => ({ ...activeInfo.options[k], ...o, inputLabel: activeInfo.options[k].label }))}
                              icon={activeInfo.icon}
                              useLevel
                              level={field.value.level}
                              onClick={() => {
                                field.value.options = field.value.options.map((o) => ({ ...o, active: !o.active }));
                                field.onChange(field.value);
                              }}
                              onChange={(e, k) => {
                                const maxStack = activeInfo.options[k].maxStack;
                                const value = inputNumberWithSpace(e.target.value);
                                field.value.options[k].stack = value > maxStack ? maxStack : value;
                                field.onChange(field.value);
                              }}
                              onLevelChange={(level) => {
                                field.value.level = level;
                                field.onChange(field.value);
                              }}
                            />
                          </FormControl>
                        </div>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                );
              })}
            </div>

            {/* 운명의 자리 */}
            <div className="w-[22%] h-full flex flex-col mt-auto">
              {item.constellations.map((constellation, j) => {
                const constellationInfo = item.raw.constellations[j];

                return (
                  <FormField
                    key={`constellations-${index}-${j}`}
                    control={form.control}
                    name={`data.${index}.constellations.${j}`}
                    render={({ field }) => (
                      <FormItem className="w-fit mt-3 justify-start">
                        <div className="flex">
                          <FormControl className="w-fit h-fit flex flex-col">
                            <CharacterOptionControlCircle
                              name={constellationInfo.name}
                              description={constellationInfo.description}
                              unlocked={field.value.unlocked}
                              options={field.value.options.map((o, k) => ({ ...constellationInfo.options[k], ...o, inputLabel: constellationInfo.options[k].label }))}
                              icon={constellationInfo.icon}
                              onClick={() => {
                                field.value.options = field.value.options.map((o) => ({ ...o, active: !o.active }));
                                field.onChange(field.value);
                              }}
                              onChange={(e, k) => {
                                const maxStack = constellationInfo.options[k].maxStack;
                                const value = inputNumberWithSpace(e.target.value);
                                field.value.options[k].stack = value > maxStack ? maxStack : value;
                                field.onChange(field.value);
                              }}
                            />
                          </FormControl>
                        </div>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                );
              })}
            </div>
          </div>
        </div>

        <div className="w-3/5 h-auto flex py-3 gap-3">
          <div className="flex flex-col gap-2">
            {/* 무기 */}
            <div className="flex justify-start mb-auto">
              <FormField
                control={form.control}
                name={`data.${index}.weapon`}
                render={({ field }) => (
                  <FormItem className="w-full h-fit mb-auto">
                    <FormControl>
                      <WeaponSettingCard
                        className={`${elementColors[item.raw.element].shadow}`}
                        type={item.raw.weaponType}
                        weapon={field.value}
                        onChange={(weapon) => {
                          if (weapon) {
                            field.onChange({
                              id: weapon.id,
                              name: weapon.name,
                              level: 90,
                              refinement: 0,
                              options: weapon.options.map((_o) => ({ active: false, stack: 0 })),
                            });
                          }
                        }}
                        onLevelChange={(level) => {
                          field.onChange({ ...field.value, level });
                        }}
                        onRefinementChange={(refinement) => {
                          field.onChange({ ...field.value, refinement });
                        }}
                        onOptionsChange={field.value.options.map((option, i) => (val) => {
                          if (typeof val !== "boolean" && Number(val) > item.raw.weapon.options[i].maxStack) {
                            val = item.raw.weapon.options[i].maxStack;
                          }
                          field.value.options[i] = { ...option, [typeof val === "boolean" ? "active" : "stack"]: val };
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
            <div className="w-full h-fit flex flex-col mx-auto">
              <FormField
                control={form.control}
                name={`data.${index}.artifact.setInfo`}
                render={({ field }) => (
                  <FormItem className="w-full h-fit mb-auto">
                    {field.value.map((set, i) => {
                      const parts = form.getValues(`data.${index}.artifact.parts`);
                      const rawInfo = artifactSets.find((s) => s.name === set.name);
                      const numberOfParts = parts.filter((p) => p.setName === set.name).length;
                      if (rawInfo) {
                        const options = rawInfo.options.map((o, j) => ({ ...o, ...field.value[i].options[j] }));
                        return (
                          <FormControl key={`${set.name}-${i}`}>
                            <ArtifactSetOptionCard
                              className={`${elementColors[item.raw.element].shadow}`}
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
            <Button type="submit" className="bg-gray-800 hover:bg-gray-600 mb-auto">
              Submit
            </Button>
            {/* 성유물 파츠 영역 */}
            <div className="flex flex-col">
              {item.artifact.parts.map((artifact, i) => {
                return (
                  <FormField
                    key={`data.${index}.artifact.parts.${i}`}
                    // className="w-full h-fit mb-auto"
                    control={form.control}
                    name={`data.${index}.artifact.parts.${i}`}
                    render={({ field }) => {
                      const [mainKey, mainValue] = Object.entries(field.value.mainStat)[0];
                      const subOptions: IArtifactOptionInfo[] = field.value.subStat.map((o) => {
                        const [key, val] = Object.entries(o)[0];
                        return { key, value: val };
                      });

                      return (
                        <FormItem className="w-full h-fit mb-auto">
                          <ArtifactPartCard
                            key={`artifact-part-${i}`}
                            className={`${elementColors[item.raw.element].shadow}`}
                            artifact={artifact}
                            main={{ key: mainKey, value: mainValue }}
                            sub={subOptions}
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
      </CardContent>
    </Card>
  );
};

export default CharacterSettingCard;
