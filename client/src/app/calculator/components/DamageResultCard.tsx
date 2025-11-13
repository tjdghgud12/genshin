"use client";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Card, CardContent } from "@/components/ui/card";
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { useDamageResultTable } from "@/hooks/useDamageResultTable";
import { IdamageCalculationResult } from "@/types/calculatorType";
import { Loader2 } from "lucide-react";
import { useState } from "react";

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
  damageResult: IdamageCalculationResult | null;
  element: "Fire" | "Water" | "Wind" | "Electric" | "Ice" | "Rock" | "Grass";
}): React.ReactElement => {
  const [open, setOpen] = useState<boolean>(true);
  const { head, body } = useDamageResultTable(damageResult);

  return (
    <Card
      className={`w-full p-0 shadow-lg border-none mb-5 transition-all duration-200 ${elementColors[element].bg} ${elementColors[element].shadow} ${open ? "" : "bg-transparent shadow-none"}`}
    >
      <CardContent className={`w-full rounded-2x`}>
        <Accordion type="single" collapsible onValueChange={(state) => setOpen(state === "calculation-result")} defaultValue="calculation-result">
          <AccordionItem className={`w-full flex flex-col -translate-y-3 relative `} value="calculation-result">
            <AccordionTrigger className="flex-none p-0 m-0 mx-auto bg-gray-700 rounded-full" arrowClassName="size-10 text-white" />
            <AccordionContent className="w-full">
              {damageResult ? (
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
                              <TableCell key={`damage-result-table-body-${rowIdx}-${colIdx}`} className="text-center" {...d.props}>
                                {d.data ? d.data : "-"}
                              </TableCell>
                            ))}
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              ) : (
                <Loader2 className="size-10 animate-spin text-muted-foreground mt-5 m-auto" />
              )}
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      </CardContent>
    </Card>
  );
};

export default DamageResultCard;
