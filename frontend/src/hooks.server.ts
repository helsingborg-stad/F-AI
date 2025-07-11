import { sequence } from '@sveltejs/kit/hooks'
import { paraglideMiddleware } from '$lib/paraglide/server.js'
import { type Handle, redirect } from '@sveltejs/kit'
import { setupScopes } from '$lib/server/hooks/setup-scopes.js'

const handleScopes: Handle = async ({ event, resolve }) => {
  try {
    event = await setupScopes(event)

    const response = await resolve(event)

    if (response.status === 401) {
      return redirect(303, '/login')
    }

    return response
  } catch (error) {
    console.log('Hook error:', error)

    if (error instanceof Response && error.status === 401) {
      return redirect(303, '/login')
    }

    // TODO: Implement error page for other type of errors.
    return redirect(303, '/login')
  }
}

const handleParaglide: Handle = ({ event, resolve }) =>
  paraglideMiddleware(event.request, ({ request, locale }) => {
    event.request = request

    return resolve(event, {
      transformPageChunk: ({ html }) => html.replace('%paraglide.lang%', locale),
    })
  })

export const handle = sequence(handleScopes, handleParaglide)
