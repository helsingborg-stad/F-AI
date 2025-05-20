import type { RequestHandler } from './$types.js'
import { api } from '$lib/api-fetch-factory.js'
import { error, text } from '@sveltejs/kit'

export const POST: RequestHandler = async (event) => {
  const { id }: { id: string } = await event.request.json()

  const response = await api.delete(`/api/conversation/${id}`, { event })

  if (!response.ok) {
    error(response.status, await response.text())
  }

  return text('')
}