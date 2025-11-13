import api from "@/lib/axios";
import { IArtifactSetsInfo } from "@/types/artifactType";
import { IWeaponInfo } from "@/types/weaponType";
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import React from "react";
import { Toaster } from "sonner";
import "./globals.css";
import Store from "./Store";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Genshin Impact Setting Calculator",
  description: "개발 중",
};

const RootLayout = async ({ children }: Readonly<{ children: React.ReactNode }>): Promise<React.ReactElement> => {
  const weaponList = Object.fromEntries((await api.get(`/weapons`)).data.map((weapon: IWeaponInfo) => [weapon.id, weapon]));
  const artifactSets = Object.fromEntries((await api.get(`/artifactsets`)).data.map((set: IArtifactSetsInfo) => [set.name, set]));

  return (
    <html className="h-full" lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen grid grid-rows-[1fr_auto]`}>
        <Store weaponList={weaponList} artifactSets={artifactSets} />
        <div>
          <Toaster richColors />
          {children}
        </div>
        <footer className="text-gray-600 p-2 mt-5 mx-auto">Created by JjoriButler</footer>
      </body>
    </html>
  );
};

export default RootLayout;
