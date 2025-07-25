import { m } from '$lib/paraglide/messages.js'
import type { IMenuItem } from '$lib/types.js'
import type { RequestEvent } from '@sveltejs/kit'
import { userCanReadAssistants, userCanWriteAssistant } from '$lib/utils/scopes.js'

export async function load(event: RequestEvent) {
  const sidebarMenu: IMenuItem[] = []

  if (await userCanReadAssistants(event)) {
    sidebarMenu.push({
      label: m.assistant_zoo_sidebar_zoo_label(),
      path: '/assistant/zoo',
    })
  }

  if (await userCanWriteAssistant(event)) {
    sidebarMenu.push({
      label: m.assistant_zoo_sidebar_user_assistants_label(),
      path: '/assistant/edit',
    })
  }
  return {
    sidebarMenu,
  }
}
