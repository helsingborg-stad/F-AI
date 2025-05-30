import { defineConfig } from 'vitest/config'
import { sveltekit } from '@sveltejs/kit/vite'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [sveltekit()],
  resolve: {
    alias: {
      $lib: '/src/lib',
      $stories: fileURLToPath(new URL('./src/stories', import.meta.url)),
    },
  },
  test: {
    environment: 'node',
    globals: true,
    include: ['src/**/*.{test,spec}.{js,ts}'],
  },
})
