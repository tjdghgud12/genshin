import { Star } from "lucide-react";
import * as React from "react";

type Props = {
  size?: number | string;
  from?: string;
  middle?: string | null;
  to?: string;
  angle?: number;
  outlined?: boolean;
  className?: string;
};

const GradientStar = ({ size = 24, from = "#FDE047", to = "#BFF8FB", middle = null, angle = 30, outlined = true, className }: Props): React.ReactElement => {
  const id = React.useId();
  const gradId = `star-gradient-${id}`;

  // 각도 회전 (중심 기준)
  const gradientTransform = `rotate(${angle})`;

  return (
    // defs를 담을 래퍼 svg
    <svg width={size} height={size} viewBox="0 0 24 24" className={className} aria-hidden>
      <defs>
        <linearGradient id={gradId} x1="0" y1="0" x2="1" y2="1" gradientTransform={gradientTransform}>
          <stop offset="0%" stopColor={from} />
          {middle ? <stop offset="60%" stopColor={middle} /> : <></>}
          <stop offset="100%" stopColor={to} />
        </linearGradient>
      </defs>

      <Star width={size} height={size} fill={`url(#${gradId})`} stroke={outlined ? "currentColor" : "none"} strokeWidth={outlined ? 1 : 0} />
    </svg>
  );
};

export default GradientStar;
