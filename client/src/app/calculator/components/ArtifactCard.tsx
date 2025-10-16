"use client";

import { Combobox } from "@/app/globalComponents/ComboBox";
import { DotBounsLoading } from "@/app/loading";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import api from "@/lib/axios";
import { calculatorCharacterInfoSchema } from "@/lib/calculator";
import { fightPropLabels } from "@/lib/fightProps";
import { inputNumberWithSpace } from "@/lib/utils";
import { useCalculatorStore } from "@/store/useCalculatorStore";
import { IArtifactOptionInfo, IArtifactSetsInfo } from "@/types/artifactType";
import { TypeMerge } from "@/types/globalType";
import { CircleOff } from "lucide-react";
import Image from "next/image";
import { Fragment, ReactElement, useCallback, useEffect, useState } from "react";
import { z } from "zod";

type TArtifactSetInfo = z.infer<typeof calculatorCharacterInfoSchema>["artifact"]["setInfo"][number];
type TArtifactPartInfo = z.infer<typeof calculatorCharacterInfoSchema>["artifact"]["parts"][number];

interface IArtifactSetOptionCard {
  className: string;
  setInfo: Omit<TypeMerge<IArtifactSetsInfo, TArtifactSetInfo>, "options"> & {
    options: TypeMerge<IArtifactSetsInfo["options"][number], TArtifactSetInfo["options"][number]>[];
    numberOfParts: number;
    affix_list: { id: string; effect: string }[];
  };
  onChnage: ((val: number | string | boolean) => void)[];
}

interface IArtifactPartCard {
  className: string;
  main: IArtifactOptionInfo;
  artifact: TArtifactPartInfo;
  sub: IArtifactOptionInfo[];
  onSetChange?: (value: string) => void;
  onMainChange?: (val: Record<string, string | number>) => void;
  onSubChange?: ((val: Record<string, string | number>) => void)[];
}

interface IArtifactPart {
  description: string;
  icon: string;
  name: string;
  pos: string;
  [key: string]: unknown;
}

