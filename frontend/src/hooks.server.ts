import { type Handle, redirect } from '@sveltejs/kit'
import { handleAccess } from '$lib/server/hooks/handle-access.js'
import { setupScopes } from '$lib/server/hooks/setup-scopes.js'
import { compose } from '$lib/server/hooks/compose.js'

export const handle: Handle = async ({ event, resolve }) => {
  try {
    event = await compose(handleAccess, setupScopes)(event)

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
