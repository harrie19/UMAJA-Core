import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'White Room Lab - AI Co-Creation Laboratory',
  description: 'Interactive 3D AI-Human Co-Creation Laboratory powered by UMAJA-Core',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="de">
      <body className="font-sans">{children}</body>
    </html>
  )
}
