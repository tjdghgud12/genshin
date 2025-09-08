"useClient";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Card, CardContent } from "@/components/ui/card";
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { IattackDamage, IdamageCalculationResult } from "@/types/calculatorType";
import { useEffect, useState } from "react";
import { calculatorLabel } from "../../../lib/calculator";

const elementColors: Record<string, Record<string, string>> = {
  Fire: { bg: `bg-Fire`, shadow: "shadow-shadow-Fire" },
  Water: { bg: `bg-Water`, shadow: "shadow-shadow-Water" },
  Wind: { bg: `bg-Wind`, shadow: "shadow-shadow-Wind" },
  Electric: { bg: `bg-Electric`, shadow: "shadow-shadow-Electric" },
  Ice: { bg: `bg-Ice`, shadow: "shadow-shadow-Ice" },
  Rock: { bg: `bg-Rock`, shadow: "shadow-shadow-Rock" },
  Grass: { bg: `bg-Grass`, shadow: "shadow-shadow-Grass" },
};

const DamageResultCard = ({
  damageResult,
  element,
}: {
  damageResult: IdamageCalculationResult;
  element: "Fire" | "Water" | "Wind" | "Electric" | "Ice" | "Rock" | "Grass";
}): React.ReactElement => {
  const [open, setOpen] = useState<boolean>(true);
  const [head, setHead] = useState<string[]>([]);
  const [body, setBody] = useState<{ props: object; data: string | number | null }[][]>([]);

  const genAttackTableData = (raw: number | null, additional: number | null): string | null => {
    if (raw == null) return null;
    return additional != null ? `${raw.toFixed(2)} (+${additional.toFixed(2)})` : `${raw.toFixed(2)}`;
  };
  const hasAdditionalKey = (obj: IattackDamage, key: keyof IattackDamage): obj is IattackDamage & Record<`${string}Additional`, number> => {
    return `${key}Additional` in obj;
  };

  useEffect(() => {
    const header = ["반응", "nomal", "charge", "falling", "elementalSkill", "elementalBurst"];
    const bodyData: (string | number | null)[][] = [];

    const excludeList = ["Additional", "Critical", "NonCritical"];
    const attackList = Object.keys(damageResult.nomal).filter((label): label is keyof IattackDamage => !label.includes("Additional"));
    const reactionList = Object.keys(damageResult).filter((label) => label.includes("Damage") && !excludeList.some((exclude) => label.includes(exclude)));

    [damageResult.nomal, damageResult.charge, damageResult.falling, damageResult.elementalSkill, damageResult.elementalBurst].map((values, i) => {
      if (i == 0) attackList.map((type) => bodyData.push([type]));
      attackList.map((key, rowIdx) =>
        bodyData[rowIdx].push(hasAdditionalKey(values, key) ? genAttackTableData(values[key], values[`${key}Additional`]) : values[key] ? values[key].toFixed(2) : null),
      );
    });

    Object.entries(damageResult.custom).map(([name, values]) => {
      header.push(name);
      attackList.map((key, rowIdx) =>
        bodyData[rowIdx].push(hasAdditionalKey(values, key) ? genAttackTableData(values[key], values[`${key}Additional`]) : values[key] ? values[key].toFixed(2) : null),
      );
    });

    // 아래가 최종적으로 담길 영역
    const body = bodyData
      .filter((row) => !row.slice(1).every((col) => col === null))
      .map((row) =>
        row.map((col) => {
          if (col === null) return { props: {}, data: col };
          const label = col?.toString().replace("Damage", "");
          return { props: {}, data: label in calculatorLabel ? calculatorLabel[label as keyof typeof calculatorLabel] : label };
        }),
      );
    setHead(header.map((d) => (d in calculatorLabel ? calculatorLabel[d as keyof typeof calculatorLabel] : d)));
    setBody(body);
    // 나머지 반응들 전부 처리해야함.
    // 아래 항목들인데 ㅈ됐지?
    // 이거 계속 추가될텐데???
    // 자동으로 긁어와서 하도록 해야할꺼같아.
    // 위 아래 전부 다
    // verloadedDamage: number; // 과부하
    // electroChargedDamage: number; // 감전
    // superconductDamage: number; // 초전도
    // shatterDamage: number; // 쇄빙

    // // 개별 치명타 옵션 보유 반응
    // bloomDamage: number; // 개화 기대값
    // bloomDamageCritical: number; // 개화 치명타
    // bloomDamageNonCritical: number; // 개화 논치명타
    // hyperBloomDamage: number; // 만개 기대값
    // hyperBloomDamageCritical: number; // 만개 치명타
    // hyperBloomDamageNonCritical: number; // 만개 논치명타
    // burgeonDamage: number; // 발화 기대값
    // burgeonDamageCritical: number; // 발화 치명타
    // burgeonDamageNonCritical: number; // 발화 논치명타
    // burningDamage: number; // 연소 기대값
    // burningDamageCritical: number; // 연소 치명타
    // burningDamageNonCritical: number; // 연소 논치명타

    // // 달반응
    // lunarChargedDamage: number; // 달감전 기대값
    // lunarChargedDamageCritical: number; // 달감전 치명타
    // lunarChargedDamageNonCritical: number; // 달감전 논치명타

    // // 확산
    // fireSwirlDamage: number; // 불확산
    // waterSwirlDamage: number; // 물확산
    // iceSwirlDamage: number; // 얼음확산
    // elecSwirlDamage: number; // 번개확산
  }, [damageResult]);

  return (
    <Card
      className={`w-full p-0 shadow-lg border-none mb-5 transition-all duration-200 ${elementColors[element].bg} ${elementColors[element].shadow} ${open ? "" : "bg-transparent shadow-none"}`}
    >
      <CardContent className={`w-full rounded-2x`}>
        <Accordion type="single" collapsible onValueChange={(state) => setOpen(state === "calculation-result")} defaultValue="calculation-result">
          <AccordionItem className={`w-full flex flex-col -translate-y-3 relative `} value="calculation-result">
            <AccordionTrigger className="flex-none p-0 m-0 mx-auto bg-gray-700 rounded-full" arrowClassName="size-10 text-white" />
            <AccordionContent className="w-full">
              <Table>
                <TableCaption>
                  ※ 고정 계수를 제외한 <span className="font-bold">변동 계수의 공격은 100%</span> 기준입니다.
                </TableCaption>
                <TableHeader className="font-bold">
                  <TableRow>
                    {head.map((d) => (
                      <TableHead key={`damage-result-table-head-${d}`} className="font-bold text-center">
                        {d}
                      </TableHead>
                    ))}
                  </TableRow>
                </TableHeader>
                <TableBody className="font-bold">
                  {body.map((row, rowIdx) => {
                    return (
                      <TableRow key={`damage-result-table-body-${rowIdx}`}>
                        {row
                          .filter((d) => d !== null)
                          .map((d, colIdx) => (
                            <TableCell key={`damage-result-table-body-${rowIdx}-${colIdx}`} className="text-center">
                              {d.data ? d.data : "-"}
                            </TableCell>
                          ))}
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      </CardContent>
    </Card>
  );
};

export default DamageResultCard;
