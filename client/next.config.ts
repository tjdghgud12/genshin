import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  turbopack: {},
  // webpack(config, { isServer }) {
  //   // 필요시 다음과 같이 설정하여 PnP 문제를 해결
  //   config.resolve.symlinks = false;
  //   return config;
  // },
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "enka.network",
        port: "",
        pathname: "/**",
      },
      {
        protocol: "https",
        hostname: "gi.yatta.moe",
        port: "",
        pathname: "/**",
      },
    ],
  },
};

export default nextConfig;
