/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/**/*.{svelte,js,ts,jsx,tsx,py}",
        "./src/fai_backend/*/*.{svelte,js,ts,jsx,tsx,py}",
        "../fai-backend/fai_backend/*/*.py",
    ],
    theme: {
        extend: {},
    },
    plugins: [require("@tailwindcss/typography"), require("daisyui"), require('autoprefixer')],
    daisyui: {
        themes: [
            "corporate",
            "business"
        ],
    },
}

