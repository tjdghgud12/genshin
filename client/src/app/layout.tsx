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
  const weaponList = (await api.get(`/weapons`)).data;
  const artifactSets = (await api.get(`/artifactsets`)).data;

  return (
    <html className="w-full h-full" lang="en">
      <body className="w-full h-full min-w-[1650px] min-h-[500px] mb-10 flex flex-col">
        <Store weaponList={weaponList} artifactSets={artifactSets}>
          {children}
        </Store>
        <footer className="text-gray-600 p-2 mt-5 mx-auto">Created by JjoriButler</footer>
      </body>
    </html>
  );
};

export default RootLayout;
