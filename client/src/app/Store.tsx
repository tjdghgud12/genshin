"use client";

import { useCalculatorStore } from "@/store/useCalculatorStore";
import { ReactElement, ReactNode, useEffect } from "react";

interface StoreProps {
  children: ReactNode;
  [key: string]: any;
}

const Store = ({ children, ...props }: StoreProps): ReactElement => {
  const setWeaponList = useCalculatorStore((state) => state.setWeaponList);

  useEffect(() => {
    if ((props as any).weaponList) setWeaponList((props as any).weaponList);
  }, [props, setWeaponList]);

  return <div className="w-full h-full">{children}</div>;
};

export default Store;
