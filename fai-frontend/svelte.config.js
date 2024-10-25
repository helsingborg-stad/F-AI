import {vitePreprocess} from '@sveltejs/vite-plugin-svelte'
import {inlineSvg} from '@svelte-put/preprocess-inline-svg/vite'

export default {
    // Consult https://svelte.dev/docs#compile-time-svelte-preprocess
    // for more information about preprocessors
    preprocess: [vitePreprocess()],
    compilerOptions: {
        customElement: true,
    },
    plugins: [
        inlineSvg(),
    ],
}
