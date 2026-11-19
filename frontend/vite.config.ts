import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { compression } from 'vite-plugin-compression2'

export default defineConfig({
  plugins: [
    {
      name: 'public-simulation-assets',
      configureServer(server) {
        server.middlewares.use((request, response, next) => {
          // Sandboxed simulations have an opaque origin. Only public media
          // receives CORS access; authenticated API responses stay private.
          if (request.url?.startsWith('/media/')) {
            response.setHeader('Access-Control-Allow-Origin', '*');
          }
          next();
        });
      },
    },
    react(),
    tailwindcss(),
    compression({ exclude: [/\.(png|jpg|jpeg|gif|webp|woff2?|ttf|eot)$/i] }),
  ],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // Vendor: React core (shared by every route)
          'vendor-react': ['react', 'react-dom', 'react-router-dom'],
          // Vendor: heavy libs loaded only when needed
          'vendor-pdf': ['pdfjs-dist', 'jspdf', 'html2canvas'],
          'vendor-katex': ['katex', 'react-katex'],
          // Zustand + axios are small but used everywhere
          'vendor-state': ['zustand', 'axios'],
        },
      },
    },
  },
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8000',
      '/ws': {
        target: 'ws://127.0.0.1:8000',
        ws: true,
      },
    },
  },
})
