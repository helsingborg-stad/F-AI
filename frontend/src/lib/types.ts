import type { icons } from '$lib/components/Icon/icons.js'

export interface IMenuItem {
  label: string
  path: string
}

export type MessageType = {
  sender: 'user' | 'bot'
  text: string
}

export type ItemOptionsType = {
  iconName: keyof typeof icons
  title: string
  onClick: () => void
}

export type HistoryItemType = {
  title: string
  itemOptions: ItemOptionsType[]
  created: Date
}

export type UserScope =
  | 'collection.read'
  | 'collection.write'
  | 'settings.read'
  | 'document.chunk'
  | 'settings.write'
  | 'group.write'
  | 'apiKey.write'
  | 'apiKey.read'
  | 'group.read'
  | 'test'
  | 'llm.run'
  | string // Allow for future scopes

export interface UserInfo {
  authenticated: boolean
  email: string
  scopes: UserScope[]
}

export interface ScopesResponse {
  scopes: UserScope[]
}

// Dummy export to prevent empty module at runtime.
// Fixes Storybook error where module is empty after TypeScript compilation.
export const __types = {}
