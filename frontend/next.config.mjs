/** @type {import('next').NextConfig} */

// In development the frontend proxies /api/* to the FastAPI backend so the
// browser makes same-origin requests (no CORS dance). Override the target
// with BACKEND_ORIGIN if the backend runs somewhere other than :8000.
const BACKEND_ORIGIN = process.env.BACKEND_ORIGIN ?? "http://localhost:8000";

const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${BACKEND_ORIGIN}/api/:path*`,
      },
    ];
  },
  // Product images come from OpenFoodFacts / brand CDNs; allow them.
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "**.openfoodfacts.org" },
      { protocol: "https", hostname: "**" },
    ],
  },
};

export default nextConfig;
