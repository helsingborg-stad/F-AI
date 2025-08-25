import type { RequestHandler } from './$types.js'
import { json } from '@sveltejs/kit'
import { BackendApiServiceFactory } from '$lib/backendApi/backendApi.js'

export const POST: RequestHandler = async (event) => {
  const { id }: { id: string } = await event.request.json()

  const api = new BackendApiServiceFactory().get(event)
  const [error] = await api.deleteConversation(id)

  if (error) {
    return json({ success: false, error }, { status: 500 })
  }

  return json({ success: true })
}
