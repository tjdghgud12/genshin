"use client";

import { useCalculatorStore } from "@/store/useCalculatorStore";
import { Fragment, ReactElement, ReactNode, useEffect } from "react";

interface StoreProps {
  children: ReactNode;
  [key: string]: any;
}

const Store = ({ children, ...props }: StoreProps): ReactElement => {
  const setWeaponList = useCalculatorStore((state) => state.setWeaponList);

  useEffect(() => {
    if ((props as any).weaponList) setWeaponList((props as any).weaponList);
  }, [props, setWeaponList]);

  return <Fragment>{children}</Fragment>;
};

export default Store;
