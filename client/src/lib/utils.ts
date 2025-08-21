import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

const inputNumberWithSpace = (val: string, useFloat?: boolean): number | string => {
  let test: RegExp;
  if (useFloat) test = /[^0-9.]/g;
  else test = /[^0-9]/g;
  const cleaned = val.replace(test, "");
  const parts = cleaned.split(".");
  if (parts.length > 2) val = parts[0] + "." + parts[1];
  else val = cleaned;

  return val;
};

export { inputNumberWithSpace };
