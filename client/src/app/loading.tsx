import { Dot } from "lucide-react";
import React from "react";

const RootLoading = (): React.ReactElement => {
  return (
    <div className="w-screen h-screen flex">
      <div className="flex items-center m-auto">
        <Dot className="w-26 h-26 text-violet-600 animate-bounce stroke-7 bounce-with-pause" style={{}} />
        <Dot className="w-26 h-26 text-violet-600 animate-bounce stroke-7 bounce-with-pause" style={{ animationDelay: "0.5s" }} />
        <Dot className="w-26 h-26 text-violet-600 animate-bounce stroke-7 bounce-with-pause" style={{ animationDelay: "1s" }} />
      </div>
    </div>
  );
};

const DotBounsLoading = (): React.ReactElement => {
  return (
    <div className="w-full h-full flex">
      <div className="flex items-center">
        <Dot className="w-28 h-28 text-violet-600 animate-bounce stroke-8 bounce-with-pause" style={{}} />
        <Dot className="w-28 h-28 text-violet-600 animate-bounce stroke-8 bounce-with-pause" style={{ animationDelay: "0.5s" }} />
        <Dot className="w-28 h-28 text-violet-600 animate-bounce stroke-8 bounce-with-pause" style={{ animationDelay: "1s" }} />
      </div>
    </div>
  );
};

export default RootLoading;
export { DotBounsLoading };
