import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Steinmetz Antiquitäten – Backend",
  robots: { index: false, follow: false },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="de">
      <body>{children}</body>
    </html>
  );
}
