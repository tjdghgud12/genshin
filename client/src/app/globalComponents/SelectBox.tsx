"use client";
import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Fragment } from "react";

interface option {
  label: string;
  data: any;
  group?: string;
  [key: string]: any;
}

const SingleSelectBox = ({
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
  return (
    <Select onValueChange={onChange} defaultValue={defaultValue}>
      <SelectTrigger className={`w-full overflow-hidden ${className}`}>
        <SelectValue placeholder={placeholder} />
      </SelectTrigger>
      <SelectContent className={`${optionClassName}`} position="popper">
        {groups.length ? (
          groups.map((group) => {
            return (
              <SelectGroup key={group}>
                <SelectLabel>{group}</SelectLabel>
                {options
                  .filter((o) => o.group === group)
                  .map((o, i) => {
                    return (
                      <SelectItem key={`select-box-option-${group}-${o.data}-${i}`} value={o.data.toString()}>
                        {o.label}
                      </SelectItem>
                    );
                  })}
              </SelectGroup>
            );
          })
        ) : (
          <Fragment>
            {options.map((o, i) => {
              return (
                <SelectItem key={`select-box-option-${o.data}-${i}`} value={o.data.toString()}>
                  {o.label}
                </SelectItem>
              );
            })}
          </Fragment>
        )}
      </SelectContent>
    </Select>
  );
};

export { SingleSelectBox };
