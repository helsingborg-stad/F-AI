import { setUser } from '$lib/state/user.svelte.js'
import { m } from '$lib/paraglide/messages.js'
import { type RequestEvent } from '@sveltejs/kit'
import {
  userCanChat,
  userCanReadAssistants,
  userCanReadSettings,
} from '$lib/utils/scopes.js'

export async function load(event: RequestEvent) {
  const user = event.locals.user || { email: '' }
  setUser(user)

  const navbarMenu = []

  const canChat = await userCanChat(event)

  if (canChat) {
    navbarMenu.push({ label: m.nav_menu_chat(), path: '/chat' })
  }

  const canReadAssistants = await userCanReadAssistants(event)

  if (canReadAssistants) {
    navbarMenu.push({ label: m.nav_menu_assistants(), path: '/assistant' })
  }

  const canReadSettings = await userCanReadSettings(event)

  if (canReadSettings) {
    navbarMenu.push({ label: m.nav_menu_settings(), path: '/settings' })
  }

  return {
    user,
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
