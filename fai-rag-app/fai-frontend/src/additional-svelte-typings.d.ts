/// <reference types="svelte" />
/// <reference types="vite/client" />

declare global {
  declare namespace svelteHTML {
    interface HTMLAttributes<T> {
      'on:felteerror'?: (event: any) => any
      'on:feltesuccess'?: (event: any) => any
      disabled?: boolean | null
    }
  }

  type EventElements = Event & {
    currentTarget: EventTarget & HTMLInputElement
  }
}
export {}
