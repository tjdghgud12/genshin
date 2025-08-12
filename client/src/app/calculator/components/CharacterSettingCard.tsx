"use Client";

import { calculatorFormSchema, formSchema } from "@/app/calculator/page";
import { Button } from "@/components/ui/button";
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Arrow } from "@radix-ui/react-popover";
import { Settings } from "lucide-react";
import Image from "next/image";
import React, { Fragment } from "react";
import { UseFormReturn, useWatch } from "react-hook-form";
import { z } from "zod";

const CharacterOptionControlCircle = ({
  type = "always",
  active = false,
  unlocked = false,
  stack = 0,
  maxStack = 1,
  inputLabel = "",
  onClick = (): void => {},
  onChange = (e: React.ChangeEvent<HTMLInputElement>): void => {},
  icon = "",
}: {
  type: "always" | "toggle" | "stack" | string;
  active: boolean;
  unlocked: boolean;
  stack: number;
  maxStack: number;
  inputLabel: string;
  onClick?: () => void;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  icon: string;
}): React.ReactElement => {
  return (
    <Fragment>
      <div className="w-fit h-fit flex">
        {type === "always" ? (
          <div
            className={`w-[5vw] h-[5vw] min-w-16 min-h-16 border-3 bg-gray-500 rounded-full ${unlocked ? "border-white" : "border-stone-400 opacity-50"} flex justify-center relative`}
          >
            <Image src={icon} alt="" priority fill sizes="(max-width: 768px) 5vw, (max-width: 1200px) 50vw, 5vw" />
          </div>
        ) : (
          <Fragment>
            <Button
              className={`w-[5vw] h-[5vw] min-w-16 min-h-16 border-3 bg-gray-500 rounded-full relative ${active && unlocked ? "border-white" : "border-stone-400"} hover:bg-gray-800`}
              disabled={!unlocked}
              onClick={onClick}
            >
              <Image src={icon} alt="" priority fill sizes="(max-width: 768px) 5vw, (max-width: 1200px) 50vw, 5vw" />
            </Button>

            {type === "stack" && (
              <Popover>
                <PopoverTrigger asChild>
                  <Button disabled={!unlocked} className="bg-transparent shadow-none mb-auto text-stone-700 hover:text-white hover:bg-transparent" size={"icon"}>
                    <Settings className="size-6 " />
                  </Button>
                </PopoverTrigger>
                <PopoverContent className="w-fit rounded-xl border-2 bg-gray-600 text-white flex" side="right">
                  <Arrow />
                  <p className="my-auto mr-3">{inputLabel}:</p>
                  <Input
                    className="w-auto max-w-[100px] border-x-0 border-t-0 shadow-none focus-visible:ring-0 rounded-none input-removeArrow text-center"
                    value={stack}
                    max={maxStack}
                    min={0}
                    onChange={onChange}
                  />
                </PopoverContent>
              </Popover>
            )}
          </Fragment>
        )}
      </div>
    </Fragment>
  );
};

const CharacterSettingCard = ({
  form,
  item,
  index,
}: {
  form: UseFormReturn<z.infer<typeof formSchema>>;
  item: z.infer<typeof calculatorFormSchema>;
  index: number;
}): React.ReactElement => {
  const { passiveSkill, activeSkill, constellations, raw } = useWatch({ control: form.control, name: `data.${index}` });

  return (
    <>
      <div className={`w-1/2 h-fit min-h-[500px] bg-right bg-size-[125%] bg-no-repeat flex flex-col px-8 py-3`}>
        {/* <div className={`w-1/2 h-fit min-h-[500px] bg-right bg-size-[125%] bg-no-repeat opacity-90 flex flex-col px-8 py-3`} style={{ backgroundImage: `url('${raw.icon.gacha}')` }}> */}
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
          <div className="mr-auto flex flex-col mt-auto">
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
                            type={passiveInfo.type}
                            active={passiveSkill[j].active}
                            unlocked={passive.unlocked}
                            stack={passive.stack}
                            maxStack={passiveInfo.maxStack}
                            inputLabel={passiveInfo.label}
                            icon={passiveInfo.icon}
                            onClick={() => form.setValue(`data.${index}.passiveSkill.${j}`, { ...passive, active: !passive.active })}
                            onChange={(e) => {
                              if (/^\d*$/.test(e.target.value)) {
                                const value = Number(e.target.value);
                                form.setValue(`data.${index}.passiveSkill.${j}`, { ...passive, stack: value > passiveInfo.maxStack ? passiveInfo.maxStack : value });
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
                            type={activeInfo.type}
                            active={activeSkill[j].active}
                            unlocked
                            stack={active.stack}
                            maxStack={activeInfo.maxStack}
                            inputLabel={activeInfo.label}
                            icon={activeInfo.icon}
                            onClick={() => form.setValue(`data.${index}.activeSkill.${j}`, { ...active, active: !active.active })}
                            onChange={(e) => {
                              if (/^\d*$/.test(e.target.value)) {
                                const value = Number(e.target.value);
                                form.setValue(`data.${index}.activeSkill.${j}`, {
                                  ...active,
                                  stack: value > activeInfo.maxStack ? activeInfo.maxStack : value,
                                });
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
                            type={constellationInfo.type}
                            active={constellations[j].active}
                            unlocked={constellation.unlocked}
                            stack={constellation.stack}
                            maxStack={constellationInfo.maxStack}
                            inputLabel={constellationInfo.label}
                            icon={constellationInfo.icon}
                            onClick={() => form.setValue(`data.${index}.constellations.${j}`, { ...constellation, active: !constellation.active })}
                            onChange={(e) => {
                              if (/^\d*$/.test(e.target.value)) {
                                const value = Number(e.target.value);
                                form.setValue(`data.${index}.constellations.${j}`, {
                                  ...constellation,
                                  stack: value > constellationInfo.maxStack ? constellationInfo.maxStack : value,
                                });
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
      <div className="w-1/2">무기 성유물 영역</div>
    </>
  );
};

export default CharacterSettingCard;
