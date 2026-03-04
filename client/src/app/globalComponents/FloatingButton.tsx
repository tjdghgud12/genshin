"use client";

import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import { ReactElement } from "react";

const FloatingButton = ({
  open,
  className,
  setOpen,
  children,
}: {
  open: boolean;
  className?: string;
  setOpen: (state: boolean) => void;
  children: React.ReactNode;
}): ReactElement => {
  return (
    <motion.button
      className={cn(
        "fixed bottom-6 right-6 w-14 h-14 rounded-full flex items-center justify-center text-white shadow-xl overflow-hidden z-50 group hover:gap-3 bg-gray-700",
        className,
      )}
      whileHover={{ width: 250 }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
      type="button"
      onClick={() => setOpen(!open)}
    >
      {children}
    </motion.button>
  );
};

export default FloatingButton;
