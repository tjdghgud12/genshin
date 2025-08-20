"use client";

import { calculatorFormSchema } from "@/app/calculator/page";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { IArtifactSetsInfo } from "@/types/artifactType";
import { TypeMerge } from "@/types/globalType";
// import Image from "next/image";
import { DotBounsLoading } from "@/app/loading";
import { Switch } from "@/components/ui/switch";
import { ReactElement, useState } from "react";
import { z } from "zod";
import { Tooltip, TooltipContent, TooltipTrigger } from "../../../components/ui/tooltip";

type TArtifactSetInfo = z.infer<typeof calculatorFormSchema>["artifact"]["setInfo"][number];

interface IArtifactSetOptionCard {
  className: string;
  setInfo: Omit<TypeMerge<IArtifactSetsInfo, TArtifactSetInfo>, "options"> & {
    options: TypeMerge<IArtifactSetsInfo["options"][number], TArtifactSetInfo["options"][number]>[];
    numberOfParts: number;
    affix_list: { id: string; effect: string }[];
  };
  props?: Record<string, unknown>;
}

const ArtifactSetOptionCard = ({ className = "", setInfo, ..._props }: IArtifactSetOptionCard): ReactElement => {
  const [imgLoading, setImgLoading] = useState<boolean>(true);

  return (
    <Card className={`w-full border-0 border-gray-400 p-1 shadow-md bg-transparent ${className}`}>
      <CardContent className="p-1 text-gray-700 flex">
        {!imgLoading && <DotBounsLoading className="w-fit h-fit m-auto" dotClassName="size-4 stroke-8" />}
        <div className="w-[7vw] h-[7vw] flex flex-col relative">
          <Tooltip delayDuration={500}>
            <TooltipTrigger asChild>
              {/* <Image className={`${imgLoading ? "" : "hidden"}`} src={setInfo.icon} alt="" priority fill sizes="(max-width: 1200px) 7vw" onLoad={() => setImgLoading(true)} /> */}
              <div className={`w-full h-full ${imgLoading ? "" : "hidden"}`}>{setInfo.name.slice(0, 1)}</div>
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
          <Label className="font-bold mx-auto">
            {setInfo.name}({setInfo.numberOfParts})
          </Label>
          <div className="flex flex-col gap-2 my-auto">
            {setInfo.options
              .filter((o) => o.type !== "always")
              .map((option, i) => {
                return (
                  <div key={`${option.label}-${i}`} className="w-full flex gap-2">
                    <Label className="w-fit h-fit font-bold my-auto">
                      {option.label}({option.requiredParts}):
                    </Label>
                    {option.type === "stack" ? (
                      <Input
                        className="w-1/2 h-fit border-b-2 border-t-0 border-x-0 rounded-none text-center font-bold shadow-none focus-visible:ring-0 input-removeArrow my-auto p-0"
                        name={`options.${i}.stack`}
                        type="number"
                        value={option.stack}
                        min={0}
                        max={option.maxStack}
                        onChange={() => {}}
                      />
                    ) : (
                      <Switch
                        className="w-[50px]"
                        thumbClassName="data-[state=checked]:translate-x-[calc(50px-(100%+2px))] data-[state=unchecked]:translate-x-0" // translate-x의 값은 내부 원 크기 +2(즉, 기본 기준 18px)만큼 -연산 후 들어가야함
                        checked={option.active}
                        onCheckedChange={() => {}}
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

const ArtifactPartCard = (): ReactElement => {
  return <div>ArtifactPartCard</div>;
};

export { ArtifactPartCard, ArtifactSetOptionCard };
