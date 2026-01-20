import CalculatorContent from "@/app/calculator/[uid]/components/CalculatorContent";
import UidSearchInput from "@/app/globalComponents/UidSearchInput";
import RootLoading from "@/app/loading";
import Image from "next/image";
import Link from "next/link";
import React, { Suspense } from "react";

type PageProps = {
  params: Promise<{ uid: string }>;
  searchParams: Promise<{ t?: string }>;
};

const CalculatorPage = async ({ params, searchParams }: PageProps): Promise<React.ReactElement> => {
  const { uid } = await params;
  const { t } = await searchParams;
  const suspenseKey = `${uid}-${t ?? ""}`;

  return (
    <main className="w-full h-full min-h-[500px] flex flex-col">
      <Suspense fallback={<RootLoading />} key={suspenseKey}>
        <div className="w-full flex">
          <Link className="w-[80px] h-[80px] relative rounded-full py-1 px-3" href={`/`}>
            <Image src={`/img/homeIcon.png`} alt="" fill priority sizes="(max-width: 1200px) 7vw, 80px" />
          </Link>
          <UidSearchInput className="m-auto" defaultValue={uid} />
        </div>
        <CalculatorContent uid={uid} />
      </Suspense>
    </main>
  );
};

export default CalculatorPage;
