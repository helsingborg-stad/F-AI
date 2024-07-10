import {defineConfig} from 'vite'
import {svelte} from '@sveltejs/vite-plugin-svelte'
import * as path from "path";

// https://vitejs.dev/config/
export default () => {
    const serverConfig = {
        host: true,
        port: 3000,
        hmr: {
            // If your frontend is on a different port than your FastAPI server
            port: 3000, // the port your Vite app runs on
            clientPort: 3000 // if your browser is on a different port
        },
        proxy: {
            '/api': 'http://localhost:8000',
        },
    }


    return defineConfig({
        plugins: [svelte()],
        server: serverConfig,
        preview: serverConfig,
        resolve: {
            alias: {
                $lib: path.resolve('./src/lib'),
            }
        }

    })
}

