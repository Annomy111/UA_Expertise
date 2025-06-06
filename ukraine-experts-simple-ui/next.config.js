/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
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
