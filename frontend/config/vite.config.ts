import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vite.dev/config/
export default defineConfig({
  root: 'web',
  plugins: [svelte()],
  server: {
    watch: {
      usePolling: true, // В Docker это важно!
      interval: 100,
    },
    host: true, // Для --host
    strictPort: true,
    port: 5173, // Убедись, что порт совпадает
  },
})
