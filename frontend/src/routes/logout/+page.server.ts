import { redirect } from '@sveltejs/kit'
import { api } from '$lib/api-fetch-factory.js'
import { clearUser } from '$lib/state/user.svelte.js'

export const actions = {
  default: async (event) => {
    api.post('/api/login/logout', { withAuth: true, event }).catch(() => {
    })

    clearUser()

    event.cookies.delete('access_token', { path: '/' })
    event.cookies.delete('refresh_token', { path: '/' })

    throw redirect(303, '/login')
  },
}
