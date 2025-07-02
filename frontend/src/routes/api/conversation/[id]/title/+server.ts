import type { RequestHandler } from './$types.js'
import { api } from '$lib/api-fetch-factory.js'
import { error, text } from '@sveltejs/kit'

export const PATCH: RequestHandler = async (event) => {
  const { id } = event.params
  const { title } = await event.request.json()

  const response = await api.patch(`/api/conversation/${id}/title`, {
    event,
    body: { title },
  })

  if (!response.ok) {
    error(response.status, await response.text())
  }

  return text('')
}
