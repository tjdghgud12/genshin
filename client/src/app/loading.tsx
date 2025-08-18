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

const DotBounsLoading = ({ className = "w-full h-full", dotClassName = "w-24 h-24 stroke-8" }: { className?: string; dotClassName?: string }): React.ReactElement => {
  return (
    <div className={`flex ${className}`}>
      <div className="flex items-center">
        <Dot className={`text-violet-600 animate-bounce bounce-with-pause ${dotClassName}`} style={{}} />
        <Dot className={`text-violet-600 animate-bounce bounce-with-pause ${dotClassName}`} style={{ animationDelay: "0.5s" }} />
        <Dot className={`text-violet-600 animate-bounce bounce-with-pause ${dotClassName}`} style={{ animationDelay: "1s" }} />
      </div>
    </div>
  );
};

export default RootLoading;
export { DotBounsLoading };
