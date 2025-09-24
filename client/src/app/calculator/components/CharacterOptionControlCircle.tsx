import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Switch } from "@/components/ui/switch";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { inputNumberWithSpace } from "@/lib/utils";
import { Arrow } from "@radix-ui/react-popover";
import { Settings } from "lucide-react";
import Image from "next/image";
import React, { Fragment } from "react";

type ToptionType = "always" | "toggle" | "stack" | string;

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
    type: ToptionType;
    active: boolean;
    maxStack: number;
    stack: number;
    inputLabel: string;
  }[];
  icon: string;
  useLevel?: boolean;
  level?: number | string;
  onClick?: () => void;
  onChange?: (value: string | boolean, index: number) => void;
  onLevelChange?: (level: number | string) => void;
}): React.ReactElement => {
  return (
    <div className="w-full h-fit flex mt-auto">
      <Tooltip delayDuration={500}>
        <TooltipTrigger asChild>
          {useLevel ? (
            <div
              className={`w-[70%] h-fit aspect-square flex-none min-w-16 min-h-16 border-3 bg-gray-500 rounded-full ${unlocked ? "border-white" : "border-gray-600 opacity-50"} flex justify-center relative mt-auto`}
            >
              <Image src={icon} alt="" priority fill sizes="(max-width: 768px) 5vw, (max-width: 1200px) 50vw, 5vw" />
            </div>
          ) : (
            <Button
              className={`w-[70%] h-fit aspect-square min-w-16 min-h-16 border-3 bg-gray-500 rounded-full relative ${unlocked ? "border-white" : "border-gray-600 opacity-70"} mt-auto hover:bg-gray-800`}
              type="button"
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
      <div className="flex flex-col flex-1">
        {options.length > 0 && (
          <Popover>
            <PopoverTrigger asChild>
              <Button
                disabled={!unlocked}
                className="w-[70%] aspect-square bg-transparent shadow-none text-stone-700 mb-auto hover:text-white hover:bg-transparent"
                size={"icon"}
                style={{ containerType: "size" }}
              >
                <Settings style={{ width: "100cqw", height: "100cqw" }} />
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-fit rounded-xl border-2 bg-gray-600 text-white grid grid-cols-[max-content_max-content] gap-1 items-start" side="right">
              <Arrow />
              {options
                .filter((o) => o.type !== "always")
                .map((o, i) => {
                  return (
                    <Fragment key={`skill-option-${o.inputLabel}`}>
                      <Label className="w-fit my-auto">{o.inputLabel}:</Label>
                      {o.type === "toggle" ? (
                        <Switch defaultChecked={o.active} onCheckedChange={(e) => onChange(e, i)} />
                      ) : (
                        <Input
                          type="number"
                          className="w-fit border-x-0 border-t-0 shadow-none focus-visible:ring-0 rounded-none input-removeArrow text-center"
                          value={o.stack}
                          max={o.maxStack}
                          min={0}
                          placeholder="중첩"
                          onChange={(e) => onChange(e.target.value, i)}
                        />
                      )}
                    </Fragment>
                  );
                })}
            </PopoverContent>
          </Popover>
        )}
        {useLevel && (
          <Input
            className="w-[80%] !text-lg border-b-2 border-t-0 border-x-0 rounded-none text-center font-bold focus-visible:ring-0 input-removeArrow p-0 mx-0 mt-auto mb-2"
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
