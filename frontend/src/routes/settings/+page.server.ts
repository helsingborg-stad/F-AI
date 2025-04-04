import type { PageServerLoad } from './$types.js';
import { error } from '@sveltejs/kit'
import { api } from '$lib/api-fetch-factory.ts'

export const load: PageServerLoad = async (event) => {
  const response = await api.get('/api/settings/settings', { event })

  if (!response.ok) {
    error(response.status)
  }

  const data = await response.json()
  return { authenticated: true, data }
}
