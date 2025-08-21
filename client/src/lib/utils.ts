import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

const inputNumberWithSpace = (val: string, useFloat?: boolean, decimalPlaces?: number): number | string => {
  let test: RegExp;
  if (useFloat) test = /[^0-9.]/g;
  else test = /[^0-9]/g;
  let cleaned = val.replace(test, "");
  const parts = cleaned.split(".");
  if (parts.length > 2) val = parts[0] + "." + parts[1];
  else val = cleaned;

  if (decimalPlaces !== undefined && useFloat && cleaned.includes(".")) {
    const [intPart, decPart] = cleaned.split(".");
    cleaned = intPart + "." + decPart.slice(0, decimalPlaces);
  }

  if (cleaned === "") return "";
  return useFloat ? Number(cleaned) : Number.parseInt(cleaned);
};

export { inputNumberWithSpace };
