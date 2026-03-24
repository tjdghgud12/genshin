"use client";

import GradientStar from "@/app/globalComponents/GradientStar";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Card, CardContent } from "@/components/ui/card";
import { Combobox, ComboboxContent, ComboboxEmpty, ComboboxInput, ComboboxItem, ComboboxList } from "@/components/ui/combobox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import api from "@/lib/axios";
import { calculatorCharacterInfoSchema } from "@/lib/calculator";
import { inputNumberWithSpace } from "@/lib/utils";
import { useWeaponInfoStore } from "@/store/weaponStore";
import { IWeaponInfo } from "@/types/weaponType";
import { Loader2 } from "lucide-react";
import Image from "next/image";
import React, { Fragment, useCallback, useEffect, useMemo, useState } from "react";
import { z } from "zod";

const weaponSubOption = {
  FIGHT_PROP_ATTACK_PERCENT: "공격력(%)",
  FIGHT_PROP_HP_PERCENT: "체력(%)",
  FIGHT_PROP_DEFENSE_PERCENT: "방어력(%)",
  FIGHT_PROP_CHARGE_EFFICIENCY: "원소 충전 효율(%)",
  FIGHT_PROP_ELEMENT_MASTERY: "원소 마스터리",
  FIGHT_PROP_CRITICAL: "치명타 확률(%)",
  FIGHT_PROP_CRITICAL_HURT: "치명타 피해(%)",
  FIGHT_PROP_PHYSICAL_ADD_HURT: "물리 피해 보너스(%)",
};

type TWeaponData = z.infer<typeof calculatorCharacterInfoSchema>["weapon"];
type TWeaponSubOptionKey = keyof typeof weaponSubOption;

interface IWeaponDetail {
  rank: number;
  icon: string;
  description: string;
  upgrade: { prop: Record<string, unknown>[] };
  affix: { name: string; upgrade: { level: number; description: string }[] } | null;
  [key: string]: unknown; // 나머지는 다 허용
}

