/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/**/*.{svelte,js,ts,jsx,tsx}",
        "../fai-backend/fai_backend/**/**/*.py",
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

