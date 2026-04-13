import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  plugins: [react(), tailwindcss()],
  build: {
    outDir: path.resolve(__dirname, 'public/assets'),
    emptyOutDir: false,
    manifest: true,
    rollupOptions: {
      input: {
        'golby-widget': path.resolve(__dirname, 'src/golby-widget.tsx'),
        'assistant-welcome': path.resolve(__dirname, 'src/assistant-welcome.tsx'),
      },
      output: {
        entryFileNames: '[name].js',
        chunkFileNames: 'golby-chunk-[name]-[hash].js',
        assetFileNames: (assetInfo) => {
          if (assetInfo.name && assetInfo.name.endsWith('.css')) {
            return 'golby-widget.css';
          }
          return 'golby-asset-[name]-[hash][extname]';
        },
      },
    },
  },
});
