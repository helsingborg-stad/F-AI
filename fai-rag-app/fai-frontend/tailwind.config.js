/** @type {import("tailwindcss").Config} */
import typography from "@tailwindcss/typography";
import daisyui from "daisyui";
import autoprefixer from "autoprefixer";

export default {
  content: [
    "./index.html",
    "./src/**/**/*.{svelte,ts,jsx,tsx,py}",
    "./src/fai_backend/*/*.{svelte,ts,jsx,tsx,py}",
    "../fai-backend/fai_backend/*/*.py"
  ],
  theme: {
    extend: {}
  },
  plugins: [typography, daisyui, autoprefixer],
  daisyui: {
    themes: [
      "corporate",
      "business"
    ]
  }
};
