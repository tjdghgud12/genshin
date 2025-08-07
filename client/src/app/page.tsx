"use client";

import { Button } from "@/components/ui/button";
import { Form, FormControl, FormDescription, FormField, FormItem, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import api from "@/lib/axios";
import { useCalculatorStore } from "@/store/useCalculatorStore";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import React from "react";
import { useForm } from "react-hook-form";
import { toast, Toaster } from "sonner";
import { z } from "zod";

// **************************** Schema ****************************
const uidFormSchema = z.object({
  uid: z.string().min(9, { error: "UID를 확인해주세요." }).max(12, {
    error: "UID를 확인해주세요.",
  }),
});
// **************************** Schema ****************************

const Home = (): React.ReactElement => {
  const router = useRouter();
  const setCalculatorData = useCalculatorStore((state) => state.setTotalCalculatorData);

  const form = useForm<z.infer<typeof uidFormSchema>>({
    resolver: zodResolver(uidFormSchema),
    defaultValues: {
      uid: "",
    },
  });

  const handleUid = (e: React.ChangeEvent<HTMLInputElement>): void => {
    const uid = e.target.value;
    if (/^\d*$/.test(uid)) {
      form.setValue("uid", uid);
    }
  };

  const onSubmit = (valus: z.infer<typeof uidFormSchema>): void => {
    toast.promise(api.get(`/api/user/${valus.uid}`), {
      loading: "로딩 중",
      success: (res) => {
        setCalculatorData(res.data.characters);
        const searchParams = new URLSearchParams({ uid: valus.uid });
        router.push(`/calculator?${searchParams.toString()}`);
        return "성공요";
      },
      error: (err) => {
        console.log(err);
        return "실패요";
      },
    });
  };

  return (
    <div>
      <main className="w-screen h-screen">
        <div className="w-screen h-full flex flex-col">
          <Toaster richColors />
          {/* 해당 위치에 뭔가 꾸밀만한 것을더 넣업자 */}
          <div />
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="w-full min-w-[1100px] flex mx-auto">
              <FormField
                control={form.control}
                name="uid"
                render={({ field }) => (
                  <FormItem id="qawdasd" className="w-1/7 h-fit mr-1 ml-auto">
                    <FormControl>
                      <Input placeholder="UID" className=" p-0 text-center" {...field} onChange={handleUid} maxLength={12} />
                    </FormControl>
                    <FormDescription />
                    <FormMessage />
                  </FormItem>
                )}
              />
              <Button type="submit" className="mr-auto">
                Submit
              </Button>
            </form>
          </Form>
        </div>
      </main>
    </div>
  );
};

export default Home;