const WeaponSettingCard = ({
  className = "",
  weapon = { id: 0, name: "", type: "WEAPON_SWORD_ONE_HAND", level: 0, refinement: 0, options: [] },
  onChange = (): void => {},
  onLevelChange = (): void => {},
  onRefinementChange = (): void => {},
  onOptionsChange = [],
}: {
  className?: string;
  weapon?: TWeaponData;
  onChange?: (weapon: TWeaponData | undefined) => void;
  onLevelChange?: (level: number | string) => void;
  onRefinementChange?: (refinement: number | string) => void;
  onOptionsChange?: ((value: boolean | number | string | null, key: string) => void)[];
}): React.ReactElement => {
  const totalWeaponList = useWeaponInfoStore((state) => state.weaponList);
  const [weaponDetail, setWeaponDetail] = useState<IWeaponDetail | null>(null);
  const [imgLoading, setImgLoading] = useState<boolean>(false);

  const getWeaponDetail = useCallback(async (id: number): Promise<void> => {
    api
      .get(`weapons/${id}`)
      .then((res) => {
        setWeaponDetail(res.data);
      })
      .catch((err) => console.error(err));
  }, []);

  const weaponList = useMemo(() => Object.values(totalWeaponList).filter((w) => w.type === weapon.type), [totalWeaponList, weapon.type]);
  const selectedWeapon = useMemo(() => weaponList.find((w) => w.id === weapon.id), [weaponList, weapon.id]);

  useEffect(() => {
    getWeaponDetail(weapon.id);
  }, [weapon.id, getWeaponDetail]);

  return (
    <Card className={`w-full max-h-full bg-gray-700 border-2 rounded-2xl overflow-y-auto scrollbar-custom shadow-none ${className}`} style={{ scrollbarGutter: "stable" }}>
      <CardContent className="w-full text-white">
        <div className="w-full flex">
          <div className="h-[8.5vw] min-h-[130px] aspect-square relative z-0 overflow-hidden">
            {!imgLoading && !weaponDetail && (
              <div className="w-full h-full flex">
                <Loader2 className="size-10 animate-spin m-auto" />
              </div>
            )}
            {weaponDetail ? (
              <Tooltip delayDuration={500}>
                <TooltipTrigger asChild>
                  <div className="w-full h-full relative overflow-hidden">
                    <div className={`w-[40%] pointer-events-none absolute inset-y-0 right-0 z-20 bg-linear-to-l from-gray-700 to-gray-700/0`} />
                    <div className={`w-[8%] pointer-events-none absolute inset-y-0 left-0 z-20 bg-linear-to-r from-gray-700 to-gray-700/0`} />
                    <div className={`h-[8%] pointer-events-none absolute inset-x-0 bottom-0 z-20 bg-linear-to-t from-gray-700 to-gray-700/0`} />
                    <div className="w-[10vw] h-[10vw] min-w-[150px] min-h-[150px] absolute z-0 -left-[20%] -top-[7%]">
                      <Image className={`object-cover`} src={weaponDetail.icon} alt="" priority fill sizes="(max-width: 1200px) 7vw" onLoad={() => setImgLoading(true)} />
                    </div>
                  </div>
                </TooltipTrigger>
                {weaponDetail.affix ? (
                  <TooltipContent className="max-w-[200px] bg-gray-500 fill-gray-500" side="right">
                    <Label className="font-bold mb-3">{weaponDetail.affix.name}</Label>
                    <Label className="leading-normal">{weaponDetail.affix.upgrade[Number(weapon.refinement) > 1 ? Number(weapon.refinement) - 1 : 0].description}</Label>
                  </TooltipContent>
                ) : (
                  <></>
                )}
              </Tooltip>
            ) : (
              <></>
            )}
          </div>
          <div className="w-[60%] flex flex-col justify-around">
            <div className="w-fit flex m-auto justify-around">
              {weaponDetail ? (
                Array.from({ length: weaponDetail.rank }).map((_, i) => (
                  <GradientStar key={`rank-${i}`} className="mx-0.5" size={23} outlined from="#Ef9FaF" to="#AFE8FB" middle="#AFE8FB" />
                ))
              ) : (
                <></>
              )}
            </div>
            <Combobox
              items={weaponList}
              value={selectedWeapon}
              itemToStringLabel={(weapon) => weapon.name}
              onValueChange={(weapon) => {
                if (weapon) {
                  setImgLoading(false);
                  getWeaponDetail(Number(weapon?.id));
                  onChange(weaponList.find((w) => w.id === Number(weapon?.id)));
                }
              }}
            >
              <ComboboxInput
                className="w-full h-fit bg-gray-700 text-white font-bold border-2 text-center"
                inputClassName="text-lg!"
                placeholder="무기"
                onKeyDown={(e) => {
                  if (e.key === "Enter") e.preventDefault();
                }}
              />
              <ComboboxContent className="bg-gray-700 text-white">
                <ComboboxEmpty>검색 결과가 없습니다.</ComboboxEmpty>
                <ComboboxList>
                  {(item: IWeaponInfo) => (
                    <ComboboxItem key={item.id} value={item}>
                      {item.name}
                    </ComboboxItem>
                  )}
                </ComboboxList>
              </ComboboxContent>
            </Combobox>
            {weaponDetail && (
              <Label className="m-auto text-lg font-bold">
                {weaponDetail.upgrade.prop[1] ? weaponSubOption[weaponDetail.upgrade.prop[1].propType as TWeaponSubOptionKey] : ""}
              </Label>
            )}
          </div>
        </div>

        <div className="w-full flex mt-1 mb-1">
          <div className="w-1/2 flex m-auto">
            <Label className="w-fit text-xl font-bold my-auto pr-2">Lv: </Label>
            <Input
              className="w-auto h-fit border-b-2 border-t-0 border-x-0 rounded-none text-lg1 text-center font-bold shadow-none focus-visible:ring-0 input-removeArrow my-auto p-0"
              name="level"
              type="number"
              value={weapon.level}
              min={1}
              max={90}
              placeholder="Lv"
              onChange={(e) => {
                const value = inputNumberWithSpace(e.target.value);
                onLevelChange(Number(value) > 90 ? 90 : value);
              }}
            />
          </div>
          <div className="w-1/2 flex m-auto">
            <Label className="w-fit text-xl font-bold my-auto pr-2">재련: </Label>
            <Input
              className="w-auto h-fit border-b-2 border-t-0 border-x-0 rounded-none text-lg! text-center font-bold shadow-none focus-visible:ring-0 input-removeArrow my-auto p-0"
              name="refinement"
              type="number"
              value={weapon.refinement}
              min={1}
              max={5}
              placeholder="재련"
              onChange={(e) => {
                const value = inputNumberWithSpace(e.target.value);
                onRefinementChange(Number(value) > 5 ? 5 : value);
              }}
            />
          </div>
        </div>

        <Label className="text-base mt-3">{weaponDetail?.description}</Label>

        <Accordion className="w-full" type="single" collapsible defaultValue="description">
          <AccordionItem value="description">
            <AccordionTrigger className="pt-1">{weaponDetail && weaponDetail.affix && <Label className="font-bold text-xl">{weaponDetail.affix.name}</Label>}</AccordionTrigger>
            <AccordionContent className="flex flex-col gap-4 scrollbar-custom whitespace-pre-wrap">
              {weaponDetail && weaponDetail.affix && (
                <Label className="text-base">{weaponDetail.affix.upgrade[Number(weapon.refinement) > 1 ? Number(weapon.refinement) - 1 : 0].description}</Label>
              )}
            </AccordionContent>
          </AccordionItem>
        </Accordion>

        <div className="h-fit mt-3">
          {weapon ? (
            <>
              {weapon.options.length ? <Label className="text-2xl font-bold mb-1">옵션</Label> : <></>}
              <div className="grid grid-cols-[auto_1fr] gap-x-3">
                {weapon.options.map((option, i) => {
                  const optionValue = weapon.options[i];
                  return option.type === "toggle" ? (
                    <Fragment key={`${weapon.name}-${option.label}-${i}`}>
                      <Label className="text-xl font-bold my-auto">{option.label}:</Label>
                      <Switch
                        className="w-[50px] h-[22px] my-auto"
                        thumbClassName="data-[state=checked]:translate-x-[calc(50px-(100%+4px))] data-[state=unchecked]:translate-x-0" // translate-x의 값은 내부 원 크기 +2(즉, 기본 기준 18px)만큼 -연산 후 들어가야함
                        checked={optionValue.active}
                        onCheckedChange={(checked) => onOptionsChange[i](checked, "active")}
                      />
                    </Fragment>
                  ) : option.type === "stack" ? (
                    <Fragment key={`${weapon.name}-${option.label}-${i}`}>
                      <Label className="text-xl font-bold my-auto">{option.label}:</Label>
                      <Input
                        className="w-fit text-lg! border-b-2 border-t-0 border-x-0 rounded-none text-center font-bold focus-visible:ring-0 input-removeArrow p-0 mx-0 mt-auto mb-2"
                        name={`options.${i}`}
                        type="number"
                        value={optionValue.stack.toString()}
                        min={0}
                        max={option.maxStack}
                        placeholder="중첩"
                        onChange={(e) => {
                          const value = inputNumberWithSpace(e.target.value);
                          onOptionsChange[i](value, "stack");
                        }}
                      />
                    </Fragment>
                  ) : option.type === "select" ? (
                    <Fragment key={`${weapon.name}-${option.label}-${i}`}>
                      <Label className="text-xl font-bold my-auto">{option.label}:</Label>
                      <div className="w-full">
                        <Combobox
                          items={option.selectList.map((w) => ({ label: w, value: w }))}
                          itemToStringValue={(label: { label: string; value: string }) => label.label}
                          value={{ label: option.select ?? "", value: option.select ?? "" }}
                          onValueChange={(option) => {
                            if (option) {
                              onOptionsChange[i](option?.value === undefined ? null : option?.value, "select");
                            }
                          }}
                        >
                          <ComboboxInput
                            className="w-full h-fit bg-gray-700 text-white font-bold border-2"
                            inputClassName="text-lg!"
                            placeholder={option.label}
                            onKeyDown={(e) => {
                              if (e.key === "Enter") e.preventDefault();
                            }}
                          />
                          <ComboboxContent className="bg-gray-700 text-white">
                            <ComboboxEmpty>검색 결과가 없습니다.</ComboboxEmpty>
                            <ComboboxList>
                              {(item: { label: string; value: string }) => (
                                <ComboboxItem key={item.value} value={item}>
                                  {item.label}
                                </ComboboxItem>
                              )}
                            </ComboboxList>
                          </ComboboxContent>
                        </Combobox>
                      </div>
                    </Fragment>
                  ) : (
                    <Fragment key={`${weapon.name}-${option.label}-${i}`} />
                  );
                })}
              </div>
            </>
          ) : (
            <></>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default WeaponSettingCard;
