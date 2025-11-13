import UidSearchInput from "@/app/globalComponents/UidSearchInput";
import React from "react";

const Home = (): React.ReactElement => {
  return (
    <main className="w-full h-full flex flex-col justify-center">
      <div className="flex flex-col items-center">
        <h1 className="text-8xl font-bold text-violet-800 mx-auto">Calculator</h1>
        <UidSearchInput className="w-1/3 mt-10 text-center" value={""} />
      </div>
    </main>
  );
};

export default Home;
