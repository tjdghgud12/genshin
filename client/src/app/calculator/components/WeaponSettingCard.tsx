"use client";

import { Combobox } from "@/app/globalComponents/ComboBox";
import GradientStar from "@/app/globalComponents/GradientStar";
import { DotBounsLoading } from "@/app/loading";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import api from "@/lib/axios";
import { calculatorCharacterInfoSchema } from "@/lib/calculator";
import { inputNumberWithSpace } from "@/lib/utils";
import { useCalculatorStore } from "@/store/useCalculatorStore";
import { IWeaponInfo } from "@/types/weaponType";
import Image from "next/image";
import React, { useCallback, useEffect, useState } from "react";
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
  type = "WEAPON_SWORD_ONE_HAND",
  weapon = { id: 0, name: "string", level: 0, refinement: 0, options: [] },
  onChange = (): void => {},
  onLevelChange = (): void => {},
  onRefinementChange = (): void => {},
  onOptionsChange = [],
}: {
  className?: string;
  type?: string;
  weapon?: TWeaponData;
  onChange?: (weapon: IWeaponInfo | undefined) => void;
  onLevelChange?: (level: number | string) => void;
  onRefinementChange?: (refinement: number | string) => void;
  onOptionsChange?: ((value: boolean | number | string) => void)[];
}): React.ReactElement => {
  const totalWeaponList = useCalculatorStore((state) => state.weaponList);
  const [weaponDetail, setWeaponDetail] = useState<IWeaponDetail | null>(null);
  const [imgLoading, setImgLoading] = useState<boolean>(false);
  const [weaponList, setWeaponList] = useState<IWeaponInfo[]>([]);
  const [selectedWeapon, setSelectedWeapon] = useState<IWeaponInfo | undefined>(undefined);

  const getWeaponDetail = useCallback(async (id: number): Promise<void> => {
    api
      .get(`weapons/${id}`)
      .then((res) => {
        setWeaponDetail(res.data);
      })
      .catch((err) => console.log(err));
  }, []);

  useEffect(() => {
    getWeaponDetail(weapon.id);
  }, [weapon.id, getWeaponDetail]);

  useEffect(() => {
    const newWeaponList = Object.values(totalWeaponList).filter((w) => w.type === type);
    setWeaponList(newWeaponList);
    setSelectedWeapon(newWeaponList.find((w) => w.id === Number(weapon.id)));
  }, [totalWeaponList, type, weapon.id]);

  return (
    <Card className={`w-full h-full border-0 border-gray-400 p-1 shadow-md bg-transparent ${className}`}>
      <CardContent className="w-full h-full p-1 text-gray-700">
        <div className="w-full flex">
          <div className="w-[40%] aspect-square mr-2">
            {!imgLoading && !weaponDetail && <DotBounsLoading className="w-fit h-full m-auto" dotClassName="size-4 stroke-8" />}
            {weaponDetail ? (
              <Tooltip delayDuration={500}>
                <TooltipTrigger asChild>
                  <div className="w-full h-full relative">
                    <Image src={weaponDetail.icon} alt="" priority fill sizes="(max-width: 1200px) 7vw" onLoad={() => setImgLoading(true)} />
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
              className="w-full h-fit bg-gray-700 text-white font-bold border-2 text-xl text-center"
              optionClassName="bg-gray-700 text-white"
              options={weaponList.map((w) => ({ label: w.name, data: w.id, raw: w }))}
              defaultValue={weapon.id.toString()}
              placeholder="무기"
              onChange={(id) => {
                setImgLoading(false);
                getWeaponDetail(Number(id));

                const weapon = weaponList.find((w) => w.id === Number(id));
                setSelectedWeapon(weapon);
                onChange(weapon ? weapon : undefined);
              }}
            />
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
              className="w-auto h-fit border-b-2 border-t-0 border-x-0 rounded-none !text-lg text-center font-bold shadow-none focus-visible:ring-0 input-removeArrow my-auto p-0"
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
              className="w-auto h-fit border-b-2 border-t-0 border-x-0 rounded-none !text-lg text-center font-bold shadow-none focus-visible:ring-0 input-removeArrow my-auto p-0"
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
        <div>
          {selectedWeapon ? (
            selectedWeapon.options.map((option, i) => {
              const optionValue = weapon.options[i];
              return (
                <div key={weapon.name + option.label + i}>
                  {option.type === "toggle" ? (
                    <div className="w-fit flex mb-1">
                      <Label className="font-bold mr-3">{option.label}:</Label>
                      <Switch
                        className="w-[50px]"
                        thumbClassName="data-[state=checked]:translate-x-[calc(50px-(100%+2px))] data-[state=unchecked]:translate-x-0" // translate-x의 값은 내부 원 크기 +2(즉, 기본 기준 18px)만큼 -연산 후 들어가야함
                        checked={optionValue.active}
                        onCheckedChange={onOptionsChange[i]}
                      />
                    </div>
                  ) : option.type === "stack" ? (
                    <div className="flex mb-1">
                      <Label className="font-bold text-lg mr-1">{option.label}:</Label>
                      <Input
                        className="w-auto h-fit border-b-2 border-t-0 border-x-0 rounded-none !text-xl text-center font-bold shadow-none focus-visible:ring-0 input-removeArrow my-auto p-0"
                        name={`options.${i}`}
                        type="number"
                        value={optionValue.stack.toString()}
                        min={0}
                        max={option.maxStack}
                        placeholder="중첩"
                        onChange={(e) => {
                          const value = inputNumberWithSpace(e.target.value);
                          onOptionsChange[i](value);
                        }}
                      />
                    </div>
                  ) : (
                    <></>
                  )}
                </div>
              );
            })
          ) : (
            <></>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default WeaponSettingCard;
