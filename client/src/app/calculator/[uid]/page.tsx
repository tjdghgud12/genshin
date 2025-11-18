import CharacterTabs from "@/app/calculator/[uid]/components/CharacterTabs";
import RootLoading from "@/app/loading";
import React, { Suspense } from "react";

const CalculatorPage = async ({ params }: { params: Promise<{ uid: string }> }): Promise<React.ReactElement> => {
  const { uid } = await params;
  return (
    <Suspense fallback={<RootLoading />} key={`${uid}-${Date.now()}`}>
      <CharacterTabs params={params} />
    </Suspense>
  );
};

export default CalculatorPage;
