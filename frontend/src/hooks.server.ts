import { type Handle, redirect } from '@sveltejs/kit'
import { handleAccess } from '$lib/server/hooks/handle-access.js'
import { setupScopes } from '$lib/server/hooks/setup-scopes.js'
import { compose } from '$lib/server/hooks/compose.js'

export const handle: Handle = async ({ event, resolve }) => {
  event = await compose(
    handleAccess,
    setupScopes
  )(event)

  const response = await resolve(event)

  if (response.status === 401) {
    return redirect(303, '/login')
  }

  return response
}
