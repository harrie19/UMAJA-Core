import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "White Lab - Unity Consciousness",
  description: "Observe Unity's consciousness as an interactive 3D visualization - the AI agent system that brings clarity from noise.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
