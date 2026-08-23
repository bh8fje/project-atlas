import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Project Atlas — Local Dashboard',
  description: 'A local-first view of your software project knowledge map.',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
