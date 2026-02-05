              import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // Serve built assets from Django static URL
  base: '/static/frontend/',
  build: {
    // Build directly into Django's static folder so collectstatic picks it up
    outDir: 'backend/static/frontend',
    emptyOutDir: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'axios', 'framer-motion'],
          ui: ['lucide-react', 'gsap'],
        },
      },
    },
  },
})
