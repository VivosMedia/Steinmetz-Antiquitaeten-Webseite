/** @type {import('next').NextConfig} */

// Alle Seiten außer der Startseite und der Verwaltung laufen unter einer
// sauberen URL ohne ".html" (z. B. /kommoden statt /kommoden.html).
const CLEAN_PAGES = [
  "kommoden", "lampen", "dekoration", "tische", "sitzmoebel",
  "sekretaere", "schraenke", "angebote", "kontakt", "impressum", "produkt",
];

const nextConfig = {
  turbopack: {
    root: import.meta.dirname,
  },
  async redirects() {
    // Alte .html-URLs dauerhaft (308) auf die sauberen URLs umleiten,
    // damit bereits von Google indexierte/verlinkte Adressen nicht brechen.
    return [
      { source: "/index.html", destination: "/", permanent: true },
      ...CLEAN_PAGES.map((page) => ({
        source: `/${page}.html`,
        destination: `/${page}`,
        permanent: true,
      })),
    ];
  },
  async rewrites() {
    // Next.js liefert Dateien aus public/ nicht automatisch für "/" aus —
    // ohne diese Regeln würden die eigentlichen .html-Dateien nicht unter
    // ihrer sauberen URL erscheinen.
    return [
      { source: "/", destination: "/index.html" },
      ...CLEAN_PAGES.map((page) => ({
        source: `/${page}`,
        destination: `/${page}.html`,
      })),
    ];
  },
};

export default nextConfig;
