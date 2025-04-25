import type { RequestEvent } from '@sveltejs/kit'
import { api } from '$lib/api-fetch-factory.js'
import type { IScopesResponse } from '$lib/types.js'

export async function setupScopes(
  event: RequestEvent<Partial<Record<string, string>>, string | null>,
) {
  const path = event.url.pathname
  const publicPaths = ['/login']

  const isPublicPath = publicPaths.some((publicPath) => publicPath === path)
  const accessToken = event.cookies.get('access_token')

  // Set default values
  event.locals.user = {
    ...event.locals.user,
    scopes: [],
  }

  if (accessToken && !isPublicPath) {
      const response = await api.get('/api/auth/scopes', { withAuth: true, event })

      if (response.ok) {
        const scopesData: IScopesResponse = await response.json()

        event.locals.user = {
          scopes: scopesData.scopes || [],
        }
      }
  }

  return event
}
