"use client";
import { useCalculatorStore } from "@/store/useCalculatorStore";
import { useSearchParams } from "next/navigation";

const CalculratorPage = (): React.ReactElement => {
  const { calculatorData, setCalculateData, setCharacterInfo } = useCalculatorStore();
  const searchParams = useSearchParams();
  searchParams.get("uid");
  return (
    <div>
      <div>{searchParams.get("uid")}</div>
      {JSON.stringify(calculatorData)}
    </div>
  );
};

export default CalculratorPage;
