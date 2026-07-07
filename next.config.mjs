/** @type {import('next').NextConfig} */
const nextConfig = {
  turbopack: {
    root: import.meta.dirname,
  },
  async rewrites() {
    // Next.js liefert Dateien aus public/ nicht automatisch für "/" aus —
    // ohne diese Regel würde die eigentliche Startseite (public/index.html)
    // nicht unter der Domain-Wurzel erscheinen.
    return [{ source: "/", destination: "/index.html" }];
  },
};

export default nextConfig;
