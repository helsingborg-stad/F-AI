import type {ErrorPayload} from "vite/types/hmrPayload.js"

export const setupGlobalErrorHandlers = () => {
    const showErrorOverlay = (err: Partial<ErrorPayload['err']>) => {
        const ErrorOverlay = customElements.get('vite-error-overlay')
        if (ErrorOverlay == null) return
        document.body.appendChild(new ErrorOverlay(err))
    }

    window.addEventListener('error', showErrorOverlay)
    window.addEventListener('unhandledrejection', ({reason}) => showErrorOverlay(reason))
};