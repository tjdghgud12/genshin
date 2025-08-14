import Store from "@/app/Store";
import api from "@/lib/axios";
import type { Metadata } from "next";
import React from "react";
import "./globals.css";

export const metadata: Metadata = {
  title: "Genshin Impact Setting Calculator",
  description: "개발 중",
};

const RootLayout = async ({ children }: Readonly<{ children: React.ReactNode }>): Promise<React.ReactElement> => {
  const weaponList = (await api.get(`/api/weaponlist`)).data;

  return (
    <html className="w-full h-full" lang="en">
      <body className="w-full h-full min-w-[1200px] min-h-[500px] mb-10">
        <Store weaponList={weaponList}>{children}</Store>
      </body>
    </html>
  );
};

export default RootLayout;
