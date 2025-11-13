import UidSearchInput from "@/app/globalComponents/UidSearchInput";
import Image from "next/image";
import Link from "next/link";
import React from "react";

const CalculratorLayout = async ({ children }: Readonly<{ children: React.ReactNode }>): Promise<React.ReactElement> => {
  return (
    <main className="w-full h-full min-h-[500px] flex flex-col">
      <div className="w-full flex">
        {/* Header */}
        <Link className="w-[80px] h-[80px] relative rounded-full py-1 px-3" href={`/`}>
          <Image src={`/img/homeIcon.png`} alt="" fill priority sizes="(max-width: 1200px) 7vw" />
        </Link>
        <UidSearchInput className="m-auto" value={null} />
      </div>
      <div className="w-full">{children}</div>
    </main>
  );
};

export default CalculratorLayout;
