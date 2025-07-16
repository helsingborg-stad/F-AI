import { hasScope, setUser } from '$lib/state/user.svelte.js'
import { m } from '$lib/paraglide/messages.js'

export function load({ locals }) {
  const user = locals.user || { scopes: [], email: '' }
  setUser(user)

  const navbarMenu = []

  if (hasScope('chat')) {
    navbarMenu.push({ label: m.nav_menu_chat(), path: '/chat' })
  }

  if (hasScope('assistant.read')) {
    navbarMenu.push({ label: m.nav_menu_assistants(), path: '/assistant' })
  }

  if (hasScope('settings.read')) {
    navbarMenu.push({ label: m.nav_menu_settings(), path: '/settings' })
  }

  return {
    user: locals.user || { scopes: [], email: '' },
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