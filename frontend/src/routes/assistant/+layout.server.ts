import { m } from '$lib/paraglide/messages.js'
import type { IMenuItem } from '$lib/types.js'
import { canCreateAssistant, canReadAssistants } from '$lib/state/user.svelte.js'

export function load() {
  const sidebarMenu: IMenuItem[] = []

  if (canReadAssistants()) {
    sidebarMenu.push({ label: m.assistant_zoo_sidebar_zoo_label(), path: '/assistant/zoo' })
  }

  if (canCreateAssistant()) {
    sidebarMenu.push({ label: m.assistant_zoo_sidebar_user_assistants_label(), path: '/assistant/edit' })
  }
  return {
    sidebarMenu,
  }
}
