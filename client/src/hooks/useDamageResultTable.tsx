"use client";

import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { calculatorLabel } from "@/lib/calculator";
import { typedKeys } from "@/lib/utils";
import { IattackDamage, IdamageCalculationResult } from "@/types/calculatorType";
import { useMemo } from "react";

type Tattack = "nomal" | "charge" | "falling" | "elementalSkill" | "elementalBurst";

const useDamageResultTable = (
  damageResult: IdamageCalculationResult | null,
): { head: string[]; body: { props: object; data: string | number | null | React.ReactElement }[][] } => {
  const genAttackTableData = (raw: number | null, additional: number | null = null): string | null => {
    if (raw == null) return null;
    return additional != null ? `${raw.toFixed(2)} (+${additional.toFixed(2)})` : `${raw.toFixed(2)}`;
  };

  const hasKey = <K extends keyof IattackDamage | keyof IdamageCalculationResult, Suffix extends string>(
    obj: IattackDamage | IdamageCalculationResult,
    key: K,
    suffix: Suffix,
  ): obj is (IattackDamage | IdamageCalculationResult) & Record<`${K}${Suffix}`, number> => {
    return `${String(key)}${suffix}` in obj;
  };

  const { head, body } = useMemo(() => {
    if (!damageResult) {
      return { head: [] as string[], body: [] as { props: object; data: string | number | null | React.ReactElement }[][] };
    }

    const header = ["반응", "nomal", "charge", "falling", "elementalSkill", "elementalBurst"];
    const bodyData: (string | number | null | React.ReactElement)[][] = [];
    const excludeList = ["Additional", "Critical", "NonCritical"];
    const damageList = typedKeys(damageResult.nomal).filter((label) => !label.includes("Additional"));
    const reactionList = typedKeys(damageResult).filter((label) => label.includes("Damage") && !excludeList.some((exclude) => label.includes(exclude)));

    damageList.map((type) => bodyData.push([type]));
    reactionList.map((type) => bodyData.push([type]));

    (header.slice(1) as Tattack[]).map((attack) => {
      const nonCritical = damageResult[`${attack}NonCritical`];
      const critical = damageResult[`${attack}Critical`];
      const expected = damageResult[attack];

      damageList.map((key, rowIdx) => {
        const nonCriticalValue = genAttackTableData(nonCritical[key], hasKey(nonCritical, key, "Additional") ? nonCritical[`${key}Additional`] : null);
        const criticalValue = genAttackTableData(critical[key], hasKey(critical, key, "Additional") ? critical[`${key}Additional`] : null);
        const expectedValue = genAttackTableData(expected[key], hasKey(expected, key, "Additional") ? expected[`${key}Additional`] : null);
        bodyData[rowIdx].push(
          criticalValue ? (
            <Tooltip delayDuration={500}>
              <TooltipTrigger type="button">{expectedValue}</TooltipTrigger>
              <TooltipContent className="max-w-[200px] bg-gray-500 fill-gray-500" side="right">
                <p>치명: {criticalValue}</p>
                <p>비치명: {nonCriticalValue}</p>
              </TooltipContent>
            </Tooltip>
          ) : (
            expectedValue
          ),
        );
      });
    });

    Object.entries(damageResult.custom).map(([name, values]) => {
      header.push(name);
      const nonCritical = damageResult.customNonCritical[name];
      const critical = damageResult.customCritical[name];
      damageList.map((key, rowIdx) => {
        const nonCriticalValue = genAttackTableData(nonCritical[key], hasKey(nonCritical, key, "Additional") ? nonCritical[`${key}Additional`] : null);
        const criticalValue = genAttackTableData(critical[key], hasKey(critical, key, "Additional") ? critical[`${key}Additional`] : null);
        const expectedValue = genAttackTableData(values[key], hasKey(values, key, "Additional") ? values[`${key}Additional`] : null);

        bodyData[rowIdx].push(
          criticalValue ? (
            <Tooltip delayDuration={500}>
              <TooltipTrigger type="button">{expectedValue}</TooltipTrigger>
              <TooltipContent className="max-w-[200px] bg-gray-500 fill-gray-500" side="right">
                <p>치명: {criticalValue}</p>
                <p>비치명: {nonCriticalValue}</p>
              </TooltipContent>
            </Tooltip>
          ) : (
            expectedValue
          ),
        );
      });
    });

    reactionList.map((key) => {
      const rowIdx = bodyData.findIndex((row) => row[0] === key);
      if (rowIdx !== -1) {
        const nonCriticalValue = hasKey(damageResult, key, "NonCritical") ? damageResult[`${key}NonCritical`] : null;
        const criticalValue = hasKey(damageResult, key, "Critical") ? damageResult[`${key}Critical`] : null;
        const expectedValue = typeof damageResult[key] === "number" ? damageResult[key].toFixed(2) : null;

        bodyData[rowIdx].push(
          criticalValue ? (
            <Tooltip delayDuration={500}>
              <TooltipTrigger type="button">{expectedValue}</TooltipTrigger>
              <TooltipContent className="max-w-[200px] bg-gray-500 fill-gray-500" side="right">
                <p>치명: {criticalValue}</p>
                <p>비치명: {nonCriticalValue}</p>
              </TooltipContent>
            </Tooltip>
          ) : (
            expectedValue
          ),
        );
      }
    });

    // table용 데이터 구조로 변경
    const body = bodyData
      .filter((row) => !row.slice(1).every((col) => col === null))
      .map((row) =>
        row.map((col, colIdx) => {
          if (col === null) return { props: {}, data: col };
          const label = col?.toString().replace("Damage", "");
          return {
            props: reactionList.includes(row[0] as keyof IdamageCalculationResult) && colIdx ? { colSpan: header.length - 1 } : {},
            data: colIdx ? col : label in calculatorLabel ? calculatorLabel[label as keyof typeof calculatorLabel] : label,
          };
        }),
      );
    const head = header.map((d) => (d in calculatorLabel ? calculatorLabel[d as keyof typeof calculatorLabel] : d));

    return { head, body };
  }, [damageResult]);

  return { head, body };
};

export { useDamageResultTable };
