const allowedDomains = process.env.NEXT_PUBLIC_IMAGE_DOMAINS
    ? process.env.NEXT_PUBLIC_IMAGE_DOMAINS.split(',')
    : []

/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: allowedDomains,
  },
};

export default nextConfig;
