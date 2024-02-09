export const setupGlobalErrorHandlers = () => {
    const showErrorOverlay = (err) => {
        const ErrorOverlay = customElements.get('vite-error-overlay');
        if (ErrorOverlay == null)
            return;
        document.body.appendChild(new ErrorOverlay(err));
    };
    window.addEventListener('error', showErrorOverlay);
    window.addEventListener('unhandledrejection', ({ reason }) => showErrorOverlay(reason));
};
//# sourceMappingURL=errorHandling.js.map