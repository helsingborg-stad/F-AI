import { hasScope, setUser } from '$lib/state/user.svelte.js'

export function load({ locals }) {
  const user = locals.user || { scopes: [], email: '' }
  setUser(user)

  const navbarMenu = [
    { label: 'Chat', path: '/chat' },
    { label: 'Assistants', path: '/assistant' },
  ]

  if (hasScope('settings.read')) {
    navbarMenu.push({ label: 'Settings', path: '/settings' })
  }

  return {
    user: locals.user || { scopes: [], email: '' },
    avatarMenu: [
      {
        title: 'Logout',
        action: '/logout',
      },
    ],
    navbar: {
      title: 'Folkets AI',
      navbarMenu: navbarMenu,
      navbarAvatar: {
        avatarMenu: [
          {
            title: 'Logout',
            action: '/logout',
          },
        ],
      },
    },
  }
}
