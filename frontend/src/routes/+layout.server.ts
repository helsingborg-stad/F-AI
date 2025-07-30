import { setUser } from '$lib/state/user.svelte.js'
import { m } from '$lib/paraglide/messages.js'
import type { RequestEvent } from '@sveltejs/kit'
import { userCanChat, userCanReadAssistants, userCanReadSettings } from '$lib/utils/scopes.js'

export async function load(event: RequestEvent) {
  const user = event.locals.user || { email: '' }
  setUser(user)

  const navbarMenu = []

  if (await userCanChat(event)) {
    navbarMenu.push({ label: m.nav_menu_chat(), path: '/chat' })
  }

  if (await userCanReadAssistants(event)) {
    navbarMenu.push({ label: m.nav_menu_assistants(), path: '/assistant' })
  }

  if (await userCanReadSettings(event)) {
    navbarMenu.push({ label: m.nav_menu_settings(), path: '/settings' })
  }

  return {
    user: event.locals.user || { email: '' },
    avatarMenu: [
      {
        title: m.nav_avatar_menu_logout(),
        action: '/logout',
      },
    ],
    navbar: {
      title: m.nav_title(),
      navbarMenu: navbarMenu,
      navbarAvatar: {
        avatarMenu: [
          {
            title: m.nav_avatar_menu_logout(),
            action: '/logout',
          },
        ],
      },
    },
  }
}
