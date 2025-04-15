import { redirect } from '@sveltejs/kit'
import { api } from '$lib/api-fetch-factory.js'
import { clearUser } from '$lib/state/user.svelte.js'

export const actions = {
  default: async (event) => {
    await api.post('/api/login/logout', { withAuth: false, event })

    clearUser()
    event.cookies.set('access_token', '', {
      path: '/',
      httpOnly: true,
      sameSite: 'lax',
      secure: true,
      maxAge: 0,
    })

    throw redirect(303, '/login')
  },
}
