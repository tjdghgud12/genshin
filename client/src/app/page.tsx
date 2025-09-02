"use client";

import { DotBounsLoading } from "@/app/loading";
import { Button } from "@/components/ui/button";
import { Form, FormControl, FormDescription, FormField, FormItem, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import api from "@/lib/axios";
import { useCalculatorStore } from "@/store/useCalculatorStore";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import React, { Fragment, useState } from "react";
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
  const [waitUserInfoFlag, setWaitUserInfoFlag] = useState<boolean>(false);

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
    setWaitUserInfoFlag(true);
    toast.promise(api.get(`/user/${valus.uid}`), {
      success: (res) => {
        setCalculatorData(res.data.characters);
        window.sessionStorage.setItem("calculatorData", JSON.stringify(res.data.characters));
        const searchParams = new URLSearchParams({ uid: valus.uid });
        router.push(`/calculator?${searchParams.toString()}`);
        setWaitUserInfoFlag(false);
        return "캐릭터 진열장의 정보를 읽어왔습니다.";
      },
      error: (err) => {
        setWaitUserInfoFlag(false);
        console.log(err);
        return "캐릭터 진열장의 정보를 읽어오는데 실패했습니다.";
      },
    });
  };

  return (
    <main className="w-full h-full flex flex-col">
      <Toaster richColors />
      {waitUserInfoFlag ? (
        <div className="m-auto">
          <DotBounsLoading />
        </div>
      ) : (
        <Fragment>
          <div className="h-1/2 flex">
            <h1 className="text-8xl font-bold text-violet-800 mt-auto mb-4 mx-auto">Calculator</h1>
          </div>
          <div />
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="w-full flex mx-auto">
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
              <Button type="submit" className="mr-auto" disabled={waitUserInfoFlag}>
                Submit
              </Button>
            </form>
          </Form>
        </Fragment>
      )}
    </main>
  );
};

export default Home;
