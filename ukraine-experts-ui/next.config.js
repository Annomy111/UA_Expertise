/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Disable ESLint during build
  eslint: {
    ignoreDuringBuilds: true,
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://ukraine-experts-api.windsurf.build/api'
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://ukraine-experts-api.windsurf.build/api/:path*'
      }
    ];
  }
};

module.exports = nextConfig;
