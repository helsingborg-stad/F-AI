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
  itemOptions: ItemOptionsType
}

// Dummy export to prevent empty module at runtime.
// Fixes Storybook error where module is empty after TypeScript compilation.
export const __types = {}
