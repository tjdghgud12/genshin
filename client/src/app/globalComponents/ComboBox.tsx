"use client";

import { Button } from "@/components/ui/button";
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { cn } from "@/lib/utils";
import { Check, ChevronsUpDown } from "lucide-react";
import { useState } from "react";

interface option {
  label: string;
  data: any;
  group?: string;
  [key: string]: any;
}

const Combobox = ({
  options = [],
  defaultValue = undefined,
  placeholder = "",
  groups = [],
  className = "",
  optionClassName = "",
  onChange = (_value): void => {},
}: {
  options: option[];
  defaultValue?: string | undefined;
  placeholder: string;
  groups?: string[];
  className?: string;
  optionClassName?: string;
  onChange?: (value?: string) => void;
}): React.ReactElement => {
  const [open, setOpen] = useState(false);
  const [value, setValue] = useState(defaultValue);

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button role="combobox" aria-expanded={open} className={`w-full text-center justify-between p-1 ${className}`}>
          {value ? options.find((option) => option.data.toString() === value)?.label : `${placeholder}`}
          <ChevronsUpDown className="opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent sideOffset={0} className={`w-full p-0 border-t-0`}>
        <Command id="Command" className={`p-0 ${className}`}>
          <CommandInput placeholder="Search Weapon..." className="w-fit h-fit" />
          <CommandList id="CommandList">
            <CommandEmpty>No Weapon found.</CommandEmpty>
            <CommandGroup className={`${optionClassName}`}>
              {options.map((option) => (
                <CommandItem
                  className={value === option.data.toString() ? `bg-accent text-accent-foreground` : ``}
                  key={option.data}
                  value={option.data.toString()}
                  onSelect={(currentValue) => {
                    onChange(currentValue);
                    setValue(currentValue === value ? "" : currentValue);
                    setOpen(false);
                  }}
                >
                  {option.label}
                  <Check className={cn("ml-auto", value === option.data.toString() ? "opacity-100" : "opacity-0")} />
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
};

export { Combobox };
