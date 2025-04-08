// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
import type { UserInfo } from '$lib/types.js'

declare global {
  namespace App {
    // interface Error {}
    interface Locals {
      user?: UserInfo
    }
    // interface PageData {}
    // interface PageState {}
    // interface Platform {}
  }
}

export {}
