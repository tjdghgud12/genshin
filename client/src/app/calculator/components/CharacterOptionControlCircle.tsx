import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { inputNumberWithSpace } from "@/lib/utils";
import { Arrow } from "@radix-ui/react-popover";
import { Settings } from "lucide-react";
import Image from "next/image";
import React from "react";

const CharacterOptionControlCircle = ({
  name = "",
  description = "",
  unlocked = false,
  options = [],
  icon = "",
  useLevel = false,
  level = 1,
  onClick = (): void => {},
  onChange = (): void => {},
  onLevelChange = (): void => {},
}: {
  unlocked: boolean;
  name?: string;
  description?: string;
  options: {
    type: "always" | "toggle" | "stack" | string;
    active: boolean;
    maxStack: number;
    stack: number;
    inputLabel: string;
  }[];
  icon: string;
  useLevel?: boolean;
  level?: number | string;
  onClick?: () => void;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>, index: number) => void;
  onLevelChange?: (level: number | string) => void;
}): React.ReactElement => {
  return (
    <div className="w-fit h-fit flex">
      <Tooltip delayDuration={500}>
        <TooltipTrigger asChild>
          {options.every((o) => o.type === "always") ? (
            <div
              className={`w-[5vw] h-[5vw] min-w-16 min-h-16 border-3 bg-gray-500 rounded-full ${unlocked ? "border-white" : "border-gray-600 opacity-50"} flex justify-center relative`}
            >
              <Image src={icon} alt="" priority fill sizes="(max-width: 768px) 5vw, (max-width: 1200px) 50vw, 5vw" />
            </div>
          ) : (
            <Button
              className={`w-[5vw] h-[5vw] min-w-16 min-h-16 border-3 bg-gray-500 rounded-full relative ${options.every((o) => o.active) && unlocked ? "border-white" : "border-gray-600"} hover:bg-gray-800`}
              type="button"
              disabled={!unlocked}
              onClick={onClick}
            >
              <Image src={icon} alt="" priority fill sizes="(max-width: 768px) 5vw, (max-width: 1200px) 50vw, 5vw" />
            </Button>
          )}
        </TooltipTrigger>
        <TooltipContent className="w-full max-w-[200px] bg-gray-500 fill-gray-500" side="right">
          <p className="font-bold">{name}</p>
          <p className="mb-2">{description}</p>
        </TooltipContent>
      </Tooltip>
      <div className="flex flex-col">
        {options.some((o) => o.type === "stack") && (
          <Popover>
            <PopoverTrigger asChild>
              <Button disabled={!unlocked} className="w-fit bg-transparent shadow-none mb-auto text-stone-700 hover:text-white hover:bg-transparent" size={"icon"}>
                <Settings className="size-6" />
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-fit rounded-xl border-2 bg-gray-600 text-white" side="right">
              <Arrow />
              {options.map((o, i) => {
                return (
                  <div key={`skill-option-${o.inputLabel}`} className="flex">
                    <Label className="my-auto mr-3">{o.inputLabel}:</Label>
                    <Input
                      type="number"
                      className="w-auto max-w-[100px] border-x-0 border-t-0 shadow-none focus-visible:ring-0 rounded-none input-removeArrow text-center"
                      value={o.stack}
                      max={o.maxStack}
                      min={0}
                      placeholder="중첩"
                      onChange={(e) => onChange(e, i)}
                    />
                  </div>
                );
              })}
            </PopoverContent>
          </Popover>
        )}
        {useLevel && (
          <Input
            className="size-6 border-b-2 border-t-0 border-x-0 rounded-none text-center font-bold focus-visible:ring-0 input-removeArrow p-0 mx-0 mt-auto mb-2"
            placeholder="Lv"
            type="number"
            value={level.toString()}
            max={10}
            min={0}
            onChange={(e) => {
              const value = inputNumberWithSpace(e.target.value);
              onLevelChange(Number(value) > 10 ? 10 : value);
            }}
          />
        )}
      </div>
    </div>
  );
};

export default CharacterOptionControlCircle;
