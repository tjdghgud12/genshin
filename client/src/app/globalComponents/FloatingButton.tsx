"use client";

import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { Plus } from "lucide-react";
import { ReactElement } from "react";

const FloatingButton = ({ open, setOpen }: { open: boolean; setOpen: (state: boolean) => void }): ReactElement => {
  return (
    <motion.div
      className="fixed bottom-6 right-6 flex flex-col items-end gap-3 z-50"
      whileHover={{ scale: 1.1, rotate: 5 }}
      whileTap={{ scale: 0.9, rotate: -5 }}
      transition={{ type: "spring", stiffness: 300 }}
    >
      <Button type="button" onClick={() => setOpen(!open)} className="w-14 h-14 rounded-full text-white shadow-xl flex items-center justify-center">
        <Plus className={`h-6 w-6 transition-transform ${open ? "rotate-45" : ""}`} />
      </Button>
    </motion.div>
  );
};

export default FloatingButton;
