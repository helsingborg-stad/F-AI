import type { RequestEvent } from '@sveltejs/kit'
import { api } from '$lib/api-fetch-factory.js'

export async function getSettings(event: RequestEvent) {
  const response = await api.get('/api/settings/settings', { event })

  if (!response.ok) {
    throw new Response('Failed to fetch settings', { status: response.status })
  }

  return await response.json()
}