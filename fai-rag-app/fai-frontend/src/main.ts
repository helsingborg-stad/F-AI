import './app.css'
import App from './App.svelte'
import {setupGlobalErrorHandlers} from "./util/errorHandling";

setupGlobalErrorHandlers()

const app = new App({
    target: document.getElementById('app') as Element,

})

export default app