const ArtifactSetOptionCard = ({ className = "", setInfo, onChnage = [] }: IArtifactSetOptionCard): ReactElement => {
  const [imgLoading, setImgLoading] = useState<boolean>(true);

  return (
    <Card className={`w-full border-0 border-gray-400 p-1 shadow-md bg-transparent ${className}`}>
      <CardContent className="p-1 text-white flex">
        {!imgLoading && <DotBounsLoading className="w-fit h-fit m-auto" dotClassName="size-4 stroke-8" />}
        <div className="w-[40%] aspect-square mr-2 my-auto relative">
          <Tooltip delayDuration={500}>
            <TooltipTrigger asChild>
              <Image className={`${imgLoading ? "" : "hidden"}`} src={setInfo.icon} alt="" priority fill sizes="(max-width: 1200px) 7vw" onLoad={() => setImgLoading(true)} />
            </TooltipTrigger>
            <TooltipContent className="max-w-[200px] bg-gray-500 fill-gray-500" side="right">
              {setInfo.affix_list.map((affix, i) => {
                return (
                  <Label key={`artifact-affix-${i}`} className={`leading-normal ${i ? "" : "mb-3"}`}>
                    {i ? 4 : 2}세트 : {affix.effect}
                  </Label>
                );
              })}
            </TooltipContent>
          </Tooltip>
        </div>

        <div className="flex-1 flex flex-col gap-5">
          <Label className="text-2xl font-bold mx-auto">
            {setInfo.name}({setInfo.numberOfParts})
          </Label>
          <div className="flex flex-col gap-2 my-auto overflow-auto" style={{ scrollbarGutter: "stable" }}>
            {setInfo.options.map((option, i) => {
              if (option.type === "always" || option.requiredParts > setInfo.numberOfParts) {
                return <Fragment key={`${option.label}-${i}`} />;
              }
              return (
                <div key={`${option.label}-${i}`} className="w-full flex gap-2">
                  <Label className="w-[50%] text-base font-bold my-auto">
                    {option.label}({option.requiredParts}):
                  </Label>
                  {option.type === "stack" ? (
                    <Input
                      className="h-fit border-b-2 border-t-0 border-x-0 rounded-none !text-lg text-center font-bold shadow-none focus-visible:ring-0 input-removeArrow my-auto p-0 flex-1"
                      name={`options.${i}.stack`}
                      type="number"
                      value={option.stack.toString()}
                      min={0}
                      max={option.maxStack}
                      placeholder="중첩"
                      onChange={(val) => onChnage[i](val.target.value)}
                    />
                  ) : (
                    <Switch
                      className="w-[50px] my-auto"
                      thumbClassName="data-[state=checked]:translate-x-[calc(50px-(100%+2px))] data-[state=unchecked]:translate-x-0" // translate-x의 값은 내부 원 크기 +2(즉, 기본 기준 18px)만큼 -연산 후 들어가야함
                      checked={option.active}
                      onClick={() => onChnage[i](!option.active)}
                    />
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

const ArtifactPartCard = ({ className, artifact, main, sub, onSetChange = (): void => {}, onMainChange = (): void => {}, onSubChange = [] }: IArtifactPartCard): ReactElement => {
  const artifactSets = useCalculatorStore((store) => store.artifactSets);
  const [ambrArtifact, setAmbrArtifact] = useState<IArtifactPart | undefined>();
  const [imgLoading, setImgLoading] = useState<boolean>(false);

  const artifactSubOptionList = [
    `FIGHT_PROP_HP`,
    `FIGHT_PROP_HP_PERCENT`,
    `FIGHT_PROP_DEFENSE`,
    `FIGHT_PROP_DEFENSE_PERCENT`,
    `FIGHT_PROP_ATTACK`,
    `FIGHT_PROP_ATTACK_PERCENT`,
    `FIGHT_PROP_CRITICAL`,
    `FIGHT_PROP_CRITICAL_HURT`,
    `FIGHT_PROP_ELEMENT_MASTERY`,
    `FIGHT_PROP_CHARGE_EFFICIENCY`,
  ];
  const artifactMainOptionBaseList: string[] = [`FIGHT_PROP_ATTACK_PERCENT`, `FIGHT_PROP_DEFENSE_PERCENT`, `FIGHT_PROP_HP_PERCENT`, `FIGHT_PROP_ELEMENT_MASTERY`];
  const artifactMainOptionList: Record<string, string | string[]> = {
    EQUIP_BRACER: "FIGHT_PROP_HP",
    EQUIP_NECKLACE: "FIGHT_PROP_ATTACK",
    EQUIP_SHOES: [...artifactMainOptionBaseList, `FIGHT_PROP_CHARGE_EFFICIENCY`],
    EQUIP_RING: [
      ...artifactMainOptionBaseList,
      "FIGHT_PROP_PHYSICAL_ADD_HURT",
      "FIGHT_PROP_FIRE_ADD_HURT",
      "FIGHT_PROP_ELEC_ADD_HURT",
      "FIGHT_PROP_WATER_ADD_HURT",
      "FIGHT_PROP_GRASS_ADD_HURT",
      "FIGHT_PROP_WIND_ADD_HURT",
      "FIGHT_PROP_ROCK_ADD_HURT",
      "FIGHT_PROP_ICE_ADD_HURT",
    ],
    EQUIP_DRESS: [...artifactMainOptionBaseList, `FIGHT_PROP_CRITICAL`, `FIGHT_PROP_CRITICAL_HURT`, `FIGHT_PROP_HEAL_ADD`],
  };

  const getArtifactDetail = useCallback(
    async (id: number): Promise<void> => {
      api
        .get(`artifactsets/${id}`)
        .then((res) => {
          if (res.status === 200) {
            const newArtifact = (res.data.suit as IArtifactPart[]).find((a) => a.pos === artifact.type);
            if (newArtifact) setAmbrArtifact(newArtifact);
          }
        })
        .catch((err) => {
          setImgLoading(true);
          console.log(err);
        });
    },
    [artifact.type],
  );

  useEffect(() => {
    getArtifactDetail(artifactSets[artifact.setName]?.id || 0);
  }, [artifactSets, artifact.setName, getArtifactDetail]);

  return (
    <Card className={`w-full border-0 border-gray-400 text-base p-1 shadow-md bg-transparent ${className}`}>
      <CardContent className="w-full h-full p-1 text-white flex flex-col gap-4 overflow-hidden">
        <div className="w-full flex">
          <div className="w-[45%] aspect-square flex flex-col relative">
            {!imgLoading && <DotBounsLoading className="w-auto h-auto m-auto" dotClassName="size-4 stroke-8" />}
            {ambrArtifact === undefined ? (
              <CircleOff className="size-10 m-auto" />
            ) : (
              <Image
                className={imgLoading ? "" : "hidden"}
                src={ambrArtifact?.icon || ""}
                alt=""
                priority
                fill
                sizes="(max-width: 1200px) 7vw"
                onLoad={() => setImgLoading(true)}
              />
            )}
          </div>
          <div className="w-[55%] h-full flex flex-col justify-between">
            <Combobox
              className="h-fit bg-gray-700 text-white text-base font-bold border-2"
              optionClassName="bg-gray-700 text-white"
              options={Object.keys(artifactSets).map((name) => ({ label: name, data: name }))}
              defaultValue={artifactSets[artifact.setName]?.name.toString() || ""}
              placeholder="성유물 세트"
              onChange={(name) => {
                if (name) {
                  const artifactInfo = artifactSets[name];
                  setAmbrArtifact(undefined);
                  setImgLoading(false);
                  onSetChange(name);
                  getArtifactDetail(Number(artifactInfo.id));
                }
              }}
            />

            {artifact && (
              <div className="min-w-0 flex flex-col">
                {Array.isArray(artifactMainOptionList[artifact.type]) ? (
                  <Combobox
                    className="h-fit bg-gray-700 text-white text-base font-bold border-2 overflow-hidden text-center"
                    optionClassName="bg-gray-700 text-white"
                    options={(artifactMainOptionList[artifact.type] as string[]).map((o) => ({
                      label: fightPropLabels[o],
                      data: o,
                    }))}
                    defaultValue={main.key}
                    onChange={(fightProp) => onMainChange({ [fightProp === undefined ? artifactMainOptionList[artifact.type][0] : fightProp]: main.value })}
                  />
                ) : (
                  <div className="w-full rounded-sm bg-gray-700 text-white font-bold border-2 text-center py-1 truncate">{fightPropLabels[main.key]}</div>
                )}
                <Input
                  className="w-full h-fit border-b-2 border-t-0 border-x-0 rounded-none !text-base text-center font-bold shadow-none focus-visible:ring-0 input-removeArrow mt-1 p-0"
                  name={`mainOption.value`}
                  type="number"
                  step="any"
                  value={main.value}
                  min={0}
                  placeholder={fightPropLabels[main.key]}
                  onChange={(e) => {
                    onMainChange({ [main.key]: inputNumberWithSpace(e.target.value, fightPropLabels[main.key].includes("%"), 2) });
                  }}
                />
              </div>
            )}
          </div>
        </div>
        <div className="flex-1 flex flex-col justify-around mx-auto">
          {sub.map(({ key, value }, i) => {
            return (
              <div key={`subOption.${i}`} className="w-full flex gap-2">
                <Combobox
                  className="w-2/3 h-fit bg-gray-700 text-white text-base font-bold border-2 overflow-hidden text-center"
                  optionClassName="bg-gray-700 text-white"
                  options={artifactSubOptionList.map((o) => ({
                    label: fightPropLabels[o],
                    data: o,
                  }))}
                  defaultValue={key}
                  onChange={(fightProp) => onSubChange[i]({ [fightProp === undefined ? artifactSubOptionList[0] : fightProp]: value })}
                />
                <Input
                  className="border-b-2 border-t-0 border-x-0 rounded-none !text-base text-center font-bold shadow-none focus-visible:ring-0 input-removeArrow mt-auto p-0"
                  name={`subOption.${i}.value`}
                  type="number"
                  step="any"
                  value={value}
                  min={0}
                  placeholder={fightPropLabels[key]}
                  onChange={(e) => {
                    if (onSubChange[i]) onSubChange[i]({ [key]: inputNumberWithSpace(e.target.value, true, 2) });
                  }}
                />
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
};

export { ArtifactPartCard, ArtifactSetOptionCard };
