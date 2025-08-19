"use client";
import { Form, FormControl, FormField, FormItem } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import api from "@/lib/axios";
import { useCalculatorStore } from "@/store/useCalculatorStore";
import { zodResolver } from "@hookform/resolvers/zod";
import { Home, Search } from "lucide-react";
// import Image from "next/image";
import { DotBounsLoading } from "@/app/loading";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import React, { Fragment, useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

// **************************** Schema ****************************
const uidFormSchema = z.object({
  uid: z.string().min(9, { error: "UID를 확인해주세요." }).max(12, {
    error: "UID를 확인해주세요.",
  }),
});
// **************************** Schema ****************************

const CalculratorLayout = ({ children }: Readonly<{ children: React.ReactNode }>): React.ReactElement => {
  const router = useRouter();
  const setCalculatorData = useCalculatorStore((state) => state.setTotalCalculatorData);
  const [waitUserInfoFlag, setWaitUserInfoFlag] = useState<boolean>(false);
  const searchParams = useSearchParams();

  const form = useForm<z.infer<typeof uidFormSchema>>({
    resolver: zodResolver(uidFormSchema),
    defaultValues: {
      uid: searchParams.get("uid")?.toString(),
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
      loading: "로딩 중",
      success: (res) => {
        setCalculatorData(res.data.characters);
        window.sessionStorage.setItem("calculatorData", JSON.stringify(res.data.characters));
        const searchParams = new URLSearchParams({ uid: valus.uid });
        router.push(`/calculator?${searchParams.toString()}`);
        setWaitUserInfoFlag(false);
        return "캐릭터 진열장의 정보를 읽어왔습니다.";
      },
      error: (err) => {
        console.log(err);
        setWaitUserInfoFlag(false);
        return "실패요";
      },
    });
  };

  return (
    <main className="w-full h-full flex flex-col">
      {waitUserInfoFlag ? (
        <div className="m-auto">
          <DotBounsLoading />
        </div>
      ) : (
        <Fragment>
          <div className="w-full flex">
            {/* Header */}
            <Link className="w-fit h-fit rounded-full" href={`/`}>
              {/* <Image src={`/img/paimon-face.png`} alt="" priority width={60} height={60} /> */}
              <Home className="text-indigo-800" width={60} height={60} />
            </Link>
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="w-1/2 h-fit min-w-[500px] flex overflow-hidden rounded-full border-2 p-1 m-auto">
                <FormField
                  control={form.control}
                  name="uid"
                  render={({ field }) => (
                    <FormItem className="w-full">
                      <FormControl>
                        <Input className="w-full border-none shadow-none focus-visible:ring-0" {...field} onChange={handleUid} maxLength={12} placeholder="UID" />
                      </FormControl>
                    </FormItem>
                  )}
                />
                <Button type="submit" className="w-auto bg-transparent rounded-full text-stone-500  hover:bg-stone-300 hover:text-white">
                  <Search />
                </Button>
              </form>
            </Form>
          </div>
          <main>{children}</main>
        </Fragment>
      )}
    </main>
  );
};

export default CalculratorLayout;
