import { canCreateAssistant, canReadAssistants } from '$lib/state/user.svelte.js'
import type { IMenuItem } from '$lib/types.js'

export function load() {
  const sidebarMenu: IMenuItem[] = []

  if (canReadAssistants()) {
    sidebarMenu.push({ label: 'Assistant Zoo', path: '/assistant/zoo' })
  }

  if (canCreateAssistant()) {
    sidebarMenu.push({ label: 'Your assistants', path: '/assistant/edit' })
  }
  return {
    sidebarMenu,
  }
}
