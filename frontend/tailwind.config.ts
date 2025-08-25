import typography from '@tailwindcss/typography'
import type { Config } from 'tailwindcss'
import daisyui from 'daisyui'

export default {
  content: [
    './src/**/*.{html,js,svelte,ts}',
    './node_modules/daisyui/dist/**/*.js',
    './node_modules/daisyui/**/*.js',
    './node_modules/@storybook/**/*.js',
  ],

  daisyui: {
    themes: ['light'],
  },

  plugins: [typography, daisyui],
} satisfies Config
