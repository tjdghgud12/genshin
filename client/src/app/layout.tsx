import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import React from "react";
import { Toaster } from "sonner";
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
  return (
    <html className="h-full" lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen grid grid-rows-[1fr_auto]`}>
        <div>
          <Toaster richColors position="bottom-left" />
          {children}
        </div>
        <footer className="text-gray-600 p-2 mt-5 mx-auto">Created by JjoriButler</footer>
      </body>
    </html>
  );
};

export default RootLayout;
