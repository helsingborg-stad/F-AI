import type { RequestHandler } from './$types.js'
import { BackendApiServiceFactory } from '$lib/backendApi/backendApi.js'
import { text } from '@sveltejs/kit'

export const PATCH: RequestHandler = async (event) => {
  const { id } = event.params
  const { title } = await event.request.json()

  const api = new BackendApiServiceFactory().get(event)
  const [error] = await api.updateConversationTitle(id, title)

  if (error) {
    throw new Response('Failed to update title', { status: 500 })
  }

  return text('')
}
