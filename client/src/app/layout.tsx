import type { Metadata } from "next";
import React from "react";
import "./globals.css";

export const metadata: Metadata = {
  title: "Genshin Impact Setting Calculator",
  description: "개발 중",
};

const RootLayout = ({ children }: Readonly<{ children: React.ReactNode }>): React.ReactElement => {
  return (
    <html lang="en">
      <body className="w-full h-full min-w-[1200px] min-h-[500px]">{children}</body>
    </html>
  );
};

export default RootLayout;
