"use client";

import FloatingButton from "@/app/globalComponents/FloatingButton";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Combobox, ComboboxContent, ComboboxEmpty, ComboboxInput, ComboboxItem, ComboboxList } from "@/components/ui/combobox";
import { Input } from "@/components/ui/input";
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { inputNumberWithSpace } from "@/lib/utils";
import { useFightPropLabelStore } from "@/store/figthtPropLabelStore";
import { CirclePlus, X } from "lucide-react";
import { useRef, useState } from "react";
import { toast } from "sonner";

const AdditionalFightProp = ({
  values,
  onChange,
}: {
  values: { key: string; value: number | string }[];
  onChange: (values: { key: string; value: number | string }[]) => void;
}): React.ReactElement => {
  const fightPropLabels = useFightPropLabelStore((state) => state.fightPropLabels);
  const sheetContentRef = useRef<HTMLDivElement>(null);
  const [open, setOpen] = useState<boolean>(false);
  const [selectedFightProp, setSelectedFightProp] = useState<string | undefined>(undefined);
  const [statValue, setStatValue] = useState<number | string | undefined>(undefined);

  const labels = Object.entries(fightPropLabels).map(([fightProp, label]) => ({ label, value: fightProp }));

  const handleStatValueChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const value = inputNumberWithSpace(event.target.value, selectedFightProp?.includes("%"), 2);
    setStatValue(value);
  };

  const handleSelectedFightPropChange = (fightProp: { label: string; value: string } | null): void => {
    setSelectedFightProp(fightProp?.value);
  };

  const handleAddFightProp = (): void => {
    if (!selectedFightProp) {
      toast.error("옵션을 선택해주세요.");
      return;
    }
    if (!statValue) {
      toast.error("값을 입력해주세요.");
      return;
    }
    const newValues = [...values, { key: selectedFightProp, value: statValue }].sort((a, b) => a.key.localeCompare(b.key));
    onChange(newValues);
  };

  const handleRemoveFightProp = (key: string, value: number | string): void => {
    const index = values.findIndex((v) => v.key === key && v.value === value);
    if (index === -1) return;
    const newValues = [...values.slice(0, index), ...values.slice(index + 1)];
    onChange(newValues);
  };

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <FloatingButton className="bg-violet-700" open={open} setOpen={setOpen}>
          <CirclePlus className={`size-8 text-white shrink-0 transition-transform ${open ? "rotate-45" : ""}`} />
          <span className="text-lg whitespace-nowrap overflow-hidden max-w-0 opacity-0 group-hover:max-w-[200px] group-hover:opacity-100 transition-all duration-300">
            추가 옵션 설정
          </span>
        </FloatingButton>
      </SheetTrigger>
      <SheetContent ref={sheetContentRef} className="overflow-auto px-2">
        <SheetDescription />
        <SheetHeader>
          <SheetTitle>추가 옵션 설정</SheetTitle>
        </SheetHeader>
        <Combobox items={labels} itemToStringValue={(label: { label: string; value: string }) => label.label} onValueChange={handleSelectedFightPropChange}>
          <ComboboxInput className="w-full" placeholder="추가 옵션 선택" />
          <ComboboxContent container={sheetContentRef}>
            <ComboboxEmpty>검색 결과가 없습니다.</ComboboxEmpty>
            <ComboboxList>
              {(item: { label: string; value: string }) => (
                <ComboboxItem key={item.value} value={item}>
                  {item.label}
                </ComboboxItem>
              )}
            </ComboboxList>
          </ComboboxContent>
        </Combobox>
        <div className="flex gap-2">
          <Input placeholder="수치를 입력해주세요." onChange={handleStatValueChange} />
          <Button type="button" className="font-bold hover:scale-105 transition-all duration-100 active:scale-95" onClick={handleAddFightProp}>
            추가
          </Button>
        </div>
        <div className="min-h-32 flex flex-wrap content-start gap-2 border-gray-200 border p-2 rounded-md shadow-sm">
          {values.map((value, i) => (
            <Badge key={`${value.key}.${value.value}.${i}`} className="w-fit h-fit flex gap-2">
              <p className="font-bold">
                {fightPropLabels[value.key]} - {value.value}
              </p>
              <Button
                type="button"
                className="w-fit h-fit p-0! transition-all duration-100 active:scale-90"
                variant="ghost"
                onClick={() => handleRemoveFightProp(value.key, value.value)}
              >
                <X className="w-4 h-4" />
              </Button>
            </Badge>
          ))}
        </div>
      </SheetContent>
    </Sheet>
  );
};

export default AdditionalFightProp;
