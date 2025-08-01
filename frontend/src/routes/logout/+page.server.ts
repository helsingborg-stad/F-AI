import { redirect } from '@sveltejs/kit'
import { clearUser } from '$lib/state/user.svelte.js'
import { BackendApiServiceFactory } from '$lib/backendApi/backendApi.js'

export const actions = {
  default: async (event) => {
    const api = new BackendApiServiceFactory().get(event)
    const [error] = await api.logout()

    if (error) {
      console.error('Failed to logout', error)
    }

    clearUser()

    event.cookies.delete('access_token', { path: '/' })
    event.cookies.delete('refresh_token', { path: '/' })

    throw redirect(303, '/login')
  },
}
