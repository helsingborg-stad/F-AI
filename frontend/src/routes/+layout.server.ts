import { setUser } from '$lib/state/user.svelte.js'
import { m } from '$lib/paraglide/messages.js'
import type { RequestEvent } from '@sveltejs/kit'
import { userCanChat, userCanReadAssistants, userCanReadSettings } from '$lib/utils/scopes.js'

export async function load(event: RequestEvent) {
  console.log('=== LAYOUT LOAD START ===')
  console.log('URL:', event.url.pathname)
  console.log('Cookies:', event.cookies.getAll())

  const user = event.locals.user || { email: '' }
  setUser(user)

  const navbarMenu = []

  try {
    console.log('Checking userCanChat...')
    const canChat = await userCanChat(event)
    console.log('userCanChat result:', canChat)

    if (canChat) {
      navbarMenu.push({ label: m.nav_menu_chat(), path: '/chat' })
    }

    console.log('Checking userCanReadAssistants...')
    const canReadAssistants = await userCanReadAssistants(event)
    console.log('userCanReadAssistants result:', canReadAssistants)

    if (canReadAssistants) {
      navbarMenu.push({ label: m.nav_menu_assistants(), path: '/assistant' })
    }

    console.log('Checking userCanReadSettings...')
    const canReadSettings = await userCanReadSettings(event)
    console.log('userCanReadSettings result:', canReadSettings)

    if (canReadSettings) {
      navbarMenu.push({ label: m.nav_menu_settings(), path: '/settings' })
    }
  } catch (error) {
    console.error('Error in layout load:', error)
  }

  console.log('Final navbarMenu:', navbarMenu)
  console.log('=== LAYOUT LOAD END ===')

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