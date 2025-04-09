// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
import type { IUserInfo } from '$lib/types.js'

declare global {
  namespace App {
    // interface Error {}
    interface Locals {
      user?: IUserInfo
    }
    // interface PageData {}
    // interface PageState {}
    // interface Platform {}
  }
}

export {}
