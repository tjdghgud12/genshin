"use Client";

import CharacterOptionControlCircle from "@/app/calculator/components/CharacterOptionControlCircle";
import { calculatorFormSchema, formSchema } from "@/app/calculator/page";
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

  return (
    <>
      <div className={`w-1/2 h-fit min-h-[500px] bg-center bg-cover bg-no-repeat opacity-90 flex flex-col px-8 py-3`}>
        {/* <div className={`w-1/2 h-fit min-h-[500px] bg-center bg-cover bg-no-repeat opacity-90 flex flex-col px-8 py-3`} style={{ backgroundImage: `url('${raw.icon.gacha}')` }}> */}
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
          <div className="w-[18%] h-full flex flex-col mt-auto mr-3">
            {item.activeSkill.map((active, j) => {
              const activeInfo = item.raw.activeSkill[j];

              return (
                <FormField
                  key={`activeSkill-${index}-${j}`}
                  control={form.control}
                  name={`data.${index}.activeSkill.${j}`}
                  render={() => (
                    <FormItem className="w-fit mt-3 justify-start">
                      <div className="flex">
                        <FormControl className="w-fit h-fit flex flex-col">
                          <CharacterOptionControlCircle
                            name={activeInfo.name}
                            description={activeInfo.description}
                            unlocked
                            options={active.options.map((o, k) => ({ ...activeInfo.options[k], ...o, inputLabel: activeInfo.options[k].label }))}
                            icon={activeInfo.icon}
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
          <div className="w-[18%] h-full flex flex-col mt-auto">
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
      <div className="w-1/2  h-fit flex px-8 py-3">
        <div className="w-2/5 flex flex-col">
          <div className="w-full flex">
            {/* 무기 옵션 선택부도 하나 추가해야함. */}
            {/* 똑같이 설정 icon 하나 추가하자 */}
            {/* 설정부는 어떻게 처리할까 */}
            {/* 1. 모든 무기의 정보를 싹 가져와야함. */}
            {/* root페이지 접근 시 요청해서 사용하자. */}
            {/* 루트페이지를 일부만 client 일부는 server단위로 쪼갤 수 있는지 알아보고, 가능하다면, 무기 및 성유물 정보는 가져와서 사용하는거로.*/}
            {/* back에서 넘겨줄 때 1차적으로 내가 현재 구현한 성유물 무기만 필터링해서 넘겨주기!! */}
            {/* FormField가 여러개 필요하네? 이름, 레벨, 재련이 필요해. */}
            {/* 일단 셀렉트박스의 옵션을 전부 가져온 다음에 생각하자. */}
            <FormField
              control={form.control}
              name={`data.${index}.weapon`}
              render={({ field }) => (
                <FormItem className="w-fit h-1/2 mb-auto justify-start">
                  <div className="flex">
                    <FormControl>
                      <SingleSelectBox />
                      {/* <Input
                        className="w-full border-none text-xl font-bold shadow-none focus-visible:ring-0 input-removeArrow"
                        {...field}
                        value={field.value}
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) => form.setValue(`data.${index}.level`, Number(e.target.value))}
                        type="number"
                        min={1}
                        max={90}
                        placeholder="Level"
                      /> */}
                    </FormControl>
                  </div>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>
          <div>세트옵션</div>
        </div>
        <div className="w-3/5 flex flex-col">성유물</div>
      </div>
    </>
  );
};

export default CharacterSettingCard;
