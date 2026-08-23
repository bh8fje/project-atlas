import type { MetadataRoute } from 'next';

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'Project Atlas',
    short_name: 'Atlas',
    description: 'Your local-first software project knowledge map.',
    start_url: '/',
    display: 'standalone',
    background_color: '#f5f3ed',
    theme_color: '#17211c',
    icons: [
      { src: '/atlas-icon.svg', sizes: 'any', type: 'image/svg+xml', purpose: 'any' },
    ],
  };
}
