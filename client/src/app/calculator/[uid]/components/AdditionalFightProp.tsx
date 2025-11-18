"use client";

import FloatingButton from "@/app/globalComponents/FloatingButton";
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { calculatorFormSchema as formSchema } from "@/lib/calculator";
import { fightPropLabels } from "@/lib/fightProps";
import { useState } from "react";
import { UseFormReturn } from "react-hook-form";
import { z } from "zod";

const AdditionalFightProp = ({ form }: { form: UseFormReturn<z.infer<typeof formSchema>> }): React.ReactElement => {
  const [open, setOpen] = useState<boolean>(false);

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <FloatingButton open={open} setOpen={setOpen} />
      </SheetTrigger>
      <SheetContent className="overflow-auto px-2">
        <SheetHeader>
          <SheetTitle>추가 옵션 설정</SheetTitle>
        </SheetHeader>
        <SheetDescription>추가할 스텟을 입력해주세요.</SheetDescription>
        {Object.entries(fightPropLabels).map(([fightProp, label]) => {
          return (
            <FormField
              key={`additional-fightProp-${fightProp}`}
              control={form.control}
              name={`additionalFightProp.${fightProp}`}
              render={({ field }) => (
                <FormItem className="grid grid-cols-[2fr_1fr] gap-3">
                  <FormLabel className="break-normal font-bold">{label}</FormLabel>
                  <FormControl>
                    <Input
                      className="w-2/5 h-fit border-b-2 border-t-0 border-x-0 rounded-none !text-lg text-center font-bold shadow-none focus-visible:ring-0 input-removeArrow my-auto p-0"
                      placeholder={label}
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          );
        })}
      </SheetContent>
    </Sheet>
  );
};

export default AdditionalFightProp;
