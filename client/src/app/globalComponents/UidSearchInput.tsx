"use client";

import { Button } from "@/components/ui/button";
import { Form, FormControl, FormField, FormItem, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { zodResolver } from "@hookform/resolvers/zod";
import { Search } from "lucide-react";
import { useRouter, useSearchParams } from "next/navigation";
import { useForm } from "react-hook-form";
import { z } from "zod";

const uidFormSchema = z.object({
  uid: z.string().min(9, { error: "UID를 확인해주세요." }).max(12, {
    error: "UID를 확인해주세요.",
  }),
});

const UidSearchInput = ({ value, className = "" }: { value: string | null; className?: string }): React.ReactElement => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const uid = value ?? searchParams.get("uid")?.toString();

  const form = useForm<z.infer<typeof uidFormSchema>>({
    resolver: zodResolver(uidFormSchema),
    defaultValues: {
      uid: uid || "",
    },
  });

  const onSubmit = (valus: z.infer<typeof uidFormSchema>): void => {
    router.push(`/calculator?${new URLSearchParams({ uid: valus.uid }).toString()}`);
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className={`w-1/2 h-fit min-w-[500px] flex overflow-hidden rounded-full border-2 p-1 mx-auto ${className}`}>
        <FormField
          control={form.control}
          name="uid"
          render={({ field }) => (
            <FormItem className="w-full">
              <FormControl>
                <Input
                  className={`w-full border-none shadow-none focus-visible:ring-0 ${className.includes("text-center") ? "text-center" : ""}`}
                  {...field}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                    const uid = e.target.value;
                    if (/^\d*$/.test(uid)) field.onChange(uid);
                  }}
                  maxLength={12}
                  placeholder="UID"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-auto bg-transparent rounded-full text-stone-500  hover:bg-stone-300 hover:text-white">
          <Search />
        </Button>
      </form>
    </Form>
  );
};

export default UidSearchInput;
