/// <reference types="svelte" />
/// <reference types="vite/client" />
declare namespace svelteHTML {
    interface HTMLAttributes<T> {
        'on:felteerror'?: (event: any) => any;
        'on:feltesuccess'?: (event: any) => any;
    }
}