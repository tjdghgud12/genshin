import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

type AnyObject = Record<string, any>;

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

const deepMergeAddOnly = <T extends AnyObject, S extends AnyObject>(target: T, source: S): T & S => {
  const result: AnyObject = { ...target };

  for (const key in source) {
    const sourceVal = source[key];
    const targetVal = target[key];

    if (targetVal === undefined) {
      result[key] = sourceVal;
    } else if (sourceVal && typeof sourceVal === "object" && targetVal && typeof targetVal === "object") {
      if (Array.isArray(sourceVal) && Array.isArray(targetVal)) {
        const minLength = Math.min(sourceVal.length, targetVal.length);
        result[key] = targetVal.map((item: (typeof targetVal)[number], idx: number) => {
          if (idx < minLength) {
            if (item && typeof item === "object" && sourceVal[idx] && typeof sourceVal[idx] === "object") {
              return deepMergeAddOnly(item as AnyObject, sourceVal[idx]);
            } else return item;
          } else return item;
        });
      } else if (!Array.isArray(sourceVal) && !Array.isArray(targetVal)) {
        result[key] = deepMergeAddOnly(targetVal, sourceVal);
      } else result[key] = targetVal;
    } else {
      result[key] = targetVal;
    }
  }

  return result as T & S;
};

export { deepMergeAddOnly, inputNumberWithSpace };
