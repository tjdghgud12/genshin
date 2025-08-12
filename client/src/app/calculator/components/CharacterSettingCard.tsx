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
          <div className={`w-[5vw] h-[5vw] border-3 bg-gray-500 rounded-full border-white flex justify-center relative`}>
            <Image src={icon} alt="" priority fill sizes="(max-width: 768px) 5vw, (max-width: 1200px) 50vw, 5vw" />
          </div>
        ) : (
          <Fragment>
            <Button
              className={`w-[5vw] h-[5vw] border-3 bg-gray-500 rounded-full relative ${active ? "border-white" : "border-stone-400"} hover:bg-gray-800`}
              disabled={!unlocked}
              onClick={onClick}
            >
              <Image src={icon} alt="" priority fill sizes="(max-width: 768px) 5vw, (max-width: 1200px) 50vw, 5vw" />
            </Button>

            {type === "stack" && (
              <Popover>
                <PopoverTrigger asChild>
                  <Button className="bg-transparent shadow-none mb-auto text-stone-700 hover:text-white hover:bg-transparent" size={"icon"}>
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
  const { passiveSkill, activeSkill, constellations } = useWatch({ control: form.control, name: `data.${index}` });

  return (
    <>
      <div className={`w-1/2 h-[500px] bg-right bg-size-[125%] bg-no-repeat flex px-8 py-3`}>
        {/* <div className={`w-1/2 h-[500px] bg-right bg-size-[125%] bg-no-repeat opacity-90 flex`} style={{ backgroundImage: `url('${rawInfo.icon.gacha}')` }}> */}
        <div className="mr-auto flex flex-col">
          <FormField
            control={form.control}
            name={`data.${index}.level`}
            render={({ field }) => (
              <FormItem className="w-fit mb-auto mx-auto justify-start">
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

          {item.passiveSkill.map((passive, j) => {
            const passiveInfo = item.raw.passiveSkill[j];
            // 여기서 on/off에 맞춰서 변경하자.
            // 클릭으로 on/off
            // 스텍값 입력은?????? 아래에 뭔가 추가해야하는데 그건 어캄???
            // 여기서 선택적 랜더링 들어가야겠네
            // 버튼 내부에 가능한가???? 인풋이
            // 아 클릭이 되네.
            // 음 스텍인 경우는 어떻게 처리할까. 애매허이
            // 음 버튼 클릭 영역이 자식쪽이냐 아니냐로 갈릴꺼같은데,
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

                        {/* <Button
                          className={`w-[5vw] h-[5vw] border-3 bg-gray-500 rounded-full ${passiveSkill[j].active ? "border-white" : "border-stone-400"} hover:bg-gray-800`}
                          disabled={!passive.unlocked}
                          onClick={() => {
                            form.setValue(`data.${index}.passiveSkill.${j}`, { ...passive, active: !passive.active });
                          }}
                        >
                          <Image src={passiveInfo.icon} alt="" priority width={60} height={60} />
                        </Button> */}
                      </FormControl>
                    </div>
                    <FormMessage />
                  </FormItem>
                )}
              />
            );
          })}
        </div>
        <div className="h-full flex flex-col">
          <div>평타</div>
          <div>원소 전투</div>
          <div>원소 폭발</div>
        </div>
        <div className="h-full flex flex-col">
          <div>1돌</div>
          <div>2돌</div>
          <div>3돌</div>
          <div>4돌</div>
          <div>5돌</div>
          <div>6돌</div>
        </div>
      </div>
      <div className="w-1/2">무기 성유물 영역</div>
    </>
  );
};

export default CharacterSettingCard;
