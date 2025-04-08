import type { RequestEvent } from '@sveltejs/kit'
import { api } from '$lib/api-fetch-factory.js'
import type { ScopesResponse } from '$lib/types.js'

export async function setupScopes(
  event: RequestEvent<Partial<Record<string, string>>, string | null>,
) {
  const path = event.url.pathname
  const publicPaths = ['/login']

  const isPublicPath = publicPaths.some((publicPath) => publicPath === path)
  const accessToken = event.cookies.get('access_token')

  // Set default values
  event.locals.user = {
    authenticated: false,
    scopes: [],
    email: '',
  }

  if (accessToken && !isPublicPath) {
    try {
      const scopesResponse = await api.get('/api/auth/scopes', { withAuth: true, event })

      if (scopesResponse.ok) {
        const scopesData: ScopesResponse = await scopesResponse.json()

        event.locals.user = {
          authenticated: true,
          scopes: scopesData.scopes || [],
          email: '',
        }
      }
    } catch (e) {
      console.log('Failed to fetch user scopes:', e)
    }
  }

  return event
}
