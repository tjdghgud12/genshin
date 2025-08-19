"use Client";

import ArtifactSetOptionCard from "@/app/calculator/components/ArtifactSetOptionCard";
import CharacterOptionControlCircle from "@/app/calculator/components/CharacterOptionControlCircle";
import WeaponSettingCard from "@/app/calculator/components/WeaponSettingCard";
import { calculatorFormSchema, formSchema } from "@/app/calculator/page";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import React from "react";
import { UseFormReturn, useWatch } from "react-hook-form";
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
  useWatch({ control: form.control, name: `data.${index}` }); // useWatch가 없는 상태에서는 React Hook Form이 이 컴포넌트를 “변화 감지 대상”으로 인식하지 않아서, 입력이 제대로 반영되지 않는 것처럼 보임
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
          className={`w-[45%] h-fit min-h-[500px] bg-[54%_center] bg-cover bg-no-repeat opacity-90 flex flex-col pl-1 py-3`}
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
                      onChange={(e: React.ChangeEvent<HTMLInputElement>) => form.setValue(`data.${index}.level`, Number(e.target.value))}
                      type="number"
                      min={1}
                      max={90}
                      placeholder="Level"
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
              {item.passiveSkill.map((passive, j) => {
                const passiveInfo = item.raw.passiveSkill[j];
                return (
                  <FormField
                    key={`passive-${index}-${j}`}
                    control={form.control}
                    name={`data.${index}.passiveSkill.${j}`}
                    render={() => (
                      <FormItem className="w-fit mt-3 justify-start">
                        <div className="flex">
                          <FormControl className="w-fit h-fit flex flex-col">
                            <CharacterOptionControlCircle
                              name={passiveInfo.name}
                              description={passiveInfo.description}
                              unlocked={passive.unlocked}
                              options={passive.options.map((o, k) => ({ ...passiveInfo.options[k], ...o, inputLabel: passiveInfo.options[k].label }))}
                              icon={passiveInfo.icon}
                              onClick={() => {
                                const options = form.getValues(`data.${index}.passiveSkill.${j}.options`);
                                form.setValue(
                                  `data.${index}.passiveSkill.${j}.options`,
                                  options.map((o) => ({ ...o, active: !o.active })),
                                );
                              }}
                              onChange={(e, k) => {
                                if (/^\d*$/.test(e.target.value)) {
                                  const value = Number(e.target.value);
                                  const maxStack = passiveInfo.options[k].maxStack;
                                  form.setValue(`data.${index}.passiveSkill.${j}.options.${k}.stack`, value > maxStack ? maxStack : value);
                                }
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
                              options={active.options.map((o, k) => ({ ...activeInfo.options[k], ...o, inputLabel: activeInfo.options[k].label }))}
                              icon={activeInfo.icon}
                              useLevel
                              level={field.value.level}
                              onClick={() => {
                                const options = form.getValues(`data.${index}.activeSkill.${j}.options`);
                                form.setValue(
                                  `data.${index}.activeSkill.${j}.options`,
                                  options.map((o) => ({ ...o, active: !o.active })),
                                );
                              }}
                              onChange={(e, k) => {
                                if (/^\d*$/.test(e.target.value)) {
                                  const value = Number(e.target.value);
                                  const maxStack = activeInfo.options[k].maxStack;
                                  form.setValue(`data.${index}.activeSkill.${j}.options.${k}.stack`, value > maxStack ? maxStack : value);
                                }
                              }}
                              onLevelChange={(level) => {
                                form.setValue(`data.${index}.activeSkill.${j}.level`, level);
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
                    render={() => (
                      <FormItem className="w-fit mt-3 justify-start">
                        <div className="flex">
                          <FormControl className="w-fit h-fit flex flex-col">
                            <CharacterOptionControlCircle
                              name={constellationInfo.name}
                              description={constellationInfo.description}
                              unlocked={constellation.unlocked}
                              options={constellation.options.map((o, k) => ({ ...constellationInfo.options[k], ...o, inputLabel: constellationInfo.options[k].label }))}
                              icon={constellationInfo.icon}
                              onClick={() => {
                                const options = form.getValues(`data.${index}.constellations.${j}.options`);
                                form.setValue(
                                  `data.${index}.constellations.${j}.options`,
                                  options.map((o) => ({ ...o, active: !o.active })),
                                );
                              }}
                              onChange={(e, k) => {
                                if (/^\d*$/.test(e.target.value)) {
                                  const value = Number(e.target.value);
                                  const maxStack = constellationInfo.options[k].maxStack;
                                  form.setValue(`data.${index}.constellations.${j}.options.${k}.stack`, value > maxStack ? maxStack : value);
                                }
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
        <div className="w-3/5  h-fit flex py-3">
          <div className="w-1/2 flex flex-col gap-2">
            <div className="w-full h-full flex">
              <FormField
                control={form.control}
                name={`data.${index}.weapon`}
                render={({ field }) => (
                  <FormItem className="w-full h-fit mb-auto justify-start">
                    <FormControl className="w-full">
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
                          if (level > 90) level = 90;
                          field.onChange({ ...field.value, level });
                        }}
                        onRefinementChange={(refinement) => {
                          if (refinement > 5) refinement = 5;
                          field.onChange({ ...field.value, refinement });
                        }}
                        onOptionsChange={field.value.options.map((_option, i) => (val) => {
                          if (typeof val === "number" && val > item.raw.weapon.options[i].maxStack) {
                            val = item.raw.weapon.options[i].maxStack;
                          }
                          form.setValue(`data.${index}.weapon.options.${i}.${typeof val === "boolean" ? "active" : "stack"}`, val);
                        })}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            <div className="w-full h-full flex flex-col">
              <FormField
                control={form.control}
                name={`data.${index}.artifact`}
                render={({ field }) => (
                  <FormItem className="w-full h-fit mb-auto justify-start">
                    {field.value.setInfo.map((val, i) => {
                      const parts = field.value.parts;
                      return (
                        <FormControl key={`${val.name}-${i}`} className="w-full">
                          <ArtifactSetOptionCard val={val} parts={[]} />
                        </FormControl>
                      );
                    })}
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
          </div>
          <div className="w-1/2 flex flex-col">
            <Button type="submit" className="bg-gray-800 hover:bg-gray-600">
              Submit
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default CharacterSettingCard;
