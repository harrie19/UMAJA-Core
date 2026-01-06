import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactStrictMode: true,
  
  // Optimize for Vercel deployment
  typescript: {
    ignoreBuildErrors: false,
  },
};

export default nextConfig;
