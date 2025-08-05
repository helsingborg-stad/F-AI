import { sequence } from '@sveltejs/kit/hooks'
import { paraglideMiddleware } from '$lib/paraglide/server.js'
import { type Handle, redirect } from '@sveltejs/kit'
import { BackendApiServiceFactory } from '$lib/backendApi/backendApi.js'

/**
 * Check if the user is authenticated, and if not redirect to login page.
 * This hook is needed as an early entrypoint to potentially refresh the
 * login token, since consequent load functions are run in parallel and
 * the login cannot be refreshed properly if needed.
 * See https://svelte.dev/docs/kit/load#Implications-for-authentication
 */
const checkAuthentication: Handle = async ({ event, resolve }): Promise<Response> => {
  const isLoginPath = event.url.pathname === '/login'

  if (isLoginPath) {
    // Authenticated user is not required for login paths
    return resolve(event)
  }

  const api = new BackendApiServiceFactory().get(event)
  const [error] = await api.getScopes()

  if (error) {
    /**
     * If we're unable to get scopes, it most likely means the user is not logged in,
     * either from being completely logged out or unable to refresh login.
     */
    redirect(301, '/login')
  }

  return resolve(event)
}

const handleParaglide: Handle = ({ event, resolve }) =>
  paraglideMiddleware(event.request, ({ request, locale }) => {
    event.request = request

    return resolve(event, {
      transformPageChunk: ({ html }) => html.replace('%paraglide.lang%', locale),
    })
  })

export const handle = sequence(checkAuthentication, handleParaglide)
