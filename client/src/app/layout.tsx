import Store from "@/app/Store";
import api from "@/lib/axios";
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import React from "react";
import "./globals.css";

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
  const weaponList = (await api.get(`/weapons`)).data;
  const artifactSets = (await api.get(`/artifactsets`)).data;

  return (
    <html className="h-full" lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen grid grid-rows-[1fr_auto]`}>
        <Store weaponList={weaponList} artifactSets={artifactSets}>
          <div className="flex flex-col justify-center">{children}</div>
        </Store>
        <footer className="text-gray-600 p-2 mt-5 mx-auto">Created by JjoriButler</footer>
      </body>
    </html>
  );
};

export default RootLayout;
