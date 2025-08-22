"use client";

import { calculatorFormSchema } from "@/app/calculator/page";
import { Combobox } from "@/app/globalComponents/ComboBox";
import { DotBounsLoading } from "@/app/loading";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import api from "@/lib/axios";
import { fightPropLabels } from "@/lib/fightProps";
import { inputNumberWithSpace } from "@/lib/utils";
import { useCalculatorStore } from "@/store/useCalculatorStore";
import { IArtifactOptionInfo, IArtifactSetsInfo } from "@/types/artifactType";
import { TypeMerge } from "@/types/globalType";
import { CircleOff } from "lucide-react";
import Image from "next/image";
import { Fragment, ReactElement, useCallback, useEffect, useState } from "react";
import { z } from "zod";

type TArtifactSetInfo = z.infer<typeof calculatorFormSchema>["artifact"]["setInfo"][number];
type TArtifactPartInfo = z.infer<typeof calculatorFormSchema>["artifact"]["parts"][number];

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
  onMainChange?: (val: Record<string, string | number>) => void;
  onSubChange?: ((val: Record<string, string | number>) => void)[];
}

interface IArtifactPart {
  description: string | null;
  icon: string | null;
  name: string | null;
  pos: string | null;
  [key: string]: unknown;
}

const ArtifactSetOptionCard = ({ className = "", setInfo, onChnage = [] }: IArtifactSetOptionCard): ReactElement => {
  const [imgLoading, setImgLoading] = useState<boolean>(true);

  return (
    <Card className={`w-full border-0 border-gray-400 p-1 shadow-md bg-transparent ${className}`}>
      <CardContent className="p-1 text-gray-700 flex">
        {!imgLoading && <DotBounsLoading className="w-fit h-fit m-auto" dotClassName="size-4 stroke-8" />}
        <div className="w-[40%] aspect-square mr-2 my-auto relative">
          <Tooltip delayDuration={500}>
            <TooltipTrigger asChild>
              <Image className={`${imgLoading ? "" : "hidden"}`} src={setInfo.icon} alt="" priority fill sizes="(max-width: 1200px) 7vw" onLoad={() => setImgLoading(true)} />
              {/* <div className={`w-full h-full ${imgLoading ? "" : "hidden"}`}>{setInfo.name.slice(0, 1)}</div> */}
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
          <Label className="text-base font-bold mx-auto">
            {setInfo.name}({setInfo.numberOfParts})
          </Label>
          <div className="flex flex-col gap-2 my-auto">
            {setInfo.options.map((option, i) => {
              if (option.type === "always") {
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

const ArtifactPartCard = ({ className, artifact, main, sub, onMainChange = (): void => {}, onSubChange = [] }: IArtifactPartCard): ReactElement => {
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
            const artifacts = res.data.suit as IArtifactPart[];
            setAmbrArtifact(artifacts.find((a) => a.pos === artifact.type));
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
    getArtifactDetail(artifactSets.find((set) => set.name === artifact.setName)?.id || 0);
  }, [artifactSets, artifact.setName, getArtifactDetail]);

  return (
    <Card className={`w-full border-0 border-gray-400 text-base p-1 shadow-md bg-transparent ${className}`}>
      <CardContent className="w-full h-full p-1 text-gray-700 flex overflow-hidden">
        <div className="w-2/5 flex flex-col mr-2">
          <Combobox
            className="w-full h-fit bg-gray-700 text-white font-bold border-2"
            optionClassName="bg-gray-700 text-white"
            options={artifactSets.map((set) => ({ label: set.name, data: set.id.toString(), raw: set }))}
            defaultValue={artifactSets.find((set) => set.name === artifact.setName)?.id.toString() || ""}
            placeholder="성유물 세트"
            onChange={(id) => {
              setAmbrArtifact(undefined);
              setImgLoading(false);
              getArtifactDetail(Number(id));
            }}
          />
          <div className="w-full flex mt-auto">
            <div className="w-[40%] aspect-square flex flex-col relative">
              {!imgLoading && <DotBounsLoading className="w-fit h-fit m-auto" dotClassName="size-4 stroke-8" />}
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
            {artifact && (
              <div className="flex-1 min-w-0 mt-auto flex flex-col">
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
                  value={main.value}
                  min={0}
                  placeholder={fightPropLabels[main.key]}
                  onChange={(e) => {
                    onMainChange({ [main.key]: inputNumberWithSpace(e.target.value, fightPropLabels[main.key].includes("%"), 2) });
                  }}
                  onBlur={(e) => {
                    onMainChange({ [main.key]: inputNumberWithSpace(Number(e.target.value).toFixed(2), fightPropLabels[main.key].includes("%"), 2) });
                  }}
                />
              </div>
            )}
          </div>
        </div>
        <div className="flex-1 grid grid-cols-2 gap-2">
          {sub.map(({ key, value }, i) => {
            return (
              <div key={`subOption.${i}`} className="flex flex-col">
                <Combobox
                  className="h-fit bg-gray-700 text-white font-bold border-2 overflow-hidden text-center"
                  optionClassName="bg-gray-700 text-white"
                  options={artifactSubOptionList.map((o) => ({
                    label: fightPropLabels[o],
                    data: o,
                  }))}
                  defaultValue={key}
                  onChange={(fightProp) => onSubChange[i]({ [fightProp === undefined ? artifactSubOptionList[0] : fightProp]: value })}
                />
                <Input
                  className="w-full h-fit border-b-2 border-t-0 border-x-0 rounded-none !text-base text-center font-bold shadow-none focus-visible:ring-0 input-removeArrow mt-auto p-0"
                  name={`subOption.${i}.value`}
                  type="number"
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
