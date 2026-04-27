import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { compression } from 'vite-plugin-compression2'

export default defineConfig({
  plugins: [
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
