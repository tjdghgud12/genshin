import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  turbopack: {},
  // webpack(config, { isServer }) {
  //   // 필요시 다음과 같이 설정하여 PnP 문제를 해결
  //   config.resolve.symlinks = false;
  //   return config;
  // },
};

export default nextConfig;
